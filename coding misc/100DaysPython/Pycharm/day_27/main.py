import tkinter

def button_clicked():
    my_label['text'] = input.get()


window = tkinter.Tk()
window.title("my first gui")
window.minsize(width=500,height=300)
window.config(padx=100,pady=200)

# label 
my_label = tkinter.Label(text="I am a label", font= ("Arial", 24, "bold"))
my_label.grid(column=1,row=1)

#button
button = tkinter.Button(text = 'Click Me', command=button_clicked)
button.grid(column=2,row=2)

#new button
new_button = tkinter.Button(text = 'Click Me')
new_button.grid(column=3,row=1)


# entry
input = tkinter.Entry(width=10)
input.grid(column=4,row=3)





window.mainloop()