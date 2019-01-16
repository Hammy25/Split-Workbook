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
        cprint("Warning: Kindly enter a digit.", "yellow")
        choose_headings(headings)
    if((not(choice in range(1, len(headings) + 1)))):
        cprint("Warning: Your choice is not valid.", "yellow")
        choose_headings(headings)
    return choice - 1


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
    cprint("\n[!] Successful!", "green")
    cprint("[!] Check out " + os.path.abspath(new_path_folder) +
           " for your files.\n", "green")


def main():
    if(len(sys.argv) >= 2):
        for file in sys.argv[1:]:
            cprint("\n[!] Working with file: " +
                   str(os.path.basename(file)) + "\n", "green")
            try:
                split_to_csvs(os.path.abspath(file))
            except FileNotFoundError:
                cprint("[!!!] Error: \' " + str(os.path.abspath(file)) +
                       " \'" + " doesn\'t seem to exist.", "red")


if __name__ == "__main__":
    main()
