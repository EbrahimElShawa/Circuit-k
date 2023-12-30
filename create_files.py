from Secondary_Interfaces import component_list, magnitude_list, ramp_time_list, nodes_list, freq_list, wave_type_list, \
    angle_list, max_time, step
import os


def delete_files():

    # Specify the directory path
    directory_path = 'asset/net'

    # List all files in the directory
    files_in_directory = os.listdir(directory_path)

    # Iterate through the files and delete them
    for file_name in files_in_directory:
        file_path = os.path.join(directory_path, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def netlist():
    with open('assets/net/net.txt', 'w') as file:
        # Write content to the file
        for i in range(len(component_list)):
            comp_name = component_list[i] + str(i)
            if component_list[i] not in "R" and "L" and "C":
                create_source_file(i)
                file.write(comp_name + " " + nodes_list[i][0] + " " + nodes_list[i][1] + "\n")
            else:
                file.write(comp_name + " " + nodes_list[i][0] + " " + nodes_list[i][1] + " " + magnitude_list[i] +"\n")


def create_source_file(index):
    with open("assets/net/net" + component_list[index] + str(index) + ".txt", 'w') as file:
        file.write("Type\n")
        file.write(wave_type_list[index] + "\n")
        file.write("Ramp up time" + "\n")
        file.write(ramp_time_list[index] + "\n")
        file.write("Magnitude" + "\n")
        file.write(magnitude_list[index] + "\n")
        file.write("Frequency" + "\n")
        file.write(freq_list[index] + "\n")
        file.write("Phase" + "\n")
        file.write(angle_list[index] + "\n")


def create_time_file():
    with open("assets/net/net_cond.txt", 'w') as file:
        file.write("0 " + max_time + " " + step + "\n")


def create():
    delete_files()
    netlist()
    create_time_file()
