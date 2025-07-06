from tkinter import *
import random
root = Tk()
root.title("Game")

n1=0
n2=0
def reset():
    global n1,n2
    n1=0
    n2=0
    l4.config(text=f"your_score = {n1}\ncomputer_score = {n2}", font="Courier 10 ")


def pb(text):
    l1.config(text=text)
    game()

def game():
    lst1 = ["🪨 Rock", "📄 Paper", "✂ Scissor"]
    a = random.choice(lst1)
    root.after(100, lambda: show_result(a))
def show_result(a):
    global n1,n2
    l2.config(text=a)
    current = l1.cget("text")
    if current==a:
        l3.config(text="TIE", fg="grey")
        l4.config(text=f"your_score = {n1}\ncomputer_score = {n2}", font="Courier 10 ")
    elif (current == "🪨 Rock" and a == "📄 Paper") or \
        (current == "✂ Scissor" and a == "🪨 Rock") or \
        (current == "📄 Paper" and a == "✂ Scissor"):
        l3.config(text="YOU LOSE", fg="red")
        n2 = n2 + 1
        l4.config(text=f"your_score = {n1}\ncomputer_score = {n2}", font="Courier 10 ")

    else:
        l3.config(text="YOU WIN", fg="green")
        n1 = n1 + 1
        l4.config(text=f"your_score = {n1}\ncomputer_score = {n2}", font="Courier 10 ")



f = Frame(root, bg="light blue", width="600", height="350",highlightbackground="black", highlightthickness=2, relief=RAISED)
f.pack()
f.pack_propagate(False)

l = Label(f, text="Game", font="Georgia 15 bold", fg="red", bg="light blue")
l.grid(row=0, column=1)
l = Label(f, text="Rock Paper Scissor", font="Georgia 24 bold", fg="red", bg="light blue")
l.grid(row=1, column=1)

b1 = Button(f, text="🪨 Rock", bg="brown", width="10", height="2", font="Arial 11 bold", command=lambda : pb(b1["text"]))
b1.grid(row=6, column=0, padx=10, pady=10)
b2 = Button(f, text="📄 Paper", bg="blue", width="10", height="2", font="Arial 11 bold", command=lambda : pb(b2["text"]))
b2.grid(row=7, column=1, padx=10, pady=10)
b3 = Button(f, text="✂ Scissor", bg="grey", width="10", height="2", font="Arial 11 bold", command=lambda : pb(b3["text"]))
b3.grid(row=6, column=2, padx=10, pady=10)
b4 = Button(f, text="RESET", bg="orange", width="8", height="1", font="Times 7 bold", command=reset)
b4.grid(row=10, column=1)

l1 = Label(f, text="", font=5, bg="light blue")
l1.grid(row=5, column=1)

Label(f, text="---------------------", bg="light blue").grid(row=4, column=1)
Label(f, text="Computer Choice", bg="light blue", font="Arial 12 ").grid(row=2, column=1)
Label(f, text="Your Choice", bg="light blue", font="Arial 12 ").grid(row=6, column=1)
l3 = Label(f, text="", bg="light blue", font=3)
l3.grid(row=8, column=1)

l2 = Label(f, text="", bg="light blue", font=5)
l2.grid(row=3, column=1)

l4 = Label(f, text="", bg="light blue")
l4.grid(row=9, column=1)

root.mainloop()
