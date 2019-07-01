import os
import sys
import pandas as pd
from termcolor import cprint
from pathlib import Path


def read_doc(file_path):
    """
    Read Data in a file
    """
    if('.csv' in os.path.basename(file_path)):
        data = pd.read_csv(file_path)
    else:
        data = pd.read_excel(file_path)
    return data


def get_headings(df):
    """
    Get a list of the columns in the dataframe.
    """
    return list(df.columns)


def choose_headings(headings):
    """
    Choose a column to split document.
    """
    count = 1
    choice = 0
    for i in headings:
        print(str(count) + '. ' + i)
        count = count + 1
    try:
        choice = int(input("Choose a coloumn: (number of coloumn)"))
    except ValueError:
        cprint("[!!]Warning: Kindly enter a digit.", "yellow")
        choose_headings(headings)
    if((not(choice in range(1, len(headings) + 1)))):
        cprint("[!!]Warning: Your choice is not valid.", "yellow")
        choose_headings(headings)
    return choice - 1


def get_number_of_records(df):
    """
    Get the number of records in a dataframe
    """
    return len(df)


def choose_number_of_records():
    """
    Choose how many records should be in one document
    """
    try:
        choice = int(input("How many records should be in one file?"))
    except ValueError:
        cprint("[!!]Warning: Kindly enter a digit.", "yellow")
        choose_number_of_records()
    return choice


def make_new_directory(file_path):
    """
    Make a new directory
    """
    n_path_folder = Path(file_path + "_files")
    n_path_folder.mkdir(parents=True, exist_ok=True)
    return n_path_folder


def determine_name_of_file(file_path, value, new_folder):
    """
    Determine name of file being written.
    """
    if(isinstance(value, str)):
        pass
    else:
        value = str(value)
    doc_name = os.path.basename(file_path).split(".")[0]
    final_doc_name = doc_name + "-_" + value + ".csv"
    final_d_path = new_folder.joinpath(final_doc_name)
    return final_d_path


def write_a_file(data_to_write, file_path, value, n_folder):
    """
    Write one csv.
    """
    final_d_path = determine_name_of_file(file_path, value, n_folder)
    data_to_write.to_csv(final_d_path, encoding="utf-8", index=False)


def write_csvs_from_range(records_per_file, no_of_files, file_path, new_folder, data):
    """
    Write csvs from a range of data.
    """
    first_index = 0
    last_index = records_per_file
    for i in range(no_of_files):
        data_to_write = data[first_index:last_index]
        write_a_file(data_to_write, file_path, i, new_folder)
        first_index = last_index
        last_index = last_index + records_per_file


def write_csvs_from_coloumn(unique_values, file_path, col_name, new_folder, data):
    """
    Write csvs based on the coloumn chosen.
    """
    for i in unique_values:
        if(not(pd.isnull(i))):
            final_data = data.loc[data[col_name] == i]
            write_a_file(final_data, file_path, i, new_folder)


def print_out_success_message(new_path):
    """
    Print success message
    """
    cprint("\n[!] Successful!", "green")
    cprint("[!] Check out " + os.path.abspath(new_path) +
           " for your files.\n", "green")


def split_to_csvs_number(file_path):
    """
    Write csvs based on number of records per file specified
    """
    data = read_doc(file_path)
    new_path_folder = make_new_directory(file_path)
    length_of_doc = get_number_of_records(data)
    cprint("[!]Info: The document has " +
           str(length_of_doc) + " records.\n", "green")
    records_per_file = choose_number_of_records()
    if(records_per_file >= length_of_doc):
        cprint(
            "[!!!]Error: You entered a number larger than the number of records.", "red")
        split_to_csvs_number(file_path)
    number_of_final_files = length_of_doc // records_per_file
    extra_records = length_of_doc % records_per_file
    if (extra_records == 0):
        write_csvs_from_range(
            records_per_file, number_of_final_files, file_path, new_path_folder, data)
    else:
        number_of_final_files = number_of_final_files + 1
        write_csvs_from_range(
            records_per_file, number_of_final_files, file_path, new_path_folder, data)
        len_doc = length_of_doc - \
            (number_of_final_files - 1) * records_per_file
        cprint("[!]Info: The last file has " +
               str(len_doc) + " records.", "green")
    print_out_success_message(new_path_folder)


def split_to_csvs(file_path):
    """
    Split the document to many csvs (based on coloumns)
    """
    data = read_doc(file_path)
    headings = get_headings(data)
    choice = choose_headings(headings)
    new_path_folder = make_new_directory(file_path)
    col_name = headings[choice]
    unique_values = set(data[col_name])
    write_csvs_from_coloumn(unique_values, file_path,
                            col_name, new_path_folder, data)
    print_out_success_message(new_path_folder)


def main():
    choice = 0
    choices = [1, 2]
    if(len(sys.argv) >= 2):
        for file in sys.argv[1:]:
            cprint("\n[!] Info: Working with file: " +
                   str(os.path.basename(file)) + "\n", "green")
            cprint("How do wish to split the file: ", "green")
            try:
                choice = int(
                    input("1.Through coloumns.\n2.Through number of records.\nEnter choice: "))
            except ValueError:
                cprint("[!!]Warning: You didn\'t enter a digit.", "red")
                main()
            if choice in choices:
                if (choice == 1):
                    try:
                        split_to_csvs(os.path.abspath(file))
                    except FileNotFoundError:
                        cprint("[!!!]Error: \' " + str(os.path.abspath(file)) +
                               " \'" + " doesn\'t seem to exist.", "red")
                elif(choice == 2):
                    try:
                        split_to_csvs_number(os.path.abspath(file))
                    except FileNotFoundError:
                        cprint("[!!!]Error: \' " + str(os.path.abspath(file)) +
                               " \'" + " doesn\'t seem to exist.", "red")
            else:
                cprint("[!!]Warning: You didn't choose a valid option:", "red")
                main()


if __name__ == "__main__":
    main()
