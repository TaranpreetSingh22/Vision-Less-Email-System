import imaplib
import email
from tkinter import *
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
import threading
import re
from datetime import datetime, timedelta

def main():
    # Set up the Tkinter GUI
    root = Tk()
    root.title("VISIONLESS EMAIL FOR VISUALLY IMPAIRED USERS")

    w=700
    h=550

    ww=root.winfo_screenwidth()
    wh=root.winfo_screenheight()

    x=(ww/2)-(w/2)
    y=(wh/2)-(h/2)

    root.geometry('%dx%d+%d+%d'%(w,h,x,y))
    root.resizable(0,0)

    lis=[]
    date = datetime.now() - timedelta(days=3)
    date_string = date.strftime('%d-%b-%Y')

    # Set up the IMAP connection
    host = 'imap.gmail.com'
    port = 993
    username = 'your email address'
    password = 'your password'
    mail = imaplib.IMAP4_SSL(host, port)
    mail.login(username, password)
    mail.select('inbox')

    #start_date = datetime.datetime(2023, 4, 19).strftime('%d-%b-%Y')
    #end_date = datetime.datetime(2023, 4, 23).strftime('%d-%b-%Y')

    # Search for email messages
    #typ, data = mail.search(None, 'SENTSINCE {0} ALL'.format(start_date))
    result, data = mail.search(None, f'(SINCE "{date_string}")')
    msg_ids = data[0].split()

    # Create a text widget to display the messages
    text_widget = Text(root,bd=1,relief=SOLID)
    text_widget.pack(expand=YES, fill=BOTH)

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
            #return "Could not request results from Google Speech Recognition service; {0}".format(e)
            SpeakText('Could not request results from Google Speech Recognition service')
        except sr.UnknownValueError:
            #return "Sorry, I didn't understand that."
            SpeakText('Sorry, I didn\'t understand that. Please repeat again.')
            return None
    
    # Loop through the message IDs and add them to the text widget  text
    SpeakText('please wait for a moment. while emails are loadig')
    count=[]
    for msg_id in reversed(msg_ids):
        # Fetch the message data
        typ, msg_data = mail.fetch(msg_id, '(RFC822)')
        count.append(msg_id)
        email_message = email.message_from_bytes(msg_data[0][1])
        text = f"From: {email_message['From']}\n\nTo: {email_message['To']}\n\nSubject: {email_message['Subject']}\n\n"
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                text += soup.get_text().replace('<div class="auto"></div>', '')
                break
        text += '\n\n'
        lis.append(text)
        text_widget.insert(END, text)
        text_widget.insert(END,'-'*87+'\n', text)
    
    def search():
        SpeakText('Whose mail do you want to search?')
        while(True):
            res=response()
            if res==None:
                continue
            else:
                break
        final=re.findall('[a-z]*',res)
        txt=''.join(final)
        print(txt)
        count=0
        #print(''.join(txt))

        mail = imaplib.IMAP4_SSL(host, port)
        mail.login(username, password)
        mail.select('inbox')

       # start_date = datetime.datetime(2023, 4, 22).strftime('%d-%b-%Y')
       # end_date = datetime.datetime(2023, 4, 23).strftime('%d-%b-%Y')

    # Search for email messages
       # typ, data = mail.search(None, 'SENTSINCE {0} SENTBEFORE {1}'.format(start_date, end_date))
       #voice
        result, data = mail.search(None, f'(SINCE "{date_string}")')
        msg_ids = data[0].split()
        items=[]

        for msg_id in reversed(msg_ids):
            typ, msg_data = mail.fetch(msg_id, '(RFC822)')
            email_message = email.message_from_bytes(msg_data[0][1])
            fro=email_message['From'].replace(' ','').lower()
            print(fro)
            if txt in fro:
                items.append(msg_id)

        for i in range(len(items)):
            typ, msg_data = mail.fetch(items[i], '(RFC822)')
            email_message = email.message_from_bytes(msg_data[0][1])
            text = f"From: {email_message['From']}\n\nTo: {email_message['To']}\n\nSubject: {email_message['Subject']}\n\n"
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    soup = BeautifulSoup(html, 'html.parser')
                    text += soup.get_text().replace('<div class="auto"></div>', '')
                    break
            text += '\n\n'
            SpeakText(text)
            count+=1
            SpeakText('Do you want to read next mail of same user? say Yes or no')
            while True:
                ans=response()
                if ans=='yes' or ans=='yesss' or ans=='yess' or ans=='ES' or ans=='ESS' or ans=='SS' or ans=='S':
                    break
                if ans=='no':
                    SpeakText('double tap spacebar to exit')
                    break
                elif ans==None:
                    continue
                else:
                    break
            if ans=='yes' or ans=='yesss' or ans=='yess' or ans=='ES' or ans=='ESS' or ans=='SS' or ans=='S':
                continue
            elif ans=='no':
                break
            else:
                SpeakText('command not found. double tap spacebar to exit.')
                break
        if(count==len(items)):
            SpeakText('sorry, No more messages available of this user. double tap spacebar to exit ') 

    def readmail():
        mail = imaplib.IMAP4_SSL(host, port)
        mail.login(username, password)
        mail.select('inbox')

        result, data = mail.search(None, f'(SINCE "{date_string}")')
        msg_ids = data[0].split()
        items=[]

        for msg_id in reversed(msg_ids):
            items.append(msg_id)
            

        for i in range(len(items)):
            typ, msg_data = mail.fetch(items[i], '(RFC822)')
            email_message = email.message_from_bytes(msg_data[0][1])
            text = f"From: {email_message['From']}\n\nTo: {email_message['To']}\n\nSubject: {email_message['Subject']}\n\n"
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    soup = BeautifulSoup(html, 'html.parser')
                    text += soup.get_text().replace('<div class="auto"></div>', '')
                    break
            text += '\n\n'
            SpeakText(text)

            SpeakText('Do you want to read next mail? say yes or no.')
            while(True):
                res=response()
                if res=='yes' or res=='s':
                    break
                elif res=='no':
                    break
                elif res==None:
                    continue
                else:
                    SpeakText('Command not found. double tap space bar to exit.')
                    break
            if res=='yes' or res=='s':
                    continue
            elif res=='no':
                    SpeakText('Double tap space bar to exit')
                    break
            else:
                break

    def check():
        SpeakText('Do you want to search a particular Email or read the Emails one by one. Say search or reed.')
        while(True):
            res=response()
            if res=='search':
                search()
                break
            elif res=='read' or res=='reed' or res=='red' or res=='reaed':
                readmail()
                break
            elif res==None:
                continue
            else:
                SpeakText('Command not found. doubletap space bar to exit.')
                break
        
    def delay1():
        threading.Thread(target=check).start()


    root.after(5000,lambda:delay1())

# Close the connection
    mail.close()
    mail.logout()


# Start the mainloop to display the Tkinter window
    root.mainloop()

if __name__=='__main__':
    main()