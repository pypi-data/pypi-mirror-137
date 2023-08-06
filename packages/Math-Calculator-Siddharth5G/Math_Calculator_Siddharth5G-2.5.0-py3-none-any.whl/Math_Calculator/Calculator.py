import sys
from tkinter import *
from tkinter import Button
from tkinter import font
import math

if sys.platform == 'darwin':
   from tkmacosx import Button

def GUI_MathCalculator():
 window = Tk()
 window.title('Math Calculator')
 window.geometry('490x400')
 window.resizable(0, 0)
 var = IntVar()
 menubar = Menu(window)
 Settings = Menu(menubar, tearoff = 0)
 menubar.add_cascade(label = 'Settings', menu = Settings)
 Settings.add_command(label = 'Darkmode', command = lambda: Darkmode() )
 Settings.add_command(label = 'Lightmode', command = lambda: Lightmode() )
 Settings.add_checkbutton(label = 'Resizable', onvalue = 1, offvalue = 0, variable = var, command = lambda: resize())
 Settings.add_command(label = 'Tutorial', command = lambda: Tutorial())

 window.config(menu = menubar)

 def resize():
  if var.get()  == 1:
     window.resizable(1, 1)
     Tk.update
  elif var.get() == 0:
     window.resizable(0, 0)
     Tk.update
 
 def Lightmode():
   entryborder.configure(highlightbackground = '#f0f0ed', background = 'white')
   for i in range(len(key_matrix)):
     for j in range(len(key_matrix[i])):
         
         btn_dict['btn_'+str(key_matrix[i][j])] = b = Button(window, bd = 0, text = str(key_matrix[i][j]), font = myFont, bg = 'white', fg = 'black')
         btn_dict['btn_'+str(key_matrix[i][j])].grid(row = i+2, column = j, padx = 5, pady = 5, ipadx = 5, ipady = 5)
         btn_dict['btn_'+str(key_matrix[i][j])].bind('<Button-1>', Calculate)
   display.configure(fg = 'black', bg = 'white')
   display2.configure(fg = 'black', bg = 'white')
   window.configure(background= '#f0f0ed')

 def Darkmode():
   entryborder.configure(highlightbackground = 'dark grey', background = '#707070')
   for i in range(len(key_matrix)):
     for j in range(len(key_matrix[i])):
         
         btn_dict['btn_'+str(key_matrix[i][j])] = b = Button(window, bd = 0, text = str(key_matrix[i][j]), font = myFont, bg = 'black', fg = 'white', highlightbackground= 'darkgrey')
         btn_dict['btn_'+str(key_matrix[i][j])].grid(row = i+2, column = j, padx = 5, pady = 5, ipadx = 5, ipady = 5)
         btn_dict['btn_'+str(key_matrix[i][j])].bind('<Button-1>', Calculate)
   display.configure(fg = 'white', bg = '#707070')
   display2.configure(fg = 'white', bg = '#707070')
   window.configure(background = 'dark grey')



 def Tutorial():
  global tutorial
  tutorial = Toplevel(window)
  tutorial.geometry('500x600')
  tutorial.resizable(0, 0)
  tutorial.title('Tutorial')
  global menubar
  menubar = Menu(window)
  tut = Label(tutorial, text = 'This is a Math Calculator!', font = ('Arial', 25), fg = 'black', highlightthickness = 0)
  tut.grid(row = 1, column = 1, columnspan = 10, padx = 100)
  tut3 = Label(tutorial, text = 'Functions:', anchor = 'e', justify = 'center', font = ('Arial', 20) )
  tut3.grid(column = 1, row = 3)
  tut2 = Message(tutorial, text = 'Addition              Subtraction         Multiplication            Division            Percentage            Square Root ', font = ('Helvetica', 17), anchor = 'e', justify= 'left')
  tut2.grid(column= 1, row = 4)


 entryborder = Frame(window,highlightthickness = 15, background = 'white')
 entryborder.grid(rowspan = 2, columnspan =10)
 global inp
 inp = StringVar()
 global inp2
 inp2 = StringVar()
 myFont = font.Font(size = 15)
 display2 = Entry(entryborder, text = inp2, width = 40, justify = 'right', font = ('Helvetica', 15), bd = 0, highlightthickness = 0,)
 display2.grid(row = 1, columnspan = 10, padx = 0, pady = 10, ipady = 10, ipadx = 50)
 display = Entry(entryborder, text = inp, width = 40, justify = 'right', font = ('Helvetica', 15), bd = 0, highlightthickness = 0,)
 display.grid(row = 0, columnspan = 10, padx = 0, pady = 10, ipady = 10, ipadx = 50)
 key_matrix = [['AC', u'\u221A', '/', "C"],
               ['7', '8', '9', '*'],
               ['4', '5', '6', '-'],
               ['1', '2', '3', '+'],
               ['%', 0, '.', '=']]
 
 
 
 btn_dict = {}
 
 ans_to_print = 0
 
 def Calculate(event):
     button = event.widget.cget('text')
 
     global key_matrix, inp, ans_to_print

     try:
         if(button == u"\u221A"):
             ans = float(inp.get())**(0.5)
             ans_to_print = str(ans)
             inp2.set(str(ans))

         elif button == 'AC':
             inp.set('')
             inp2.set('')

         elif button == 'p':
              a = StringVar('')
              a = inp.get()
              a.replace('%','/')
              inp.set(a)
              b = inp2.get()*100
              inp2.set(b)
 
         elif button == 'C':
             inp.set(inp.get()[:len(inp.get())-1])

         elif button == '=':
             ans_to_print = str(eval(inp.get()))
             inp2.set(ans_to_print)

         else:
             inp.set(inp.get()+str(button))
       
     except:
            inp.set('Wrong Operation!')
 
 for i in range(len(key_matrix)):
     for j in range(len(key_matrix[i])):
        
         btn_dict['btn_'+str(key_matrix[i][j])] = b = Button(window, bd = 0, text = str(key_matrix[i][j]), font = myFont, bg = 'white', fg = 'black')
         btn_dict['btn_'+str(key_matrix[i][j])].grid(row = i+2, column = j, padx = 5, pady = 5, ipadx = 5, ipady = 5)
         btn_dict['btn_'+str(key_matrix[i][j])].bind('<Button-1>', Calculate)
 
 window.mainloop()
