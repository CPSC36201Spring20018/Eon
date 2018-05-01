from tkinter import *

window = Tk()
window.title("Test")

backgroundImg = 'sample_gui/space.gif'
upArrowImg = 'sample_gui/up_arrow.gif'
downArrowImg = 'sample_gui/down_arrow.gif'
settingImg = 'sample_gui/gear.png'

currentTemperature = 80
requestedTemperature = 70

img = PhotoImage(file = backgroundImg)
upimg = PhotoImage(file = upArrowImg)
downimg = PhotoImage(file = downArrowImg)
setimg = PhotoImage(file = settingImg)

w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry("%dx%d+0+0" %(w,h))

background = Label(window, image=img)
background.place(x=0,y=0, relwidth=1, relheight=1)
background.image = img


currentTemp = Label(window, font = "Impact 60 bold", fg = "white", text = str(currentTemperature))
currentTemp.place(relx=0.17,rely=0.33)

requestedTemp = Label(window, font = "Impact 40 bold", fg = "white", text = str(requestedTemperature))
requestedTemp.place(relx=0.2,rely=0.7)

settingsButton = Button(window)
settingsButton.config(image=setimg,width=setimg.width(),height=setimg.height())
settingsButton.place(relx=0.2,rely=0.0)

downButton = Button(window)
downButton.config(image=downimg,width=downimg.width(),height=downimg.height())
downButton.place(relx=0.12,rely=0.9)

upButton = Button(window)
upButton.config(image=upimg,width=upimg.width(),height=upimg.height())
upButton.place(relx = 0.32,rely=0.9)

citiesButton = Button(text="cities", fg="black")
citiesButton.place(relx=0.27,rely=0.0)

window.mainloop()

