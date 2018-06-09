import os
import time
import shutil
import Tkinter
import zipfile
import threading
import platform
from Tkinter import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# This definition helps to read data in list format from a space separated data file
def read_DataFile(filepath):
    # Open the data file
    fid = open(filepath, "r+")
    # fid = open("file.txt", "r+")
    # Read the data line wise and store in 2-D list
    data = []
    while True:
        line = fid.readline().strip()
        if line == '':
            break
        else:
            if str(filepath).endswith('.csv'):
                data.append(line.strip().split(','))
            else:
                data.append(line.strip().split())
    # Close opened file
    fid.close()
    # PreProcess the data & covert to float
    dataSet = []
    for row in range(len(data)):
        dataSet.append([])
        for col in range(len(data[row])-1):
            dataSet[row].append(float(data[row][col]))
        dataSet[row].append(int(data[row][-1]))
    # Return dataSet
    return dataSet


# This class helps to display animation in a separate thread while other jobs are done
class AnimationApp(threading.Thread):
    frameNo = 1
    exitFlag = 0
    progress = ''
    def __init__(self,parent,imgFile,delay=0.2):
        self.parent=parent
        self.image=imgFile
        self.interval=delay
        self.animeWin = Toplevel(self.parent)
        self.animeWin.title("Working..")
        self.animeWin.focus_force()
        self.animeWin.geometry("%dx%d+%d+%d" %(self.animeWin.winfo_screenwidth()/2.5,self.animeWin.winfo_screenheight()/2.5,
                                            self.animeWin.winfo_screenwidth()/3.5,self.animeWin.winfo_screenheight()/5))
        self.animeWin.config(bg="white",pady=30)
        self.animeWin.protocol("WM_DELETE_WINDOW", self.callback)
        self.label = Tkinter.Label(self.animeWin)
        self.label.config(bg="white")
        self.textlabel = Tkinter.Label(self.animeWin,font="Verdana 16")
        self.textlabel.config(text="Working on It..",fg="red")
        self.progresslabel = Tkinter.Label(self.animeWin,font="Verdana 12")
        self.progresslabel.config(text=self.progress,fg="red",bg="white")
        threading.Thread.__init__(self)
        self.daemon=True
        self.start()
    def callback(self):
        self.exitFlag = 1
        self.animeWin.quit()
        self.animeWin.destroy()
    def updateProgress(self, progress):
        self.progress = progress
    def updateImage(self, imagefile):
        self.image = imagefile
        self.frameNo = 1
    def run(self):
        while True:
            if self.interval != -1:
                time.sleep(self.interval)
            try:
                img = PhotoImage(file="imgsrc/"+self.image+".gif",format="gif - {}".format(self.frameNo))
                self.label.config(image=img)
                self.label.image = img
                self.label.pack(fill="x")
                self.textlabel.pack(fill="x",pady=(10,0))
                if self.progress != '':
                    self.progresslabel.config(text=self.progress)
                self.progresslabel.pack(fill="x")
                self.animeWin.update()
                self.frameNo += 1
            except:
                self.frameNo=0
            if self.exitFlag:
                break


# This definition helps to read data and find if it is discrete or continuous
def natureOfData(dataSet):
    index = 0
    scale = 0; count = 0
    window = (len(dataSet[2])/5)
    if window <= 5:
        window = len(dataSet[2])-1
    # Transposing dataSet
    dataSet = [list(x) for x in zip(*dataSet[1:])]
    dataSet = dataSet[:-1]  # Removing the column for class
    while index+window <= len(dataSet):
        distinctElements = []
        totElements = 0
        for eachrow in dataSet[index:index+window]:
            # Checking if entire attribute column has 0, FCD will fail
            if set(eachrow) == {0}:
                return 'Discrete'
            for eachel in eachrow:
                if eachel not in distinctElements:
                    distinctElements.append(eachel)
                totElements +=1
        if (len(distinctElements)*100.0)/totElements < 6.0:
            scale += 1
        index += window
    if scale == index/window:
        return 'Discrete'
    return 'Continuous'

# print natureOfData([[0,0],[1,2,1],[1,1,8],[2,2,7]])
def createZipAndSendMail(dirPath, mailToList):
#    print dirPath
#    print mailToList
    dirName = dirPath.split('/')[-2]
#    print dirName
    zipf = zipfile.ZipFile('mRMRStats.zip', mode='w', allowZip64=True,
                           compression=zipfile.ZIP_DEFLATED)
    # zf = zipfile.ZipFile(dirName+'.zip', 'w')
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            # root = root.split('\\')[-1]
            # print os.path.join(root, file)
            zipf.write(os.path.join(root, file),arcname=dirName+'\\'+file)
            # print root+file+''
    zipf.close()
    time.sleep(1)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("mrmrapp.auto@gmail.com", "mrmr12345")

    for email in mailToList:
        msg = MIMEMultipart()
        msg['From'] = "mrmrapp.auto@gmail.com"
        msg['To'] = str(email)
        msg['Subject'] = "mRMR App Run Results"
        body = ("\nHi\n\nThe details for mRMR App run you initiated are as follows.\n\n"
        "  Date               : " + ' '.join(dirName.split('_')[1].split('-')) + "\n"
        "  Time               : " + dirName.split('_')[2] + " Hrs\n"
        "  System Name  : " + platform.node() + "\n"
        "  System Info     : " + platform.system()+" "+platform.release()+"\n\n"
        "The detailed Statistics are also enclosed hereby.Extract the file in your system \n"
        "to view the results.\n\n"
        "Have a great day..!\n\n"
        "**************************************************************************************************************\n"
        "       This is a script generated mail. Please mail to the admin at krprince16@gmail.com    \n"
        "       in case of any queries.\n"
        "**************************************************************************************************************\n")
        msg.attach(MIMEText(body, 'plain'))

        filename = "mRMRStats.zip"
        attachment = open("mRMRStats.zip", "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        text = msg.as_string()
        try:
            server.sendmail("mrmrapp.auto@gmail.com", str(email), text)
        except:
            print "Error sending e-mail for " + email

    server.quit()
        # shutil.rmtree('mRMRStats.zip') # , ignore_errors=True

# createZipAndSendMail('C:/Users/Prince/PycharmProjects/mrmr/outPut/mRMR_17-May-2016_0048/',
#                      ['ritesh.kumar465@gmail. com'])

# shutil.rmtree('mRMRStats')
