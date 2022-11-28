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
  - ;p;locf
I'll use `pytermgui` as the front end.  

## To-do:
- Get the GUI woeking
- Made a way to modify the database