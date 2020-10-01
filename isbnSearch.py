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



def make_window(isbn):
    layout_NewWindow = [
        [sg.Text('ISBN: '), sg.Text(isbn)],
        [sg.Text('Enter Quantity', size=(15, 1)), sg.InputText(key='-QUAN-')],
        [sg.Text('Enter Condition', size=(15, 1)), sg.Button('New'), sg.Button('Like New'), sg.Button('Rebind')],
        [sg.Text('Enter Pallet Number', size=(15, 1)), sg.InputText('PALLET ', key='-PALLET-')],
        [sg.Text('Enter Lot Number', size=(15, 1)), sg.InputText('LOT ', key='-LOT-')],
        [sg.Submit(), sg.Button('Back'), sg.Button('Display Inventory'), sg.Exit()] ]
    return sg.Window('Inventory Details', layout_NewWindow)

def make_init_window():
    layout_new_init = [
        [sg.Text('Enter ISBN', size=(15, 1)), sg.InputText(key='-ISBN-')],
        [sg.Button("Continue"), sg.Button('Display Inventory')] ]
    return sg.Window('Enter ISBN', layout_new_init)

def make_multi_window():
    layout_multi = [
        [sg.Text('ISBN Already exists in CSV File')],
        [sg.Text('Would you like to add it as a new entry or edit existing instance?')],
        [sg.Button('Add New Entry'), sg.Button('Edit Existing Entry'), sg.Button('Display Inventory')],
        [sg.Exit()] ]
    return sg.Window('MultiTest', layout_multi)

def enterISBN():
    isbnEntered = False
    initWindow = make_init_window()
    while True:
        initEvent, initValues = initWindow.read()

        while not isbnEntered:
            if initEvent == sg.WIN_CLOSED:
                isbn = 'Exit'
                initWindow.close()
                return isbn
            if initEvent == 'Display Inventory':
                display_CSV()
                break
            if initEvent == 'Continue':
                isbn = initValues['-ISBN-']
                if isbn == '':
                    sg.Popup('Please Enter an ISBN')
                    break
                else:
                    initWindow.close()
                    return isbn

def display_CSV():
    sg.set_options(auto_size_buttons=True)
    filename = 'test.csv'
    data = []
    header_list = []

    try:
        df = pd.read_csv(filename, sep=',', engine='python', header=None)
        header_list = df.iloc[0].tolist()
        data = df[1:].values.tolist()
    except:
        sg.popup_error('Error Reading File')
        return

    displayLayout = [
        [sg.Table(values=data, headings=header_list, display_row_numbers=True, auto_size_columns=False, num_rows=min(25, len(data)))]
    ]
    displayWindow = sg.Window('Table', displayLayout, grab_anywhere=False)
    disEvent, disValues = displayWindow.read()
    displayWindow.close()

initialLayout = [
    [sg.Text('Enter ISBN', size=(15,1)), sg.InputText(key='-ISBN-')],
    [sg.Button("Continue")]]

layoutWin2 = [
    [sg.Text('ISBN Already exists in CSV File')],
    [sg.Text('Would you like to add it as a new entry or edit existing instance?')],
    [sg.Button('Add New Entry'), sg.Button('Edit Existing Entry')],
    [sg.Exit()] ]

windowMultInst_active = False # Second window for checking for multiple instances of an entered ISBN
condition = ' '
isbn = enterISBN()
window = make_window(isbn)
while True:  # Loop for window to remain open
    isbnList = []
    if isbn == 'Exit':
        break


    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):  # same as event == "Exit" or event == sg.WIN_CLOSED:
        window.close()
        break

    if event == 'Back':
        window.close()
        isbn = enterISBN()

    if event == 'Display Inventory':
        display_CSV()

    # If else statements for the condition buttons
    # Button colors changes based off of which condition is selected
    if event == 'New':
        condition = 'New'
        window[event].update(button_color=('white','black'))
        window['Rebind'].update(button_color=('white', 'dark blue'))
        window['Like New'].update(button_color=('white', 'dark blue'))
    if event == 'Like New':
        condition = 'Like New'
        window[event].update(button_color=('white', 'black'))
        window['Rebind'].update(button_color=('white', 'dark blue'))
        window['New'].update(button_color=('white', 'dark blue'))
    if event == 'Rebind':
        condition = 'Rebind'
        window[event].update(button_color=('white', 'black'))
        window['Like New'].update(button_color=('white', 'dark blue'))
        window['New'].update(button_color=('white', 'dark blue'))


    if event == 'Submit':
        pallet = values['-PALLET-']
        lot = values['-LOT-']
        quantity = values['-QUAN-']

        # If nothing is entered in for the pallet or lot number, set the value to a dash
        if pallet == 'PALLET ':
            pallet = '-'
        if lot == 'LOT ':
            lot = '-'

        if not isbnlib.notisbn(isbn, level='strict'): #Verify the ISBN is valid
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
                window.close()
                windowMultInst = make_multi_window()
                while True:
                    event2, values2 = windowMultInst.Read()
                    if event2 == 'Add New Entry':
                        toCSVFile('test.csv', isbnList)
                        windowMultInst.Close()
                        windowMultInst_active = False
                        window = make_window(isbn)
                        condition = ' '
                        break
                    #if event2 == 'Edit Existing Entry':

                    if event2 == 'Display Inventory':
                        display_CSV()

                    if event2 == sg.WIN_CLOSED or event2 == 'Exit':
                        windowMultInst.Close()
                        windowMultInst_active = False
                        window = make_window(isbn)
                        condition = ' '
                        break
            else:
                toCSVFile('test.csv', isbnList) #Convert into the CSV File
                window.close()
                window = make_window(isbn)
                condition = ' '
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
