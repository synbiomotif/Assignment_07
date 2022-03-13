#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Songli Zhu, 2022-Mar-05, Modify the script by calling functions
# Songli Zhu, 2022-Mar-13, Modify the script to handle structured errors and use binary data to store  
#------------------------------------------#

import pickle
# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    # TODONE add functions for processing here
    """Processing the data from user input"""
    @staticmethod
    def cd_addition():
        """Function to add data from user input to a 2D table (list of dictionaries)
        
        Reads the data from user input and store the data into dictionaries
        save the dictionaries into a list. 

        Args:
            None

        Returns:
            None.
        """
        intID, strTitle, stArtist = IO.cd_info()
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
        lstTbl.append(dicRow)
        IO.show_inventory(lstTbl)
    
    @staticmethod
    def cd_deletion(intIDDel):
        """Function to delete data from user input to a 2D table (list of dictionaries)
        
        Reads the data from user input and search the data from a 2D table (list of dicts) 
        Try matching the user input to the value of each dictionary in a 2D table 
        if found, delete the dictionary from the 2D table 
        otherwise, return error message

        Args:
            intIDDel (int): deletion ID of the CD used to find its match from 
            from a 2D table (list of dictionaries) that holds the data

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
    
    @staticmethod
    def inventory_save():
        """Function to save data from a 2D table (list of dicts) to file, 
        Reads the data from user input and store the data into dictionaries
        save the dictionaries into a list. 

        Args:
            None.
            
        Returns:
            None.
        """          
        FileProcessor.write_file(strFileName,lstTbl)

class FileProcessor:
    """Processing the data to and from dat file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            data (list): 2D data structure (list of dicts) that holds the data during runtime.
        """
        with open(file_name,'rb') as objFile:
            data = pickle.load(objFile)
        return data

    @staticmethod
    def write_file(file_name, table):
        """Function to write data from a 2D table (list of dicts) to file, 
        Reads the data from a 2D table (list of dicts) into a file 
        one dictionary row in table represents one line in the file. 

        Args:
            file_name (string): name of file used to save the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        """  
        # TODONE Add code here
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    # TODONE add I/O functions as needed
    
    @staticmethod
    def cd_info(): 
        """Gets user input for cd information

        Args:
            None.

        Returns:
            intID (int): an interger of the user input for the id of a cd
            strTitle (string): a string of the user input for the title of a cd
            stArtist (string): a string of the user input for the artist of a cd

        """
        flag = 1
        while flag:
            strID = input('Enter ID: ').strip()
            try: 
                intID = int(strID)
                flag = 0                      
            except ValueError:
                print('That is not an integer!')
                print('Please try again!')
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()

        return intID, strTitle, stArtist

# 1. When program starts, read in the currently saved Inventory
try:
    data = FileProcessor.read_file(strFileName, lstTbl)
    for row in data:
        print(row)
except FileNotFoundError:
    print('dat file does not exist!\n')
    print('loading...')
    print('Create a new dat file!\n')
    open(strFileName,'x')
    
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled\n') # add extra \n 
        if strYesNo.lower() == 'yes':
            print('reloading...')
            data = FileProcessor.read_file(strFileName, lstTbl)
            for row in data:
                print(row)
                print()
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TODONE move IO code into function
        # 3.3.2 Add item to the table
        # TODONE move processing code into function
        DataProcessor.cd_addition()
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        flag = 1
        while flag:
            try:
                IDDel = input('Which ID would you like to delete? ').strip()
                intIDDel = int(IDDel)
                flag = 0
            except ValueError:
                print('That is not an integer!')
                print('Please try again!')
        # 3.5.2 search thru table and delete CD
        # TODONE move processing code into function
        DataProcessor.cd_deletion(intIDDel)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODONE move processing code into function
            DataProcessor.inventory_save()
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




