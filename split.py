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


def split_to_csvs_number(file_path):
    """
    Write csvs based on number of records per file specified
    """
    data = read_doc(file_path)
    new_path_folder = Path(file_path + "_files")
    new_path_folder.mkdir(parents=True, exist_ok=True)
    length_of_doc = get_number_of_records(data)
    cprint("[!]Info: The document has " +
           str(length_of_doc) + " records.\n", "green")
    records_per_file = choose_number_of_records()
    if(records_per_file >= length_of_doc):
        cprint("[!!!]Error: You entered a number larger than the number of records.", "red")
        split_to_csvs_number(file_path)
    number_of_final_files = length_of_doc // records_per_file
    extra_records = length_of_doc % records_per_file
    if (extra_records == 0):
        first_index = 0
        last_index = records_per_file
        for i in range(number_of_final_files):
            doc_name = os.path.basename(file_path).split(".")[0]
            final_doc_name = doc_name + "-_" + str(i) + ".csv"
            final_d_path = new_path_folder.joinpath(final_doc_name)
            data[first_index:last_index].to_csv(
                final_d_path, encoding="utf-8", index=False)
            first_index = last_index
            last_index = last_index + records_per_file
    else:
        number_of_final_files = number_of_final_files + 1
        print("Number of files: " + str(number_of_final_files))
        first_index = 0
        print("Records per file: " + str(records_per_file))
        last_index = records_per_file
        for i in range(number_of_final_files):
            doc_name = os.path.basename(file_path).split(".")[0]
            final_doc_name = doc_name + "-_" + str(i) + ".csv"
            final_d_path = new_path_folder.joinpath(final_doc_name)
            data[first_index:last_index].to_csv(
                final_d_path, encoding="utf-8", index=False)
            first_index = last_index
            last_index = last_index + records_per_file
        len_doc = length_of_doc - \
            (number_of_final_files - 1) * records_per_file
        cprint("[!]Info: The last file has " +
               str(len_doc) + " records.", "green")
    cprint("\n[!] Successful!", "green")
    cprint("[!] Check out " + os.path.abspath(new_path_folder) +
           " for your files.\n", "green")


def split_to_csvs(file_path):
    """
    Split the document to many csvs.
    """
    data = read_doc(file_path)
    headings = get_headings(data)
    choice = choose_headings(headings)
    new_path_folder = Path(file_path + "_files")
    new_path_folder.mkdir(parents=True, exist_ok=True)
    col_name = headings[choice]
    unique_values = set(data[col_name])
    for i in unique_values:
        if(not(pd.isnull(i))):
            doc_name = os.path.basename(file_path).split(".")[0]
            final_doc_name = doc_name + "-" + str(i) + ".csv"
            final_data = data.loc[data[col_name] == i]
            final_d_path = new_path_folder.joinpath(final_doc_name)
            final_data.to_csv(final_d_path, encoding="utf-8", index=False)
    cprint("\n[!] Info: Successful!", "green")
    cprint("[!] Info: Check out " + os.path.abspath(new_path_folder) +
           " for your files.\n", "green")


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
