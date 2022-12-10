# partLibrary

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
I'll use ~~`pytermgui`~~ `textual` as the front end. 
    - I started with pytermgui, it seems like a really nice library, but it doesn't seem to play nice with Windows for me.

## To-do:
[x] Made a way to modify the database
[ ] Get the GUI working
    [ ] Make a 'scan card to log in' page
    [ ] Make a 'scan parts to borrow them, scan card to log out' page, with parts list of borrowed parts.
    [ ] Make 'scan to log in' page show all the parts and their status
