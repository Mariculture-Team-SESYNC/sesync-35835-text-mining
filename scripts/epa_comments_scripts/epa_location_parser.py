import glob
import pandas as pd
import pip
import re
import PyPDF2

# path to where the comment files are
PATH = '/nfs/mariculture-data/PPA_Data/EPA Public Comment/' 

# Combine all the paths for the folders into one list
# In: list of folder names containing the podf/txt files
# Out: a list of paths
def combine_paths(folders):
    return [PATH + f for f in folders]

# Function check if a location string is valid if it matched the regex expression
# In: text line
# Out: True if location is valid, else false
def check_valid_location(line):
    # Add or remove expression here to check for other cases
    # City, State Abbreviation 9 digit zip code
    city_state_zip_regex = '([A-Z][a-z]+\s?)+,\s[A-Z]{2}\s\d{5}-?\d{4}?'
    # State Abbreviation and 9 digit zip code with dash (#####-####)
    state_dash_9zip_regex = '[A-Z]{2}\s\d{5}-?\d{4}?'
    # State Abbreviation and 9 digit zip code no dash (#########)
    state_noDash_9zip_regex = '[A-Z]{2}\s\d{9}?'
    # State Abbreviation and 5 digit zip code
    state_5zip_regex = '[A-Z]{2}\s\d{5}?'

    # pass any of regular expression
    # and the string in search() method
    if(re.search(city_state_zip_regex, line) or re.search(state_dash_9zip_regex, line)
      or re.search(state_noDash_9zip_regex, line) or re.search(state_5zip_regex, line)):
        return True
    else:
        return False

# Function to valid locations. Uses check_valid_location.
# It traverses backwards until a valid line with a possible location is found.
# In: a list of lines 
# Out: location string of a file, False if location string criteria is not met
def find_location(line_list):
    line_list.reverse()
    for line in line_list:
        # for every line in the list of line check if a line is a valid location
        # break loop once a valid location is found
        if(check_valid_location(line.rstrip())):
            return line.rstrip()
            break
    return False

# Function to find a name
# It traverses a list until a possible name is found. It is assumed that the name is the line above a location
# In: list of lines
# Out: name
def find_name(line_list):
    # Note the location function reversed the list, so no need to reverse the list again. 
    for line in line_list:
        # A name is the line above a location.
        # If the line is not empty and not a location then it is a posibble name
        if(check_valid_location(line.rstrip()) == False and line.rstrip() != ''):
            return line.rstrip()
            break
    return False

# Function to extraact comment text
# In string of pdf page or text file
# Out: text comment
# Assumes commments start with Dear and end with Thank you
def find_text(data):
    try:
        text = re.search(r'Dear\s*(.*?)\s*Thank you', data).group()
    except AttributeError:
        text = re.search(r'Dear\s*(.*?)\s*Thank you', data)

    return text

# Function to write resulst
# In: dictionary and output path
# Out: a csv file for each key in the dictionary containing the location information
def dict_to_df(dict, output):
    for key, value in dict.items():
        df = pd.DataFrame(value, columns=['location', 'flag', 'name', 'comment'])
        try:
            # used for naming results from pdfs
            fname = key.split('/')
            fname = fname[len(fname)-1]
        except:
            # used for naming results from txt folders
            fname = key

        df.to_csv(output + fname + ".csv", index=False)
        print("Check file here:" + output + fname)

# Function to read every page in a pdf and get its location and name
def get_pdf_page(pdfReader, path):
    info = []
    # get location and name from every page
    for i in range(0, pdfReader.numPages):
        # creating a page object 
        pageObj = pdfReader.getPage(i)
        # extracting text from page 
        txt = pageObj.extractText()

        # get text commment 
        txt_comment = find_text(txt)

        # split by new line 
        txt_list = txt.split("\n")
        location = find_location(txt_list)
        
        # odd locations
        # If find_locations() returns false then a location does not meet the criteria specified in check_valid_location()
        # a message is attached to check this file manually
        odds = ""
        if not (location):
            odds = "Check: " + path + " , page: " + str(i)

        # get name
        name = find_name(txt_list)

        info.append([location, odds, name, txt_comment])

    return info

# Function to read the pdf file
# Get location for every page
# In: file path
# Out: a list with a location and path. Note: path is empty if locatoin is 'valid'.
def create_pdf_obj(path):
    with open(path, 'rb') as pdf:
        pdfReader = PyPDF2.PdfFileReader(pdf)
        info = get_pdf_page(pdfReader, path)
    
    return info

# Functions starts the process to read a pdf file and get the location string for every page
# In: file path
# Out: a list with a location and path. Note: path is empty if locatoin is 'valid'.
def pdf_start(f):
    info = create_pdf_obj(f)
    return info

# Main funciton to extract location data from pdf files
# In: list of all the pdf paths, output path
def pdf_main(pdf_files, output):
    # create a dictionary where the key is a path to a pdf
    pdfDict = {key: None for key in pdf_files}

    # get the locations of every page in every pdf file
    # assign locations to dictionary
    for f in pdf_files:
        info = pdf_start(f)
        pdfDict[f] = info

    # write each key value pair in the dictionary as a csv file
    dict_to_df(pdfDict, output)

# Read text file
# In: txt file path
# Out: a list where each line in the txt file is an item in the list
def read_txt_file(path):
    with open(path, encoding='cp1252') as file:
        line_list = file.readlines()
        return line_list

# Read text file as one
# In: path
# Out: sting of text file. New line characters are replaced by a single space.
def read_as_one(path):
    with open(path, encoding='cp1252') as file:
        data = file.read().replace('\n', ' ')
        return data

# Function starts the process to read a txt file and get the location string
# In: file path
# Out: a list with a location and path. Note: path is empty if locatoin is 'valid'.
def txt_start(f):
    # read txt file and get lines
    line_list = read_txt_file(f)

    # read text file as one
    data = read_as_one(f)
    
    # get location
    location = find_location(line_list)
    
    # odd locations
    # If find_locations() returns false then a location does not meet the criteria specified in check_valid_location()
    # a message is attached to check this file manually
    odds = ""
    if not (location):
        odds = "Check: " + f

    # get name
    name = find_name(line_list)
    # get text comment
    txt_comment = find_text(data)
    
        
    return [location, odds, name, txt_comment]

# Main funciton to extract location data from txt files
# In: list of folders with txt files, list of all the txt paths, output path
def txt_main(txt_folders, txt_files, output):
    # Create a distionary to reference the results to each one of the folders
    txtDict = {key: None for key in txt_folders}

    # for every file in each folder get the location using txt_start()
    for i in range(0, len(txt_folders)):
        info = [txt_start(f) for f in txt_files[i]]
        txtDict[txt_folders[i]] = info
    
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





