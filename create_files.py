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
            comp_name = component_list[i] + str(i)
            if component_list[i] not in ["R", "L", "C"]:
                create_source_file(i)
                file.write(comp_name + " " + nodes_list[i][0] + " " + nodes_list[i][1] + "\n")
            else:
                file.write(comp_name + " " + nodes_list[i][0] + " " + nodes_list[i][1] + " " + magnitude_list[i] + "\n")


def create_source_file(index):
    from Secondary_Interfaces import component_list, magnitude_list, \
        ramp_time_list, freq_list, wave_type_list, angle_list
    with open(DIR_PATH + component_list[index] + str(index) + ".txt", 'w') as file:
        file.write("Type\n")
        file.write(str(wave_type_list[index]) + "\n")
        file.write("Ramp_up_time" + "\n")
        file.write(str(ramp_time_list[index]) + "\n")
        file.write("Magnitude" + "\n")
        file.write(str(magnitude_list[index]) + "\n")
        file.write("Frequency" + "\n")
        file.write(str(freq_list[index]) + "\n")
        file.write("Phase" + "\n")
        file.write(str(angle_list[index]) + "\n")


def create_time_file():
    from Secondary_Interfaces import max_time, step
    with open(DIR_PATH + "net_cond.txt", 'w') as file:
        file.write("0 " + max_time + " " + step + "\n")


def create():
    delete_files()
    netlist()
    create_time_file()
