import glob
import pandas as pd
import pip
import PyPDF2

# path to where the comment files are
PATH = '/nfs/mariculture-data/PPA_Data/EPA Public Comment/' 

# Combine all the paths for the folders into one list
# In: list of folder names containing the podf/txt files
# Out: a list of paths
def combine_paths(folders):
    return [PATH + f for f in folders]

# Function to get locations.
# It is assumed that the last line in a file is the location.
# It traverses backwards until a valid line with a possible location is found.
# In: a list of lines 
# Out: location string of a file
def find_location(lst):
    lst.reverse()
    for el in lst:
        if el != '\n' and el != ' ' and el != '':
            return el.rstrip('\n')
            break
        else:
            pass

# Function to write resulst
# In: dictionary and output path
# Out: a csv file for each key in the dictionary containing the location information
def dict_to_df(dict, output):
    for key, value in dict.items():
        df = pd.DataFrame(value, columns=['location', 'flag'])
        try:
            # used for naming results from pdfs
            fname = key.split('/')
            fname = fname[len(fname)-1]
        except:
            # used for naming results from txt folders
            fname = key

        df.to_csv(output + fname + ".csv", index=False)
        print("Check file here:" + output + fname)

# Function to read every page in a pdf and get its location
def get_pdf_page(pdfReader, path):
    locations = []
    # get location from every page
    for i in range(0, pdfReader.numPages):
        # creating a page object 
        pageObj = pdfReader.getPage(i)
        # extracting text from page 
        txt = pageObj.extractText()
        # split by new line 
        txt_list = txt.split("\n")
        loc = find_location(txt_list)
        
        # odd locations
        # Most locatinos have the following format: LL #########, where LL are letters.
        # Some locations do not follow this format. Also not always the location is listed in the last line of the file.
        # beacuse of this, we assume a valid location starts with a letter and ends in a number. If it does not then a message
        # is attached to check this file manually.
        odds = ""
        if not (loc[0].isalpha() and loc[len(loc)-1].isnumeric()):
            odds = "Check: " + path + " , page: " + str(i)
        locations.append([loc, odds])
    
    return locations

# Function to read the pdf file
# Get location for every page
# In: file path
# Out: a list with a location and path. Note: path is empty if locatoin is 'valid'.
def create_pdf_obj(path):
    with open(path, 'rb') as pdf:
        pdfReader = PyPDF2.PdfFileReader(pdf)
        locations = get_pdf_page(pdfReader, path)
    
    return locations

# Functions starts the process to read a pdf file and get the location string for every page
# In: file path
# Out: a list with a location and path. Note: path is empty if locatoin is 'valid'.
def pdf_start(f):
    locations = create_pdf_obj(f)
    return locations

# Main funciton to extract location data from pdf files
# In: list of all the pdf paths, output path
def pdf_main(pdf_files, output):
    # create a dictionary where the key is a path to a pdf
    pdfDict = {key: None for key in pdf_files}

    # get the locations of every page in every pdf file
    # assign locations to dictionary
    for f in pdf_files:
        locations = pdf_start(f)
        pdfDict[f] = locations

    # write each key value pair in the dictionary as a csv file
    dict_to_df(pdfDict, output)

# Read text file
# In: txt file path
# Out: a list where each line in the txt file is an item in the list
def read_file(path):
    with open(path, encoding='cp1252') as file:
        line_list = file.readlines()
        return line_list

# Function starts the process to read a txt file and get the location string
# In: file path
# Out: a list with a location and path. Note: path is empty if locatoin is 'valid'.
def txt_start(f):
    # read txt file
    data = read_file(f)
    
    # get location
    location = find_location(data)
    
    # odd locations
    # Most locatinos have the following format: LL #########, where LL are letters.
    # Some locations do not follow this format. Also not always the location is listed in the last line of the file.
    # beacuse of this, we assume a valid location starts with a letter and ends in a number. If it does not then a message
    # is attached to check this file manually.
    odds = ""
    if not (location[0].isalpha() and location[len(location)-1].isnumeric()):
        odds = "Check: " + f
        
    return [location, odds]

# Main funciton to extract location data from txt files
# In: list of folders with txt files, list of all the txt paths, output path
def txt_main(txt_folders, txt_files, output):
    # Create a distionary to reference the results to each one of the folders
    txtDict = {key: None for key in txt_folders}

    # for every file in each folder get the location using txt_start()
    for i in range(0, len(txt_folders)):
        locationsM = [txt_start(f) for f in txt_files[i]]
        txtDict[txt_folders[i]] = locationsM
    
    # write each key value pair in the dictionary as a csv file
    dict_to_df(txtDict, output)

def main(txt_folders, pdf_folders, output):
    # Get all the txt files from the specified folders
    # 1b requires it own case for some reason
    ALL_PATHS = combine_paths(txt_folders)
    txt_files = []
    for p in ALL_PATHS:
        # For every path get all the txt files, join all txt files in a nested list
        # where each element in the list is a list of txt files in a folder
        tmp_list = []
        if '1b' in p:
            for f in glob.glob(PATH + "*[b]/*.txt"):
                tmp_list.append(f)
        else:
            for f in glob.glob(p + "/*.txt"):
                tmp_list.append(f)
        txt_files.append(tmp_list)

    txt_main(txt_folders, txt_files, output)

    # Get all the pdf files from the specified folders
    ALL_PATHS = combine_paths(pdf_folders)
    pdf_files = [[f for f in glob.glob(p + '/*.pdf')] for p in ALL_PATHS]
    pdf_main(pdf_files[0], output)


if __name__ == "__main__":
    # Specify paths folder where files are located and the output folder to dave results
    main(['1. Mass 1', '1. Mass 1b'], ['2. Mass 2 with attachments - FOTE'], '/nfs/mariculture-data/PPA_Data/EPA Public Comment/EPACommentsLocations/')






