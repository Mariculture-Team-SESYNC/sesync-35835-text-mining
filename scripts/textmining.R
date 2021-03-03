library(pdftools)
setwd("/research-home/agarcia/textmining_35835")

PATH = "/research-home/agarcia/textmining_35835/data"

# make a vector of PDF file names
myfiles <- list.files(path = PATH, pattern = "pdf",  full.names = TRUE)

# convert each PDF file that is named in the vector into a text file 
# text file is created in the same directory as the PDFs
lapply(myfiles, function(i) system(paste("pdftotext",paste0('"', i, '"')), 
                                   wait= FALSE))


# make a vector of TXT file names
mytxtfiles <- list.files(path = PATH, pattern = "txt",  full.names = TRUE)

# Extract Full text
# Use regex to extract that part of each txt file
# Assumes that the Full text is always between the words 'Full text: '
# and 'Subject:'
fulltexts <- lapply(mytxtfiles, function(i) {
  j <- paste0(scan(i, what = character()), collapse = " ")
  regmatches(j, gregexpr("(?<=Full text: ).*?(?=Subject:)", j, perl=TRUE))
})

# write full txts as txt files 
lapply(1:length(fulltexts), 
       function(i) write.table(fulltexts[i], file=paste(mytxtfiles[i], "fulltexts", "txt", sep="."), quote = FALSE, row.names = FALSE, col.names = FALSE, eol = " " ))

# Extract Location
# Assumes that location is between country of publication
# and publication subject
locationtexts <- lapply(mytxtfiles, function(i) {
  j <- paste0(scan(i, what = character()), collapse = " ")
  regmatches(j, gregexpr("(?<=Country of publication: ).*?(?=Publication subject:)", j, perl=TRUE))
})

# write location txts as txt files 
lapply(1:length(locationtexts), 
       function(i) write.table(locationtexts[i], file=paste(mytxtfiles[i], "locationtexts", "txt", sep="."), quote = FALSE, row.names = FALSE, col.names = FALSE, eol = " " ))

