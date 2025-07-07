from tkinter import *
root = Tk()
root.title("Simple Calculator")

def click(event):
    global scvalue
    text = event.widget.cget("text")
    if text == "=":
        if scvalue.get().isdigit():
            value = int(scvalue.get())
        else:
            try:
                value = round(eval(screen.get()), 4)
            except Exception as e:
                value = "Error"
        scvalue.set(value)
        screen.update()
    elif text == "AC":
        scvalue.set("")
        screen.update()
    elif text == "⌫":
        current = scvalue.get()
        scvalue.set(current[:-1])
    else:
        scvalue.set(scvalue.get() + text)
        screen.update()

f = Frame(root, bg="grey", width="400", height="350",highlightbackground="black", highlightthickness=2, relief=RAISED)
f.pack()
f.pack_propagate(False)

l = ["AC","⌫","%","/",
     "7","8","9","*",
     "4","5","6","-",
     "1","2","3","+",
     "**","0",".","="]
r = 1
c = 0
for i,item in enumerate(l):
    b1 = Button(f, text=item, bg="Orange",width="5", font="Helvetica 30 bold", relief=RAISED, bd=3)
    b1.bind("<Button-1>", click)
    b1.grid(row=r, column=c, padx=1, pady=2)
    c = c+1
    if c>3:
        c = 0
        r = r+1

scvalue = StringVar()
scvalue.set("")
screen = Entry(f, textvariable=scvalue, font="lucida 35 bold", width=21)
screen.grid(row=0, columnspan=4)
screen.bind("<Key>", lambda e:"break")


root.mainloop()
