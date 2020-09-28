import isbnlib
import pandas as pd

def get_isbn_metadata(isbn, arr):
  try:
    arr.append(isbnlib.meta(str(isbn), service='wiki'))
    arr.append(isbnlib.cover(str(isbn)))
    return arr

  except isbnlib.ISBNLibException:
  	arr.append(isbnlib.meta(str(isbn), service='goob'))
  	arr.append(isbnlib.cover(str(isbn)))
  	return arr

  else:
  	arr.append(isbnlib.meta(str(isbn), service='openl'))
  	arr.append(isbnlib.cover(str(isbn)))
  	return arr

def toCSVFile(arr):
  df = pd.DataFrame(arr)
  return df.to_csv('test.csv', index=False, encoding='utf-8 ')

#Code For Testing Below
arr = []
isbn = 9780618250578

metadataInfo = get_isbn_metadata(isbn, arr)

isbn = 9781680450262

metadataInfo = get_isbn_metadata(isbn, arr)

toCSVFile(arr)