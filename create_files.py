import os

DIR_PATH = r"assets/net/"


def delete_files():
    files_in_directory = os.listdir(DIR_PATH)

    for file_name in files_in_directory:
        file_path = os.path.join(DIR_PATH, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def netlist():
    from Secondary_Interfaces import component_list, magnitude_list, nodes_list
    with open(DIR_PATH + "net.txt", 'w') as file:
        for i in range(len(component_list)):
            comp_name = component_list[i]
            if component_list[i] == "R":
                comp_name = comp_name + "es" + str(i + 1)
            elif component_list[i] == "C":
                comp_name = comp_name + "ap" + str(i + 1)
            elif component_list[i] == "L":
                comp_name = comp_name + "ci" + str(i + 1)
            else:
                comp_name = comp_name + str(i + 1)
                create_source_file(i)

            file.write(comp_name + " " + nodes_list[i][0] + " " + nodes_list[i][1] + " " + magnitude_list[i] + "\n")


def create_source_file(index):
    from Secondary_Interfaces import component_list, magnitude_list, \
        ramp_time_list, freq_list, wave_type_list, angle_list
    with open(DIR_PATH + component_list[index] + str(index + 1) + ".txt", 'w') as file:
        file.write("Type\n")
        file.write(str(wave_type_list[index]) + "\n")
        file.write("Ramp_up_time" + "\n")
        file.write(str(ramp_time_list[index]) + "\n")
        file.write("Magnitude" + "\n")
        if component_list[index] in ["Ieq", "Veq"]:
            file.write("-1\n")
        else:
            file.write(str(magnitude_list[index]) + "\n")
        file.write("Frequency" + "\n")
        file.write(str(freq_list[index]) + "\n")
        file.write("Phase" + "\n")
        file.write(str(angle_list[index]) + "\n")


def create_time_file(max_time, step):
    with open(DIR_PATH + "net_cond.txt", 'w') as file:
        file.write("0 " + max_time + " " + step + "\n")


def create():
    delete_files()
    netlist()
    create_time_file()