def reset_No(c): 
     b = float(input('Type your second number__'))
     operator = input('Type your operator__')
     if(operator == '+'):
        c = c + b
        print(c)
     if(operator == '-'):
        c = c - b
        print(c)
     if(operator == 'x' or operator == 'X'):
        c = c * b
        print(c)
     if(operator == '/'):
        c = c / b
        print(c)
     if(operator == '*'):
        c = c ** b
        print(c)
     if(operator == '//'):
        c = c // b
        print(c)
     if(operator == '%'):
        c = c % b
        print(c)
     if(operator == 'sqr'):
        c = math.sqrt((c))
        print(c)
     if(operator == 'p'):
        c = (c/b)*100
        print(c)
     contin = input('quit?__')
     if(contin == 'yes'):
        print('quitting...')
        exit()
     elif(contin == 'no'):
       reset = input('Reset calculator?__')
     if reset == 'yes':
        reset_Yes()
     if reset == 'no':
        reset_No(c) 

def reset_Yes():
     print('resetting...')
     a = float(input('Type your first number__'))
     b = float(input('Type your second number__'))
     operator = input('Type your operator__')
     if(operator == '+'):
        c = a + b
        print(c)
     if(operator == '-'):
        c = a - b
        print(c)
     if(operator == 'x' or operator == 'X'):
        c = a * b
        print(c)
     if(operator == '/'):
        c = a / b
        print(c)
     if(operator == '*'):
        c = a ** b
        print(c)
     if(operator == '//'):
        c = a // b
        print(c)
     if(operator == '%'):
        c = a % b
        print(c)
     if(operator == 'sqr'):
        c = math.sqrt((a))
        print(c)
     if(operator == 'p'):
        c = (a/b)*100
        print(c)
  
     contin = input('quit?__')
     if(contin == 'yes'):
        print('quitting...')
        exit()
     elif(contin == 'no'):
        reset = input('Reset calculator?__')
     if reset == 'yes':
        reset_Yes()
     if reset == 'no':
        reset_No(c) 

def Text_MathCalculator():
 a = float(input('Type your first number__'))
 b = float(input('Type your second number__'))
 operator = input('Type your operator__')
 if(operator == '+'):
     c = a + b
     print(c)
 if(operator == '-'):
     c = a - b
     print(c)
 if(operator == 'x' or operator == 'X'):
     c = a * b
     print(c)
 if(operator == '/'):
     c = a / b
     print(c)
 if(operator == '*'):
     c = a ** b
     print(c)
 if(operator == '//'):
     c = a // b
     print(c)
 if(operator == '%'):
     c = a % b
     print(c)
 if(operator == 'sqr'):
     c = math.sqrt((a))
     print(c)
 if(operator == 'p'):
     c = (a/b)*100
     print(c)
             
 contin = input('quit?__')
 if(contin == 'yes'):
      print('quitting...')
      exit()
 elif(contin == 'no'):
        reset = input('Reset calculator?__')
        if reset == 'yes':
           reset_Yes()
        if reset == 'no':
           reset_No(c)
print('Hello! This is a Math Calculator:')
gui = input('Do you want a Graphical User Interaface(GUI) or Text Based User Interface?__ ')
if(gui == 'GUI'):
   print('Starting Graphical User Interface...')
   GUI_MathCalculator()
elif(gui == 'TUI'):
   print('Starting Text Based User Interface...')
   Text_MathCalculator()
else:
   print('Unrecognized Entry, Starting Text Based User Interface...')
   Text_MathCalculator()
