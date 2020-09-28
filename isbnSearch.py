import isbnlib
import pandas as pd

def get_isbn_metadata(isbn, isbnList):
  try:
    isbnList.append(isbnlib.meta(str(isbn), service='wiki'))
    isbnList.append(isbnlib.cover(str(isbn)))
    return isbnList

  except isbnlib.ISBNLibException:
  	isbnList.append(isbnlib.meta(str(isbn), service='goob'))
  	isbnList.append(isbnlib.cover(str(isbn)))
  	return isbnList

  else:
  	isbnList.append(isbnlib.meta(str(isbn), service='openl'))
  	isbnList.append(isbnlib.cover(str(isbn)))
  	return isbnList

def toCSVFile(isbnList):
  df = pd.DataFrame(isbnList)
  return df.to_csv('test.csv', index=False, encoding='utf-8 ')

#Code For Testing Below
isbnList = []
isbn = 9780618250578

metadataInfo = get_isbn_metadata(isbn, isbnList)

isbn = 9781680450262

metadataInfo = get_isbn_metadata(isbn, isbnList)

toCSVFile(isbnList)
