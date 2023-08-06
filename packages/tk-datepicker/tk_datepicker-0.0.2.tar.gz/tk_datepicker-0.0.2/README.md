# Calendar for your Tkinter application

<img src="https://img.shields.io/badge/python-3.10-brightgreen"> <img src="https://img.shields.io/badge/Version-0.0.1-informational">

## Installation

    pip3 install tk_datepicker

## Quick start
The Datepicker class from the tk_datepicker module takes 2 arguments: an input class object for displaying the date and any object from the tkinter module that will open the calendar when clicked
```python
from tkinter import Tk, Entry, Button
from tk_datepicker import Datepicker

root = Tk()
root.geometry("600x600")
entry = Entry()
entry.pack()
button = Button(text="Click me!")
button.pack()
dp = Datepicker(entry, button)
root.mainloop()
```
Output:

<img src="https://user-images.githubusercontent.com/62384889/153004057-c65620d3-372d-4012-af92-c1d2b43f39c1.png">

## Calendar appearance settings
You can use the ui_settings method of the Datepicker class object to change the colors
```python
dp = Datepicker(entry, button)
dp.ui_settings(days_bg="#888", days_fg="#FFF", t_days_bg="#FFF", t_days_fg="#FFF", 
               back_month_text="<= Back", next_month_text="Next =>")
```
Output:

<img src="https://user-images.githubusercontent.com/62384889/153005095-4c173491-ef71-475b-b16a-9ed870aabdf3.png">
Full list of customizations:

    • ctrl_btn_bg - Change month button background color
    • ctrl_btn_fg - Change month button foreground color
    • ctrl_lbl_bg - Name of the month background color
    • ctrl_lbl_fg - Name of the month foreground color
    • ctrl_border - Border size for items that are higher
    • back_month_text - Last month button text
    • next_month_text - Next month button text
    • week_days_bg - Names of the days of the week background color
    • week_days_fg - Names of the days of the week foreground color
    • week_border - Names of the days of the week border size
    • days_bg - Days of this month background color
    • days_fg - Days of this month foreground color
    • days_border - Days of this month border size
    • t_days_bg - Days not of this month background color
    • t_days_fg - Days not of this month foreground color
    • t_days_border - Days not of this month border size
    • output_format - Date output format (default "%Y.%m.%d")
   
## Calendar rendering
The calendar is rendered relative to the object it is attached to. The calendar tries to find free space to render in this order:

    1) TOP CENTER
    2) TOP LEFT
    3) TOP RIGHT
    4) BOTTOM CENTER
    5) BOTTOM LEFT
    6) BOTTOM RIGHT
    7) RIGHT CENTER
    8) LEFT CENTER
In case the calendar cannot find a place to render, it will be rendered from x=0, y=0, keep that in mind
