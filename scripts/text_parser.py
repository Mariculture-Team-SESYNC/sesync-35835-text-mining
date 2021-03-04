import re
import pandas as pd 

PATH = '/research-home/agarcia/textmining_35835/data/'

# Define columns (sections in the articles)
COLS = ['Title', 'Publication info', 'Abstract', 'Links', 'Full text',
       'Subject', 'Location', 'Company / organization:',
       'Publication title', 'Publication year', 'Publication date',
       'Publisher', 'Place of publication', 'Country of publication',
       'Publication subject', 'Source type', 'Language of publication', 
        'Document type', 'ProQuest document ID', 'Document URL', 'Copyright',
       'Last updated', 'Database']

# Read text file
def read_file(path, name):
    with open(path + name, 'r') as file:
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
    result = re.search(f'{start}: \s*(.*?)\s*{end}', article)
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
            lst.append(f'{c} does not exit in article!')
    return lst


def main():
    # read txt file
    data = read_file(PATH, 'ProQuestDocuments.txt')
    
    # Get articles
    articles = get_articles(data)

    # Get all articles split into sections
    main = [split_article(a, COLS) for a in articles]

    # now we have all the split articles in a list
    # Create a dataframe where each row represents an article
    # and each columns represents a sectoin in the article
    df = pd.DataFrame(main, columns=COLS)

    df.to_csv(PATH + "parsed_txt.csv")

if __name__ == "__main__":
    main()