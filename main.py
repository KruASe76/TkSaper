from tkinter import *
import random

win=Tk()
win.geometry('630x780')
win.title('Сапёр')
win.resizable(False, False)

btn_dict, colors, taps, stop={}, ['#fffffffff', '#0000ff', '#009900', '#ff0000', '#000077', '#660000', '#cccc00', '#ff7700', '#000000'], 0, False

def tap(event):
    global stop, taps, label
    if event.widget['bg']=='#eeeeee':
        if event.widget['text']=='💣':
            event.widget['fg']='#000000'
            event.widget['bg']='#ff0000'
            stop=True
            label['text']+='\nYou lost :('
            for i in btn_dict.values():
                autotap(i)
        else:
            event.widget['fg']=colors[event.widget['text']]
            event.widget['bg']='#ffffff'
        
        taps+=1
        if taps==90:
            stop=True
            label['text']+='\nYou won! :)'

def autotap(btn): #Это тот же tap(), только входящая переменная - кнопка, а не event
    if btn['text']=='💣':
        btn['fg']='#000000'
    else:
        btn['fg']=colors[btn['text']]
        btn['bg']='#ffffff'

def flag(event):
    global stop
    if event.widget['bg']!='#ff8888' and event.widget['bg']!='#ffffff' and not stop:
        event.widget['bg']='#ff8888'
        event.widget['fg']='#ff8888'
    elif event.widget['bg']=='#ff8888' and not stop:
        event.widget['bg']='#eeeeee'
        event.widget['fg']='#eeeeee'

def time():
    global stop
    text=label['text']
    try:
        num1, num2=int(text[:2]), int(text[3:])
        num2+=1
        if num2==60:
            num1+=1
            num2=0
        if len(str(num1))==1:
            num1='0'+str(num1)
        if len(str(num2))==1:
            num2='0'+str(num2)
    except ValueError:
        pass
    
    if not stop:
        label['text']=str(num1)+':'+str(num2)
        win.after(1000, time)


#Генерация поля
for i in range(10):
    for j in range(10):
        btn=Button(win, width=6, height=3, text=0, font='arial 13', bg='#eeeeee', fg='#eeeeee')
        btn.bind('<Button-1>', tap)
        btn.bind('<Button-3>', flag)
        btn_dict[str(i)+str(j)]=btn

#Заполнение минами
for i in range(10):
    rand=random.randint(0, 99)
    if len(str(rand))==1:
        rand='0'+str(rand)
    else:
        rand=str(rand)

    while btn_dict[rand]['text']=='💣':
        rand=random.randint(0, 99)
        if len(str(rand))==1:
            rand='0'+str(rand)
        else:
            rand=str(rand)
    
    btn_dict[rand]['text']='💣'

#Назначение индекса каждой клетке без бомбы
for i in btn_dict.keys():
    if btn_dict[i]['text']!='💣':
        ii=int(i)
        for delta in [-11, -10, -9, -1, 1, 9, 10, 11]:
            ind=ii+delta
            if len(str(ind))==1:
                ind1='0'+str(ind)
            else:
                ind1=str(ind)
            
            try:
                if ind<0 or (i[1]=='0' and ind1[1]=='9') or (i[1]=='9' and ind1[1]=='0'):
                    raise KeyError
                if btn_dict[ind1]['text']=='💣':
                    btn_dict[i]['text']+=1
            except KeyError:
                pass

label=Label(win, text='00:00', font='arial 24')

for i in btn_dict.keys():
    btn_dict[i].place(x=int(i[0])*63, y=int(i[1])*70+80)

label.pack()
win.after(1000, time)

win.mainloop()
