import glob
import PyPDF2

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


# Converts and writes pdfs into txts
# Saves pages for pdf A-S in respective folders
def pdfPageConvertTxt(pdf_files, output):
    for element in pdf_files:
        letter = getPDFLetter(element)
        with open(element, 'rb') as f:
            doc = PyPDF2.PdfFileReader(f)
            #save the extracted data from pdf to a txt file
            for page in range(0, doc.numPages):
                pageObj = doc.getPage(page)
                txt = pageObj.extractText()

                fname = PATH + output + '/part' + letter + '/' + str(page+1) + '.txt'
                with open(fname, 'w') as f: # write file
                    print(txt, file=f)
        
        print("Done", letter)

def pdfWholeConvertTxt(pdf_files, output):
    for element in pdf_files:
        fname = element.split('/').pop().split('.')[0]
        with open(element, 'rb') as f:
            doc = PyPDF2.PdfFileReader(f)
            all_txt = ''
            #save the extracted data from pdf to a txt file
            for page in range(0, doc.numPages):
                pageObj = doc.getPage(page)
                txt = pageObj.extractText()
                all_txt = all_txt + txt
            
            fname = PATH + output + '/' + fname + '.txt'
            with open(fname, 'w') as f: # write file
                print(all_txt, file=f)
                
        print("Done", fname)


def main(pdf_path, output, flag):
    # Get all the pdf files from the specified folder
    ALL_PATHS = combinePaths(pdf_path)
    pdf_files = [f for f in glob.glob(ALL_PATHS + '/*.pdf')]

    if(flag.lower() == 'y'):
        pdfPageConvertTxt(pdf_files, output)
    else:
        pdfWholeConvertTxt(pdf_files, output)


if __name__ == "__main__":
    # Specify paths and whether or not to split into pages
    main('7. Unique comments with Attachments/Attachments', 
    'EPACommentsLocations/uniqueAttachmentsTxt',
    'n')
