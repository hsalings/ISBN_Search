'''
What the code should do:

Input ISBN
Get info from ISBN and insert into CSV File
  - Remember CSV needs pallet/lot numbers and conditions
Sync with Amazon

'''

import isbnlib  # For searching ISBNs
import pandas as pd  # For the dataframe to convert to .CSV
import PySimpleGUI as sg  # For the GUI

layout = [
    [sg.Text("Testing")],
    [sg.Text('Enter ISBN', size=(15,1)), sg.InputText(key='-ISBN-')],
    #[sg.Submit(), sg.Cancel()],
    [sg.Button("Exit")]]

window = sg.Window("Test", layout)

while True:  # Loop for window to remain open
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):  # same as event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()

sg.Popup(event, values, values['-ISBN-'])

def get_isbn_metadata(isbn, isbnList):
    # Takes the ISBN and appends information from it into an array
    try:
        isbnList.append(isbnlib.meta(str(isbn),
                                     service='wiki'))  # Appends ISBN number, title, author, publisher, year, and language
        isbnList.append(isbnlib.cover(str(isbn)))  # Appends link to cover of book

        return isbnList  # Returns the appended array

    except isbnlib.ISBNLibException:
        # Try different service (Google Books) for searching the ISBN information
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
    # Convert the array into a CSV file format
    df = pd.DataFrame(isbnList)
    return df.to_csv('test.csv', index=False, encoding='utf-8 ')


isbnList = []
isbn = values['-ISBN-']

if not isbnlib.notisbn(isbn, level='strict'):
  if isbnlib.is_isbn10(isbn):
    isbn = isbnlib.to_isbn13(isbn)
  metadataInfo = get_isbn_metadata(isbn, isbnList)
  toCSVFile(isbnList)
  sg.Popup(metadataInfo)
else:
  sg.Popup('Not a Valid ISBN')


'''
#Code For Testing Below

Example 10 digit: 039591082X

isbnList = []
#isbn = 9780618250578
#isbn = input("Test: \n")

metadataInfo = get_isbn_metadata(isbn, isbnList)

#isbn = 9781680450262
#metadataInfo = get_isbn_metadata(isbn, isbnList)

toCSVFile(isbnList)

'''
