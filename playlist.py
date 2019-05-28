"""
Script to for selecting and opening a web links from a list
loaded from a text file

Author: Julian Ding
"""

import webbrowser
import os

# Directory for preferred browser
BROWSER = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
# Mode for opening links (0 = same tab <seems to be broken for Chrome>, 1 = new window, 2 = new tab)
MODE = 2

# Default directory for the script to scan
IN_DIR = ''

# File extension for input files
EXT = '.txt'
# Delimiter between name and link string in input files
DELIM = '~'
# Symbols with special interpretations in input files
HEADER = '>'
COMMENT = '#'

# Global list of (name, link) tuples to be populated by contents of input files
LINKS = []

def get_files():
    print("Scanning default directory... (Note: this can be changed in the script)")
    directory = IN_DIR
    while not os.path.exists(directory):
        input_string = directory+" is not a valid directory on this machine, please input an alternate directory: "
        directory = input(input_string)
        directory = directory.replace("\\", "/")
    if not directory.endswith("/"):
        directory += "/"
    index = 1 # Keeps track of list index
    files = [f for f in os.listdir(directory) if f.endswith(EXT)]
    for file in files:
        print('Contents of file:', file)
        # Open file for reading
        f = open(directory+file, 'r')
        lines = f.readlines()
        # Process contents of file
        total, inner_total = 0, 0
        for line in lines:
            # Strip newline
            if line.endswith('\n'):
                line = line[:-1]
            # Ignore comments
            if line.startswith(COMMENT):
                continue
            # Print headers
            elif line.startswith(HEADER):
                if total != 0 and inner_total == 0:
                    print('\t\t(Empty)')
                else:
                    print('\t'+line[1:])
                inner_total = 0
            # Process contents of line. Note that lines without DELIM are ignored
            else:
                split_line = line.split(DELIM, 1)
                split_line = [l.strip() for l in split_line]
                if len(split_line) == 2:
                    print('\t\t'+str(index)+'.', split_line[0])
                    LINKS.append((split_line[0], split_line[1]))
                    index += 1
                    total += 1
                    inner_total += 1
                    
        if total != 0 and inner_total == 0:
            print('\t\t(Empty)')
        if total == 0:
            print('\t(Empty)')
        f.close()

def selection_loop():
    while True:
        command = input('\nEnter the index of a link to open: ')
        
        if command == 'exit':
            break
        if not command.isdigit():
            print('"'+command+'"', 'cannot be interpreted as an integer.')
            continue
        
        index = int(command)
        index -= 1 # Zero-based indexing
        webbrowser.get(BROWSER).open(LINKS[index][1], MODE)
        print('Opened link to', LINKS[index][0])

WELCOME_MESSAGE = '''Welcome to an interactive link-opening script!
Written by Julian Ding

Note: enter "exit" at any time to stop the program.
'''
        
if __name__ == '__main__':
    print(WELCOME_MESSAGE)
    get_files()
    selection_loop()
    print('\nExiting program...')
