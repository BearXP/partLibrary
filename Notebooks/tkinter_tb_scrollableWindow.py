# https://pythonguides.com/python-tkinter-table-tutorial/#Python_Tkinter_Table_with_Scrollbar

import tkinter as tk
from  tkinter import ttk


ws  = tk.Tk()
ws.title('Equipment Library')
ws.geometry('640x480')
bgColour = '#292F36'
headerColour = "#4ECDC4"
textColour = "#F7FFF7"
ws['bg'] = bgColour
ttk.Style().configure("Treeview", background=bgColour, 
                    foreground=textColour, fieldbackground=bgColour)
window_frame = tk.Frame(ws, background=bgColour)
window_frame.pack()

# Header
l1 = tk.Label(window_frame, text="Scan your card to log in", background=headerColour, foreground=textColour, width="100", height="2", font='Helvetica 14 bold')
l1.pack()

# TextBox Creation
def callback(event):
    global sv
    print(sv.get())
    return
sv = tk.StringVar()
# sv.trace("w", lambda name, index, mode, sv=sv:callback(sv))
e = tk.Entry(window_frame, textvariable=sv)
e.bind("<Enter>",  callback)
e.pack()

#scrollbar
scroller = tk.Scrollbar(window_frame,orient='vertical')
scroller.pack(side=tk.RIGHT, fill=tk.Y)
table = ttk.Treeview(window_frame,yscrollcommand=scroller.set)
table.pack()
scroller.config(command=table.yview)

#define our column
cols = {
    "player_id" : "Id",
    "player_name" : "Name",
    "player_Rank" : "Rank",
    "player_states" : "State",
    "player_city" : "City"
}
table['columns'] = tuple(cols.keys())

# format our columns & headers
table.column("#0", width=0,  stretch=tk.NO)
table.heading("#0",text="",anchor=tk.CENTER)
for ref, text in cols.items():
    table.column(ref,anchor=tk.CENTER, width=80)
    print(ref)
    table.heading(ref,text=text,anchor=tk.CENTER)

#add data 
table.insert(parent='',index='end',iid=0,text='',values=('1','Ninja','101','Oklahoma', 'Moore'))
table.insert(parent='',index='end',iid=1,text='',values=('2','Ranger','102','Wisconsin', 'Green Bay'))
table.insert(parent='',index='end',iid=2,text='',values=('3','Deamon','103', 'California', 'Placentia'))
table.insert(parent='',index='end',iid=3,text='',values=('4','Dragon','104','New York' , 'White Plains'))
table.insert(parent='',index='end',iid=4,text='',values=('5','CrissCross','105','California', 'San Diego'))
table.insert(parent='',index='end',iid=5,text='',values=('6','ZaqueriBlack','106','Wisconsin' , 'TONY'))
table.insert(parent='',index='end',iid=6,text='',values=('7','RayRizzo','107','Colorado' , 'Denver'))
table.insert(parent='',index='end',iid=7,text='',values=('8','Byun','108','Pennsylvania' , 'ORVISTON'))
table.insert(parent='',index='end',iid=8,text='',values=('9','Trink','109','Ohio' , 'Cleveland'))
table.insert(parent='',index='end',iid=9,text='',values=('10','Twitch','110','Georgia' , 'Duluth'))
table.insert(parent='',index='end',iid=10,text='',values=('11','Animus','111', 'Connecticut' , 'Hartford'))
table.pack()


ws.mainloop()