from cProfile import label
from cgitb import text
from tkinter import *
from turtle import width

window = Tk()
window.title("Mile to Km Converter")
window.config(padx=20,pady=20)

def calculate():
    output['text'] = float(entry.get())*1.609

# miles input
entry = Entry(width=5)
entry.insert(END, string="0")
entry.focus()
entry.grid(column=2,row=1)


# text
km_label = Label(text='Km')
km_label.grid(column=3, row=2)

mile_label = Label(text='Miles')
mile_label.grid(column=3, row=1)

equal_label = Label(text='is equal to')
equal_label.grid(column=1, row=2)

output = Label(text='0')
output.grid(column=2, row=2)

# calculate button
button = Button(text='Calculate',command=calculate)
button.grid(column=2,row=3)




window.mainloop()