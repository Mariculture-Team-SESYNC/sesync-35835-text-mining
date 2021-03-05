import re
import pandas as pd 

# path to where the txt files are
PATH = '/nfs/mariculture-data/Text_Parser/data/' 

# Define columns (sections in the articles)
COLS = ['Title', 'Publication info', 'Abstract', 'Links', 'Full text',
       'Subject', 'Location', 'Company / organization',
       'Publication title', 'Publication year', 'Publication date',
       'Publisher', 'Place of publication', 'Country of publication',
       'Publication subject', 'Source type', 'Language of publication', 
        'Document type', 'ProQuest document ID', 'Document URL', 'Copyright',
       'Last updated', 'Database']

# Read text file
def read_file(path, name):
    with open(path + '/'+ name, 'r') as file:
        data = file.read().replace('\n', ' ')
        return data

# Parse the articles in the txt file
# Articles are between dotted lines
def get_articles(string): 
    lst = list(string.split("____________________________________________________________"))
    # remove dotted lines 
    lst = list(filter(None, lst))
    # if last item in the list has 'contact us at:' then delete it we don't need it
    if "" in lst[len(lst)-1]:
        del lst[-1]
    
    return lst 


# Using regex get a specified section in an article
def get_section(start, end, article):
    result = re.search(start + ': \s*(.*?)\s*' + end, article)
    return result.group(1)


# Split and article into sections
# A nested list representing the article split into sections is returned
# [['title','full text','Subject'...]]
def split_article(article, cols):
    lst = []
    for c in cols:  
        try:
            sec = get_section(c, '  ', article)
            lst.append(sec)
        except:
            lst.append('Does not exit in article.')
    return lst

# Main function to parse a text file
# Params: path to read/write files, name of the txt file, output file name
# Note: the output file will be a csv
def main(path, input, output):
    # read txt file
    data = read_file(path, input)
    
    # Get articles
    articles = get_articles(data)

    # Get all articles split into sections
    main = [split_article(a, COLS) for a in articles]

    # now we have all the split articles in a list
    # Create a dataframe where each row represents an article
    # and each columns represents a sectoin in the article
    df = pd.DataFrame(main, columns=COLS)

    df.to_csv(path + '/' + output + ".csv")

if __name__ == "__main__":
    # Main function takes in a path to read/write,
    # a name of a txt file to read, and a string name for the output csv file
    main(PATH, "ProQuestDocuments.txt", "ProQuestDocuments_parsed")