import smtplib
import getpass
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

#use this command to use .env variables - first install it --- 
# pip install python-dotenv

# password = getpass.getpass()
# print(password)

load_dotenv()

def send_email():
    sender_add = os.getenv("EMAIL_SENDER")
    # password = getpass.getpass()
    password = os.getenv("EMAIL_PASSWORD")
   
    subject = 'Artificial intelligence and machine learning : Automation in Python'
    body = '''
            This is a session on automation in python.
            We are sending an email.
            This is a second trial email.
            Good luck !
            Have a beautiful day ahead!
            '''
            
    try: 
    #server initialization
        server =  smtplib.SMTP('smtp.gmail.com', 587)
        #587 is gmail port for smtp protocol 
        server.starttls()
        server.login(sender_add, password)
    
    #drafting message body 
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_add
        msg['To'] = os.getenv("EMAIL_RECEIVER")
        # recipients = os.getenv("EMAIL_RECEIVER")  for single person
        recipients = ['acjadhav2400@gmail.com', 'aarya.jadhav22@mmit.edu.in']
    #msg.set_param('importance', 'high')
    
        server.sendmail(sender_add, recipients, msg.as_string())
        print("Email sent successfully!")
        
    except Exception as e :
        print("failed")
    
    finally:
        server.quit()
        
        
    
send_email()