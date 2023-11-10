import tkinter as tk
import speech_recognition as sr
import smtplib
import pyttsx3
import threading

def main():

    # Create a window
    window = tk.Tk()
    window.title("VISIONLESS EMAIL FOR VISUALLY IMPAIRED USERS")

    w=600
    h=240

    ww=window.winfo_screenwidth()
    wh=window.winfo_screenheight()

    x=(ww/2)-(w/2)
    y=(wh/2)-(h/2)

    window.geometry('%dx%d+%d+%d'%(w,h,x,y))
    window.resizable(0,0)
    window.resizable(False,False)

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
                #for i in range(1000*60):
                audio2 = r.listen(source2)
                # Using google to recognize audio
                text = r.recognize_google(audio2)
                text = text.lower()
                return text

        except sr.RequestError as e:
            SpeakText('Could not request results from Google Speech Recognition service')
        
        except sr.UnknownValueError:
            SpeakText('Sorry, I didn\'t understand that. Please repeat again.')
            return None
            
            
    def send_email():
        sender_email = "your email address"
        sender_password = "your password"
        recipient_email = recipient_email_entry.get()
        subject = subject_entry.get()
        body = body_entry.get('1.0', tk.END)
        message = f"Subject: {subject}\n\n{body}"
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message)
            SpeakText("mail sent successfully. double tap space bar to exit.")

        except:
            SpeakText("failed to send mail. double tap space bar to exit.")
            
        finally:
            server.quit()
      

    #asking user inputs
    def toaddress():
        SpeakText(r"Enter receipent's email address")
        while(True):
            txt=response()
            if txt==None:
                continue
            break
        txt=txt+"@gmail.com"
        txt=txt.replace(' ','')
        recipient_email_entry.insert('end',txt)
        SpeakText('You Said '+txt)
        SpeakText("Do you want to continue or change the recipients email address. say continue or change")
        while(True):
            ans=response()
            if ans=='continue' or ans=='Continue':
                sub()
                break
            elif ans=='change' or ans=='Change':
                txt=''
                recipient_email_entry.delete(first=0,last='end')
                toaddress()
                break
            elif ans==None:
                continue
            else:
                SpeakText('Sorry i didn\'t understand that. please repeat again or double tap space bar to exit. ')
                continue


    def sub():
        SpeakText('enter subject.')
        while(True):
            txt=response()
            if txt==None:
                continue
            break
        subject_entry.insert('end',txt)
        SpeakText('You Said '+txt)
        SpeakText("Do you want to continue or change the Subject. say continue or change")
        while(True):
            ans=response()
            if ans=='continue' or ans=='Continue':
                body()
                break
            elif ans=='change' or ans=='Change':
                txt=''
                subject_entry.delete(first=0,last='end')
                sub()
                break
            elif ans==None:
                continue
            else:
                SpeakText('Sorry i didn\'t understand that. please repeat again or double tap space bar to exit. ')
                continue

    def body():
        SpeakText('enter body.')
        while(True):
            txt=response()
            if txt==None:
                continue
            break
        body_entry.insert('end',txt)
        SpeakText('You Said '+txt)
        SpeakText("Do you want to continue or change the body. say continue or change")
        while(True):
            ans=response()
            if ans=='continue' or ans=='Continue':
                sndcmd()
                break
            elif ans=='change' or ans=='Change':
                txt=''
                body_entry.delete('1.0',tk.END)
                body()
                break
            elif ans==None:
                continue
            else:
                SpeakText('Sorry i didn\'t understand that. please repeat again or double tap space bar to exit. ')
                continue

    def sndcmd():
        SpeakText('say the command send mail to send the email.')
        while(True):
            txt=response()
            if txt==None:
                continue
            break
        txt.lower()
        if txt=='send email' or txt=='send' or txt=="send me" or txt=="send send send" or txt=="send send":
            send_email()
        else:
            SpeakText('mail not sent. double tap space bar to exit.')

    #different thread processes
    def delay2():
        threading.Thread(target=toaddress).start()
       
     # Create labels
    recipient_email_label = tk.Label(window, text="Recipient Email Address:")
    recipient_email_label.grid(row=0, column=0)
    subject_label = tk.Label(window, text="Subject:")
    subject_label.grid(row=1, column=0)
    body_label = tk.Label(window, text="Body:")
    body_label.grid(row=2, column=0)

     # Create entry fields
    recipient_email_entry = tk.Entry(window,width=40)
    recipient_email_entry.grid(row=0, column=1)
    subject_entry = tk.Entry(window,width=40)
    subject_entry.grid(row=1, column=1)
    body_entry = tk.Text(window, height=10, width=50)
    body_entry.grid(row=2, column=1)

    # Create buttons
    send_button = tk.Button(window, text="Send", command=send_email)
    send_button.grid(row=3, column=1)

    #time gaps between choices                  

    window.after(5000,lambda:delay2())  #where 1000=1 sec

    # Start the window
    window.mainloop()

if __name__=="__main__":
    main()