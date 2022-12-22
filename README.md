# Part Library

## Background
I wanted to make a very simple tool to keep track of which user has borrowed which tool.  
There's a better tool incoming, but for the short term I thought I could cobble together something in a couple of hours which could:
 1. Read the user / tool ID using a handheld barcode scanner (in keyboard mode)
 2. Use a CSV file as the database (for ease of setup)
 3. Present a simple GUI which doesn't require much thought
 
## Method:
I'll use `logZero` to keep audit logs  
I'll use `pandas` to manage the csv database
   - Why csv? Unlike sqlite it's easy to edit using a notepad, and unlike toml or json it's obvious when data is missing.

I'll use ~~`pytermgui`~~ ~~`textual`~~ `tkinter` as the front end. 
   - I started with pytermgui, it seems like a really nice library, but it doesn't seem to play nice with Windows for me.
   - While textual was beautiful for Windows 10 onwards, it didn't render correctly on the Windows 7 PC.

## To-do / Status:
Given that the plan was to *cobble together something in a couple of hours*, I would say that the outstanding features are overkill for the time being. I might want to organise the email reminders though...

I'll let Thomas add the rest.

- [x] Made a way to modify the database
- [X] Get the GUI working
    - [X] Make a 'scan card to log in' page
    - [X] Make a 'scan parts to borrow them, scan card to log out' page, with parts list of borrowed parts.
    - [X] Make 'scan to log in' page show all the parts and their status
- [x] Generate history logs
- [x] Add all the users to the database
- [ ] Add all equipment to the database
  - [x] Multimeters
  - [x] Oscilloscopes
  - [x] Power Supplies
  - [x] Signal Generators
  - [ ] Thermal Camera
  - [ ] Rest
- [x] Generate reminder emails about overdue parts.
    - Note: The Win7 PC can **NOT** be connected to the network, so it will probably need to be a think I run manually every morning.
- [x] Highlight rows when they're overdue
  - > https://stackoverflow.com/questions/62657893/ttk-treeview-set-cell-background-color-based-on-cell-value
- [ ] Show return date (1 week from borrowed time).

## How to build
- Have a PC with Python 3.8 installed (See *python-3.8.10.exe* attached)
  - Ensure the environmental variables are setup correctly
- For the first time setup, go to the folder with this README.md in it using command prompt and run the commands:
```bash
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```
- To build run the following commands
```bash
.\venv\Scripts\activate.bat
auto-py-to-exe
```
  - Script Location: Select the app.py file
  - One Directory
  - Windows Based (hide the console)
  - Additional Files:
    - config.toml
    - database.csv
  - CONVERT .PY TO .EXE

And you should be done.

I'll mention that I keep considering running the python file on the PC, rather than generating an executable, but since I can't connect the PC to the network I can't `pip install` the required files.