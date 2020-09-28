import isbnlib
import pandas as pd

def get_isbn_metadata(isbn, isbnList):
  #Takes the ISBN and appends information from it into an array
  try:
    isbnList.append(isbnlib.meta(str(isbn), service='wiki')) #Appends ISBN number, title, author, publisher, year, and language
    isbnList.append(isbnlib.cover(str(isbn))) #Appends link to cover of book
    return isbnList #Returns the appended array

  except isbnlib.ISBNLibException:
    #Try different service (Google Books) for searching the ISBN information
  	isbnList.append(isbnlib.meta(str(isbn), service='goob'))
  	isbnList.append(isbnlib.cover(str(isbn)))
  	return isbnList

  else:
    # Try different service (OpenL) for searching the ISBN information
  	isbnList.append(isbnlib.meta(str(isbn), service='openl'))
  	isbnList.append(isbnlib.cover(str(isbn)))
  	return isbnList

def toCSVFile(isbnList):
  #Convert the array into a CSV file format
  df = pd.DataFrame(isbnList)
  return df.to_csv('test.csv', index=False, encoding='utf-8 ')

#Code For Testing Below
isbnList = []
isbn = 9780618250578

metadataInfo = get_isbn_metadata(isbn, isbnList)

isbn = 9781680450262

metadataInfo = get_isbn_metadata(isbn, isbnList)

toCSVFile(isbnList)
