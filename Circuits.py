import pandas as pd
import numpy as np
import os
from circuitTools import evaluate_equation_for_range
from Secondary_Interfaces import progress_bar_window, update

pi = np.pi
exp = np.exp
sin = np.sin
sqrt = np.sqrt


class Circuit:
    def __init__(self, data_file):
        with open(data_file[:-4] + '_cond.txt') as reader:
            first_line = reader.readline().split()
            if len(first_line) != 0:
                self._circuit = TimeDomainCircuit(data_file)
            else:
                raise ValueError(f'The format of {data_file[:-4]}_cond.txt is invalid. \n'
                                 'The first line should be "tmin tmax step" or "fmin fmax step".')

    @property
    def domain_vec(self):
        if isinstance(self._circuit, TimeDomainCircuit):
            return self._circuit.t_vec

    @property
    def node_voltages(self):
        if isinstance(self._circuit, TimeDomainCircuit):
            return self._circuit.node_voltages

    @property
    def branch_voltages(self):
        if isinstance(self._circuit, TimeDomainCircuit):
            return self._circuit.branch_voltages

    @property
    def currents(self):
        if isinstance(self._circuit, TimeDomainCircuit):
            return self._circuit.currents


class TimeDomainCircuit:
    comp_types = {'R': 0, 'L': 1, 'C': 2, 'V': 10, 'I': 20}

    def __init__(self, data_file):
        progress_bar_window()
        self.dirname = os.path.dirname(data_file)
        self.data_df = pd.read_csv(data_file, sep=' ',
                                   names=['Component Name', 'From Node', 'To Node', 'Value'])
        self.data_df.loc[:, ['From Node', 'To Node']] = self.data_df.loc[:, ['From Node', 'To Node']].astype(str)
        mask = self.data_df['Component Name'].str.startswith(('Ieq', 'Veq'))
        self.data_df.loc[mask, 'Value'] = '-1'
        self.unique_user_nodes = self.unique_nodes()
        self.nodes_transf = self.trandform_nodes()
        self._data_arr = self._df_to_array()
        self._masks = {
            comp_type: self._data_arr[:, 0] == type_code
            for comp_type, type_code in TimeDomainCircuit.comp_types.items()
        }
        self.domain_range = pd.read_csv(data_file[:-4] + '_cond.txt', sep=" ",
                                        names=['D min', 'D max', 'step'])
        self.domain_vec = self._get_domain_vec()
        self.no_nodes = int(self._data_arr[:, [1, 2]].max())
        self.no_branches = int(self._data_arr.shape[0])
        self._v_s_list = self._get_sources_list('V')
        self._i_s_list = self._get_sources_list('I')
        self._inc_mat = self._calc_inc_mat()
        self._v_adj = self._inc_mat[:, self._masks['V']]
        self.t_vec = self._get_domain_vec()
        self.time_step = self.t_vec[1] - self.t_vec[0]
        self.t_max = self.domain_range.iloc[0, -2]
        self._v_s = self._get_sources('V')
        self._i_s = self._get_sources('I')
        self._y_b = self._calc_y_b()
        self._y_n = self._calc_y_n()
        self._mna_mat = self._calc_mna_mat()
        self.v_n = np.zeros((self.no_nodes, len(self.t_vec)))
        self.v_b = np.zeros((self.no_branches, len(self.t_vec)))
        self.i_b = np.zeros((self.no_branches, len(self.t_vec)))
        self._current_sources = self._data_arr[self._masks['I']]
        self._inductors = self._data_arr[self._masks['L']]
        self._capacitors = self._data_arr[self._masks['C']]
        self.no_inductors = len(self._inductors)
        self.no_capacitors = len(self._capacitors)
        self.no_current_sources = len(self._current_sources)
        self._solve_circuit()
        self.node_voltages = self.create_df('V')
        self.branch_voltages = self.create_df('V', isbranch=True)
        self.currents = self.create_df('I', isbranch=True)

    def _df_to_array(self):
        data_transf = self.data_df.copy()
        # to convert '0' to 0 ( object to int ) in data_trans
        data_transf.replace({'From Node': self.nodes_transf, 'To Node': self.nodes_transf}, inplace=True)
        data_transf['Component Name'] = self.data_df['Component Name'].map(
            lambda name: TimeDomainCircuit.comp_types[name[0]])
        return np.array(data_transf, dtype=float)

    # MAKE A LIST WHICH STORE THE SOURCES AND THEIR COMPONANTS
    def _get_sources_list(self, source_nature):
        sources_data = self.data_df[self.data_df['Component Name'].str[0] == source_nature]
        x = sources_data['Component Name'].to_list()
        sources_list = []
        for i in x:
            sources_list.append(
                [
                    pd.read_csv(os.path.join(self.dirname, i + '.txt'), sep=' ', names=[i])
                ]
            )
        return sources_list

    def _get_domain_vec(self):
        tmin, tmax, step = self.domain_range.iloc[0, :]
        tmin = float(tmin)
        tmax = float(tmax)
        step = float(step)
        if step == 0.0:
            return np.array([tmin], dtype=float)
        else:
            return np.arange(tmin, tmax + step, step, dtype=float)  # to get full range

    def _calc_inc_mat(self):
        inc_mat = np.zeros((self.no_nodes, self.no_branches))
        for b in range(0, self.no_branches):
            node_from = int(self._data_arr[b, 1])
            node_to = int(self._data_arr[b, 2])
            if node_from != 0:
                inc_mat[node_from - 1, b] = 1
            if node_to != 0:
                inc_mat[node_to - 1, b] = -1
        return inc_mat

    def unique_nodes(self):
        user_nodes_flat = pd.concat([self.data_df['From Node'], self.data_df['To Node']])
        return user_nodes_flat.unique()

    def trandform_nodes(self):
        nodes_transf = {'0': 0}
        k = 1
        for user_node in self.unique_user_nodes:
            if user_node != '0':
                nodes_transf[user_node] = k
                k = k + 1
        return nodes_transf

    def _get_sources(self, source_nature):
        source_list = self._v_s_list if source_nature == 'V' else self._i_s_list
        sources = np.zeros((len(source_list), len(self.t_vec)))
        for idx, source in enumerate(source_list):  # v1 , v2 , v3
            ramp_up = float(list(source[0].loc[3])[0])
            mag = float(list(source[0].loc[5])[0])
            bf_ramp = self.t_vec < ramp_up  # mask for before ramp
            aft_ramp = self.t_vec >= ramp_up  # mask for after ramp
            skip = ramp_up == 0
            if list(source[0].loc[1])[0] == 'DC':
                if skip:
                    sources[idx, :] = mag
                else:
                    slope = mag / ramp_up
                    sources[idx, bf_ramp] = slope * self.t_vec[bf_ramp]
                    sources[idx, aft_ramp] = mag

            elif list(source[0].loc[1])[0] == 'SINE':
                frq = float(list(source[0].loc[7])[0])
                ang = float(list(source[0].loc[9])[0])
                w = 2 * pi * frq
                if skip:
                    sources[idx, :] = mag * np.sqrt(2) * np.sin(w * self.t_vec[:] + np.radians(ang))
                else:
                    slope = mag * np.sqrt(2) / ramp_up
                    sources[idx, bf_ramp] = slope * np.sin(w * self.t_vec[bf_ramp] + np.radians(ang)) * self.t_vec[
                        bf_ramp]
                    sources[idx, aft_ramp] = mag * np.sqrt(2) * np.sin(w * self.t_vec[aft_ramp] + np.radians(ang))

            elif list(source[0].loc[1])[0] == 'RECTANGLE':
                frq = float(list(source[0].loc[7])[0])
                ang = float(list(source[0].loc[9])[0])
                w = 2 * pi * frq
                if skip:
                    sources[idx, :] = mag * np.sign(np.sin(w * self.t_vec[:] + np.radians(ang)))
                else:
                    slope = mag / ramp_up
                    sources[idx, bf_ramp] = slope * np.sign(np.sin(w * self.t_vec[bf_ramp] + np.radians(ang))) * \
                                            self.t_vec[bf_ramp]
                    sources[idx, aft_ramp] = mag * np.sign(np.sin(w * self.t_vec[aft_ramp] + np.radians(ang)))



            elif list(source[0].loc[1])[0] == 'TRIANGLE':
                frq = float(list(source[0].loc[7])[0])
                ang = float(list(source[0].loc[9])[0])
                w = 2 * pi * frq
                if skip:
                    sources[idx, :] = (2 * mag * np.sqrt(3) / pi) * np.arcsin(
                        np.sin(w * self.t_vec[:] + np.radians(ang)))
                else:
                    slope = mag * np.sqrt(3) / ramp_up
                    sources[idx, bf_ramp] = (2 * slope / pi) * np.arcsin(
                        np.sin(w * self.t_vec[bf_ramp] + np.radians(ang))) * self.t_vec[bf_ramp]
                    sources[idx, aft_ramp] = (2 * mag * np.sqrt(3) / pi) * np.arcsin(
                        np.sin(w * self.t_vec[aft_ramp] + np.radians(ang)))



            elif list(source[0].loc[1])[0] == 'SAWTOOTH':
                frq = float(list(source[0].loc[7])[0])
                ang = float(list(source[0].loc[9])[0])
                w = 2 * pi * frq
                if skip:
                    sources[idx, :] = (2 * mag * np.sqrt(3) / np.pi) * np.arctan(
                        np.tan(np.pi * self.t_vec[:] / (1 / frq) + np.radians(ang)))
                else:
                    slope = mag * np.sqrt(3) / ramp_up
                    sources[idx, bf_ramp] = (2 * slope / np.pi) * np.arctan(
                        np.tan(np.pi * self.t_vec[bf_ramp] / (1 / frq) + np.radians(ang))) * self.t_vec[bf_ramp]
                    sources[idx, aft_ramp] = (2 * mag * np.sqrt(3) / np.pi) * np.arctan(
                        np.tan(np.pi * self.t_vec[aft_ramp] / (1 / frq) + np.radians(ang)))
            else:
                sources[idx] = evaluate_equation_for_range(list(source[0].loc[1])[0], self.t_vec)

        return sources

    def _calc_branch_adm(self, branch):
        if branch[0] == TimeDomainCircuit.comp_types['R']:
            return 1 / branch[3]
        elif branch[0] == TimeDomainCircuit.comp_types['L']:
            return self.time_step / (2 * branch[3])
        elif branch[0] == TimeDomainCircuit.comp_types['C']:
            return ((2 * branch[3]) / self.time_step)

    def _calc_y_b(self):
        y_b = np.zeros((self.no_branches, self.no_branches))
        for i in range(self.no_branches):
            if self._data_arr[i, 0] in [TimeDomainCircuit.comp_types['R'], TimeDomainCircuit.comp_types['L'],
                                        TimeDomainCircuit.comp_types['C']]:
                y_b[i, i] = self._calc_branch_adm(self._data_arr[i, :])
        return y_b

    def _calc_y_n(self):
        y_n = np.zeros((self.no_nodes, self.no_nodes))
        passive_branch = self._data_arr[self._masks['R'] | self._masks['L'] | self._masks['C']]
        for idx in range(passive_branch.shape[0]):
            y = self._calc_branch_adm(passive_branch[idx, :])
            node_from = int(passive_branch[idx, 1])
            node_to = int(passive_branch[idx, 2])
            if node_from != 0:
                y_n[node_from - 1, node_from - 1] += y
                if node_to != 0:
                    y_n[node_to - 1, node_to - 1] += y
                    y_n[node_from - 1, node_to - 1] -= y
                    y_n[node_to - 1, node_from - 1] -= y
            else:
                y_n[node_to - 1, node_to - 1] += y

        return y_n

    def _calc_mna_mat(self):
        upper_mat = np.concatenate((self._y_n, self._v_adj), axis=1)
        bottom_right_mat = np.zeros((self._v_adj.shape[1], self._v_adj.shape[1]))
        lower_mat = np.concatenate((self._v_adj.T, bottom_right_mat), axis=1)
        return np.concatenate((upper_mat, lower_mat), axis=0)

    # بيحسب i_n بتاعت مصادر التيار و coil و capacitor
    def _calc_i_n_nth(self, ind_cur_inj_nth, cap_cur_inj_nth, nth_iter):
        i_n = np.zeros(self.no_nodes)
        # store the branches.
        branches_single_type = [self._current_sources, self._inductors, self._capacitors]
        # store the current that flows in this branches.
        current_injections = [self._i_s[:, nth_iter], ind_cur_inj_nth, cap_cur_inj_nth]
        # make the matrix that detect the current direction of in each branch.
        for br_single_type, current_inj in zip(branches_single_type, current_injections):
            for idx in range(br_single_type.shape[0]):
                node_from = int(br_single_type[idx, 1])
                node_to = int(br_single_type[idx, 2])
                if node_from != 0:
                    i_n[node_from - 1] += -current_inj[idx]
                if node_to != 0:
                    i_n[node_to - 1] += current_inj[idx]
        return i_n

    def _calc_i_b_nth(self, ind_cur_inj_nth, cap_cur_inj_nth, i_v_s_nth, nth_iter):
        i_b_nth = np.zeros(self.no_branches)
        i_b_nth[self._masks['I']] = self._i_s[:, nth_iter]
        i_b_nth[self._masks['V']] = i_v_s_nth
        i_b_nth[self._masks['L']] += ind_cur_inj_nth  # the current of the source of the ind
        i_b_nth[self._masks['C']] += cap_cur_inj_nth  # the current of the source of the cap
        i_b_nth += self._y_b @ self.v_b[:, nth_iter]  # the current of the resistance of coil or capacitor
        return i_b_nth

    def _calc_ind_cur_inj_nth(self, ind_vals, nth_iter):
        prev_br_current = self.i_b[self._masks['L'], nth_iter]
        prev_res_current = self.time_step / (2 * ind_vals) * self.v_b[self._masks['L'], nth_iter]
        # print("xl",1/ (self.time_step / (2 * ind_vals)) ," t",self.time_step)
        return prev_br_current + prev_res_current

    def _calc_cap_cur_inj_nth(self, cap_vals, nth_iter):
        prev_br_current = -self.i_b[self._masks['C'], nth_iter]
        prev_res_current = -2 * cap_vals / self.time_step * self.v_b[self._masks['C'], nth_iter]
        return prev_br_current + prev_res_current

    def _solve_circuit(self):
        ind_cur_inj_nth = np.zeros(self.no_inductors)  # inductive current injection at the nth time step
        cap_cur_inj_nth = np.zeros(self.no_capacitors)  # capacitive current injection at the nth time step
        ind_vals = self._data_arr[self._masks['L'], 3]
        cap_vals = self._data_arr[self._masks['C'], 3]
        print("\n\nstart analyzing .......%")
        for nth_iter in range(len(self.t_vec)):
            cur_time = nth_iter / (self.t_max / self.time_step) * self.t_max
            percentage = (cur_time / self.t_max) * 100
            print(f"{cur_time} second ------ {percentage} %")
            update(percentage, cur_time)
            i_n_kth = self._calc_i_n_nth(ind_cur_inj_nth, cap_cur_inj_nth, nth_iter)
            rhs_nth = np.concatenate((i_n_kth, self._v_s[:, nth_iter]))
            ans_nth = np.linalg.solve(self._mna_mat, rhs_nth)
            self.v_n[:, nth_iter], i_v_s_nth = ans_nth[:self.no_nodes], ans_nth[self.no_nodes:]
            self.v_b[:, nth_iter] = self._inc_mat.T @ self.v_n[:, nth_iter]
            self.i_b[:, nth_iter] = self._calc_i_b_nth(ind_cur_inj_nth, cap_cur_inj_nth, i_v_s_nth, nth_iter)
            ind_cur_inj_nth = self._calc_ind_cur_inj_nth(ind_vals, nth_iter)
            cap_cur_inj_nth = self._calc_cap_cur_inj_nth(cap_vals, nth_iter)

    def create_df(self, signal_type='V', isbranch=False):
        """
        :param signal_type: 'V' (voltage) or 'I' (current)
        :param isbranch: False for Vn, True for Vb and Ib
        :return: a DataFrame object with indices the time vector.
        """
        if not isbranch:
            nodes_labels = self.unique_user_nodes[self.unique_user_nodes != '0']
            col_labels = 'V' + nodes_labels + ' (V)'
            arr = np.array([self.v_n[self.nodes_transf[nodes_labels[i]] - 1] for i in range(self.no_nodes)]).T
        else:
            if signal_type == 'V':
                arr = self.v_b.T
                col_labels_prefix = 'V' + self.data_df.loc[:, 'From Node']
                col_labels_prefix.replace({'V0': ''}, inplace=True)
                col_labels_suffix = '-V' + self.data_df.loc[:, 'To Node']
                col_labels_suffix.replace({'-V0': ''}, inplace=True)
                col_labels = col_labels_prefix + col_labels_suffix + ' (V)'
            else:
                arr = self.i_b.T
                col_labels = 'I' + '(' + self.data_df.loc[:, 'From Node'] + \
                             '->' + self.data_df.loc[:, 'To Node'] + ')' + ' (A)'
        df = pd.DataFrame(
            arr,
            index=self.t_vec,
            columns=col_labels
        )
        df.index.name = 'Time (s)'
        return df
