import imaplib
import base64
import os
import email
import time

# Variables

path_to_dir = '~/' # Define the local directory where the file will be uploaded

email_user = 'example@gmail.com' # Define your e-mail address 
email_pass = 'examplePass' # Define your password related to your e-mail address

# Script

connect = False
while connect == False: # Try to make connection to the imap servers of gmail
     try:
         mail = imaplib.IMAP4_SSL("imap.gmail.com")
     except:
         print ("Can't connect the internet...") # If exception -> try again
         time.sleep(2)
     else:
         connect = True # If no exception change variable connect to True and go further

print('Connection succesfully stablished ... ')
mail.login(email_user, email_pass) # Login with email and password

while True:
    mail.select('Inbox') # Check all mails in Inbox

    type, data = mail.search(None, 'UnSeen') # Only check mails that are unseen
    mail_ids = data[0]
    id_list = mail_ids.split()

    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
    # converts byte literal to string removing b''
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
    # download attachment
        for part in email_message.walk():
            fileName = part.get_filename() # Take filename of attachment
            if bool(fileName):
                filePath = os.path.join(path_to_dir, fileName) 
                if not os.path.isfile(filePath): # Download attachment to path_to_dir with fileName
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                print('Downloaded attachment of email(s) ... ')
                