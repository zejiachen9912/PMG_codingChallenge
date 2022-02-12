import sys
from sys import argv
import re
import pandas as pd


def csvCombiner(*files):
    # a regular expression to match the file name
    rexPattern = '[^\\/:*?"<>|\r\n]+$'
    master_file = pd.DataFrame()

    for file in files:
        # get the filename
        file_name = re.search(rexPattern, file).group()

        # read file from arguments passed
        input_file = pd.read_csv(file)
        # additiong the 'filmname' column and store the corresponding file_name
        input_file['filename'] = file_name

        # reformatting
        """
        Scenario 1 - we reformat '\Gingham\" Shorts"' into 'Gingham Shorts'
        Without any further info given, I assumed that this is the only formatting error that we are encountering
        Thus, I am targeting in solving this specific kind of error.
        """

        # we get all the index that contains the wrongly formatted string.
        s = '\Gingham\\" Shorts"'
        idx = input_file['category'][input_file['category'] == s].index

        # replace the string into what we desire
        for i in idx:
            input_file['category'][i] = input_file['category'][i].replace("\"", "").replace("\\","")

            # We can also assign the error value to "Short"
            #file['category'][i] = "Short"

        """
        Scenario 2 - or we can just delete the ill-formated cell if that is what we want to achieve
        """
        #file = file.drop(labels = idx, axie = 0)

        master_file = master_file.append(input_file)



    master_file.to_csv(sys.stdout, index=False)


def main():
    csvCombiner(*argv[1:])


main()
