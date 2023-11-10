from tkinter import *
import pyttsx3
import threading
from main import *

win=Tk()
win.title("VISIONLESS EMAIL FOR VISUALLY IMPAIRED USERS")

w=600
h=240

ww=win.winfo_screenwidth()
wh=win.winfo_screenheight()

x=(ww/2)-(w/2)
y=(wh/2)-(h/2)

win.geometry('%dx%d+%d+%d'%(w,h,x,y))
win.resizable(0,0)
win.resizable(False,False)

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    engine=None

def response():
    r = sr.Recognizer()

    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
            #listens for the user's input
            audio2 = r.listen(source2)
            # Using google to recognize audio
            text = r.recognize_google(audio2)
            text = text.lower()
            return text

    except sr.RequestError as e:
        SpeakText("Could not request results from Google Speech Recognition service. Please double tap space bar to exit.")

    except sr.UnknownValueError:
        SpeakText("Sorry, I didn't understand that. Please repeat again or double tap space bar to exit.")
        return None
       
def compose():
    win.destroy()
    import main
    main.main()

def inboxx():
    win.destroy()
    import receive
    receive.main()
    

def choose():
    SpeakText("do you want to compose mail or check inbox.")
    while True:
        txt=response()
        if txt=="compose email" or txt=="compose" or txt=="compose mail" or txt=="compose compose compose" or txt=="compose compose":
            #compose()
            win.after(1000,composebtn.invoke)
            break
        elif txt=="check inbox" or txt=="inbox" or txt=="checkinbox" or txt=="Jack in the Box":
            #inboxx()
            win.after(1000,inbox.invoke)
            break
        elif txt==None:   
            continue
        else:
            SpeakText('Invalid command, please repeat correct command again or double tap space bar to exit.')
            continue

def welcome():
         SpeakText('Welcome to visionless email.')

def delay2():
    threading.Thread(target=choose).start()

def delay1():
        threading.Thread(target=welcome).start()

#choices for user
composebtn=Button(win,text="COMPOSE EMAIL",width=20,height=10,command=compose)
composebtn.grid(row=2,column=2,padx=100,pady=30)
inbox=Button(win,text="INBOX",width=20,height=10,command=inboxx)
inbox.grid(row=2,column=3,padx=10,pady=30)


win.after(1000,lambda:delay1())
win.after(5000,lambda:delay2())

win.mainloop()