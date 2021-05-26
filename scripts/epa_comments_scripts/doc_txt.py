import glob
import docx2txt

# path to where the comment files are
PATH = '/nfs/mariculture-data/PPA_Data/EPA Public Comment/' 

# Used to combine paths
def combinePaths(folder):
    return PATH + folder

# Gets the letter from a pdf path
def getPDFLetter(path):
    letter = path.split('/')
    letter = letter.pop()
    letter = letter[5]
    return letter


# Converts and writes docx into txts
def docxPageConvertTxt(docx_files, output):
    for element in docx_files:
        fname = element.split('/').pop().split('.')[0] # get file number
        all_txt = docx2txt.process(element) # convert to txt
        fname = PATH + output + '/' + fname + '.txt'
        with open(fname, 'w') as f: # write file
            print(all_txt, file=f)
            
        print("Done", fname)


def main(pdf_path, output):
    # Get all the docx files from the specified folder
    ALL_PATHS = combinePaths(pdf_path)
    docx_files = [f for f in glob.glob(ALL_PATHS + '/*.docx')]
    docxPageConvertTxt(docx_files, output)


if __name__ == "__main__":
    # Specify paths
    main('7. Unique comments with Attachments/Attachments', 
    'EPACommentsLocations/uniqueAttachmentsTxt')
