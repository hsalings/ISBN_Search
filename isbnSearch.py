import isbnlib # For searching ISBNs
import pandas as pd # For the dataframe to convert to .CSV
import PySimpleGUI as sg # For the GUI

layout = [
  [sg.Text("Testing")],
  [sg.InputText()],
  [sg.Button("Exit")]]

window = sg.Window("Test", layout)

while True: # Loop for window to remain open
  event, values = window.read()
  if event == "Exit" or event == sg.WIN_CLOSED:
    break

window.close()

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
  '''
  Will rewrite this part later
  else:
    # Try different service (OpenL) for searching the ISBN information
    isbnList.append(isbnlib.meta(str(isbn), service='openl'))
    isbnList.append(isbnlib.cover(str(isbn)))
    return isbnList
  '''

def toCSVFile(isbnList):
  #Convert the array into a CSV file format
  df = pd.DataFrame(isbnList)
  return df.to_csv('test.csv', index=False, encoding='utf-8 ')

'''
#Code For Testing Below

isbnList = []
#isbn = 9780618250578
#isbn = input("Test: \n")

metadataInfo = get_isbn_metadata(isbn, isbnList)

#isbn = 9781680450262
#metadataInfo = get_isbn_metadata(isbn, isbnList)

toCSVFile(isbnList)

'''
