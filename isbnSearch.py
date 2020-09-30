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
import csv

# Functions
def tupleData(isbn, data, quan, cond, pallet, lot):
    temp = ()
    tempList = list(temp)
    for value in data.values():
        tempList.append(value)

    tempList.append(isbnlib.to_isbn10(isbn)) # Add ISBN 10
    tempList.append(quan) # Add the quantity of the book
    tempList.append(cond) # Add the condition of the book
    tempList.append(lot) # Add the lot number
    tempList.append(pallet) # Add the pallet number
    tempList.append(isbnlib.cover(isbn))  # Add cover of ISBN

    temp = tuple(tempList)
    return temp

def get_isbn_metadata(isbn):
    # Takes the ISBN and appends information from it into a list
    # isbn.meta() gives the metadata of the ISBN in a dictionary format
    try:
        isbnMeta = isbnlib.meta(str(isbn), service='wiki') # Grabs metadata of ISBN

        return isbnMeta  # Returns dict of the ISBN meta data

    except isbnlib.ISBNLibException:
        # Try different service (Google Books) for searching the ISBN information
        isbnMeta = isbnlib.meta(str(isbn), service='goob')

        return isbnMeta

def toCSVFile(file_name, isbnList):
    # Convert the list into a CSV file format

    df = pd.DataFrame(isbnList)
    df.to_csv(file_name, mode='a', index=False, header=False, encoding='utf-8 ')
    return sg.popup('ISBN has been added to CSV File')

initialLayout = [
    [sg.Text('Enter ISBN', size=(15,1)), sg.InputText(key='-ISBN-')],
    [sg.Button("Continue")]]

initWindow = sg.Window("Test", initialLayout, finalize=True)

def enterISBN():
    while True:
        initEvent, initValues = initWindow.read()

        if initEvent == 'Continue':
            isbn = initValues['-ISBN-']
            return isbn
        if initEvent == sg.WIN_CLOSED:
            break

isbn = enterISBN()
initWindow.Hide()

layout = [
    [sg.Text('ISBN: '), sg.Text(isbn)],
    [sg.Text('Enter Quantity', size=(15,1)), sg.InputText(key='-QUAN-')],
    [sg.Text('Enter Condition', size=(15,1)), sg.Button('New'), sg.Button('Like New'), sg.Button('Rebind')],
    [sg.Text('Enter Pallet Number', size=(15,1)), sg.InputText('PALLET ', key='-PALLET-')],
    [sg.Text('Enter Lot Number', size=(15,1)), sg.InputText('LOT ', key='-LOT-')],
    [sg.Submit(), sg.Button('Back'), sg.Exit()] ]

layoutWin2 = [
    [sg.Text('ISBN Already exists in CSV File')],
    [sg.Text('Would you like to add it as a new entry or edit existing instance?')],
    [sg.Button('Add New Entry'), sg.Button('Edit Existing Entry')],
    [sg.Exit()] ]

window = sg.Window("Test", layout)
windowMultInst_active = False # Second window for checking for multiple instances of an entered ISBN

while True:  # Loop for window to remain open
    isbnList = []
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):  # same as event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == 'Back':
        initWindow.UnHide()
        window.Hide()
        isbn = enterISBN()
        window[isbn].update(isbn)
        initWindow.Hide()
        window.UnHide()

    # If else statements for the condition buttons
    # Button colors changes based off of which condition is selected
    if event == 'New':
        condition = 'New'
        window[event].update(button_color=('white','black'))
        window['Rebind'].update(button_color=('white', 'dark blue'))
        window['Like New'].update(button_color=('white', 'dark blue'))
    elif event == 'Like New':
        condition = 'Like New'
        window[event].update(button_color=('white', 'black'))
        window['Rebind'].update(button_color=('white', 'dark blue'))
        window['New'].update(button_color=('white', 'dark blue'))
    elif event == 'Rebind':
        condition = 'Rebind'
        window[event].update(button_color=('white', 'black'))
        window['Like New'].update(button_color=('white', 'dark blue'))
        window['New'].update(button_color=('white', 'dark blue'))
    else:
        condition = "N/A"

    if event == 'Submit':
        pallet = values['-PALLET-']
        lot = values['-LOT-']
        quantity = values['-QUAN-']

        # If nothing is entered in for the pallet or lot number, set the value to a dash
        if pallet == 'PALLET ':
            pallet = '-'
        if lot == 'LOT ':
            lot = '-'

        if not isbnlib.notisbn(isbn, level='strict'): #Verify the ISB is valid
            metadataInfo = get_isbn_metadata(isbn)
            tupleToList = tupleData(isbn, metadataInfo, quantity, condition, pallet, lot)
            isbnList.append(tupleToList)

            alreadyExist = False # For testing if the ISBN is already in the CSV file
            with open('test.csv', 'rt') as f:
                reader = csv.reader(f, delimiter=',')
                for col in reader:
                    for row in col:
                        if row == isbn:
                            alreadyExist = True

            if alreadyExist:
                windowMultInst_active = True
                window.Hide()
                windowMultInst = sg.Window('Test', layoutWin2)
                while True:
                    event2, values2 = windowMultInst.Read()
                    if event2 == 'Add New Entry':
                        toCSVFile('test.csv', isbnList)
                        windowMultInst.Close()
                        windowMultInst_active = False
                        window.UnHide()
                        break
                    #if event2 == 'Edit Existing Entry':

                    if event2 == sg.WIN_CLOSED or event2 == 'Exit':
                        windowMultInst.Close()
                        windowMultInst_active = False
                        window.UnHide()
                        break
            else:
                toCSVFile('test.csv', isbnList) #Convert into the CSV File
        else:
            sg.Popup('Not a Valid ISBN')

window.close()



'''
  Will rewrite this part later
  else:
    # Try different service (OpenL) for searching the ISBN information
    isbnList.append(isbnlib.meta(str(isbn), service='openl'))
    isbnList.append(isbnlib.cover(str(isbn)))
    return isbnList


#Code For Testing Below
Example 10 digit: 039591082X
isbnList = []
#isbn = 9780618250578

metadataInfo = get_isbn_metadata(isbn, isbnList)
#isbn = 9781680450262
#metadataInfo = get_isbn_metadata(isbn, isbnList)
toCSVFile(isbnList)
'''
