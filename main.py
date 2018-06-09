import os
import tkMessageBox
import Tkinter
import time
from Tkinter import *
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename
from mrmr import mrmrFTestPearson, mrmrMutualInformation
from classification import classifyData
from myUtilities import read_DataFile, AnimationApp, natureOfData, createZipAndSendMail


dataSet = []
dataNature = ''
reducedData = []
reducedOptData = []
optReducedData = []
classAccuracy = {}
classAccuracyOpt = {}
saveResults = 'outPut/'
mailToList = []
dateTimeofRun = ''

# These are all the functions for first GUI which imports data and sends for mRmR and/or classification
def browseFiles():
    fpath.set(askopenfilename())

def aboutApp():
    tkMessageBox.showinfo(
            "mRMR App 1.0",
            "    Python        -    2.7.11                                                  \n\n"
            "    Team          -    Ashutosh, Ayesha, Prinon & Prince                       \n\n"
            "    Mentor        -    Prof. Shilpi Bose                                       \n\n"
            "    mRMr by     -    Mutual Information Difference for discrete                  \n"
            "                               F-Test Correlation Difference for continuous    \n\n"
            "   Classifiers    -    Naive Bayes, kNN(k=2), Support Vector Machine               ")


def displayImportedMessage(parent):
    check = Toplevel(parent)
    check.title("Message")
    check.focus_force()
    check.config(bg="white")
    check.geometry("%dx%d+%d+%d" % ((check.winfo_screenwidth() / 2.5), (check.winfo_screenheight() / 2.5),
                                    (check.winfo_screenwidth() / 4), (check.winfo_screenheight() / 4)))
    logo = PhotoImage(file="imgsrc/checkmark.gif")
    checkicon = Label(check, image=logo, bg="white")
    checkicon.pack(fill="x",pady=(10,0))
    typeOfData = Label(check)
    typeOfData.config(text=dataNature+' Data Detected',fg="red",font="verdana 14")
    typeOfData.pack(fill="x",pady=(0,10))
    check.after(2500, lambda: check.quit())
    check.mainloop()
    check.destroy()

def importData():
    path = fpath.get()
    if path == '':
        tkMessageBox.showerror("Alert", " File Path Cannot be empty ")
    else:
        try:
            mrAnime = AnimationApp(firstGui,"work",2.0)
            mrAnime.updateProgress('Reading Data..')
            globals()['dataSet'] = read_DataFile(path)
            globals()['dataNature'] = natureOfData(dataSet)
            mrAnime.callback()
        except:
            tkMessageBox.showerror("Alert", " Error in importing data file ")
            return
        displayImportedMessage(firstGui)
        firstGui.quit()

def closeMainGui():
    firstGui.destroy()
    globals()['keepRunningApp']=0
    exit(0)


# These are the functions for second GUI which take parameters for mRmR and/or classification and launch the job
def togglemrmr():
    if enablemrmr.get() == '1':
        L1.config(state=NORMAL)
        nof.config(state=NORMAL)
        goforOptimal.config(state=NORMAL)
    else:
        L1.config(state=DISABLED)
        nof.config(state=DISABLED)
        goforOptimal.config(state=DISABLED)

def toggleclassify():
    if enableclassify.get() == '1':
        CrData.config(state=NORMAL)
        CfData.config(state=NORMAL)
        L2.config(state=NORMAL)
        sratio.config(state=NORMAL)
    else:
        CrData.config(state=DISABLED)
        CfData.config(state=DISABLED)
        L2.config(state=DISABLED)
        sratio.config(state=DISABLED)

def writeToReadMe(text='', newline = True):
    readMe = open(saveResults + 'README.txt', "a")
    readMe.write(text)
    if newline:
        readMe.write('\n')
    readMe.close()

def RunTheApp():
    # Validate First before proceeding
    if enablemrmr.get()=='1':
        if (nofeatures.get() > int(globals()['dataSet'][0][1])) or (nofeatures.get() < 0):
            tkMessageBox.showerror("Alert"," Features selection is in the range of 0 to %d "
                                   % int(globals()['dataSet'][0][1]))
            return
        if nofeatures.get() == 0 and goforOpt.get() == '0':
            tkMessageBox.showerror("Alert", " mRMR enabled but both fields are empty ")
            return
    if enableclassify.get()=='1':
        if reduDataClassify.get() == '0' and fullDataClassify.get() == '0':
            tkMessageBox.showerror("Alert", " Data Parameters missing in classification ")
            return
        if reduDataClassify.get() == '1' and enablemrmr.get() == '0':
            tkMessageBox.showerror("Alert", " Enable mRMR to use Reduced Data ")
            return
        # if reduDataClassify.get() == '1' and nofeatures.get() == 0:
        #     tkMessageBox.showerror("Alert", " Optimize Data or set Features > 0 for classifying Reduced Data ")
        #     return
        if splitRatio.get()<0.4 or splitRatio.get()>0.8:
            tkMessageBox.showerror("Alert", " Split Ratio has to be in range (0.4-0.8) ")
            return
    optionsGui.destroy()
    optionsGui.master.destroy()
    animeRoot = Tkinter.Tk()
    animeRoot.withdraw()
    animeGui = Toplevel(animeRoot)
    animeGui.withdraw()

    globals()['dateTimeofRun'] = time.strftime("%d-%b-%Y_")+time.strftime("%H%M")
    globals()['saveResults'] += "mRMR_"+dateTimeofRun+"/"
    try:
        os.makedirs('/'.join(saveResults.split('/')[:-1]))
    except:
        print "Error in creating outPut Folder.."
    # Saving the original Data
    origData = open(saveResults + 'OriginalData.csv', 'w')
    for eacr in dataSet:
        for eacc in eacr[:-1]:
            origData.write(str(eacc) + ',')
        origData.write(str(eacr[-1]) + '\n')
    origData.close()
    writeToReadMe("************************************************************************\n")
    writeToReadMe("This is script generated file for mRmRApp 1.0")
    writeToReadMe("System Time : "+str('  '.join(dateTimeofRun.split('_')))+"Hrs")
    writeToReadMe("----- Beginning List of Files -----\n")
    writeToReadMe("Input Data          : "+fpath.get())
    writeToReadMe("Nature of Data      : "+dataNature)
    anime = AnimationApp(animeGui, "gears", 0.2)
    anime.updateProgress("App Run Initiated..")
    if enablemrmr.get() == '1':
        writeToReadMe("mRMR Selected       : Yes")
        writeToReadMe("No. of Features     : " + str(nofeatures.get()))
        if nofeatures.get() > 0:
            anime.updateProgress("Going for Data Reduction..")
            time.sleep(1)
            if dataNature == 'Continuous':
                globals()['reducedData'] = mrmrFTestPearson(dataSet, nofeatures.get(), anime)
                writeToReadMe("Reduced Data(FCD)   : "+"reducedData.csv")
            elif dataNature == 'Discrete':
                globals()['reducedData'] = mrmrMutualInformation(dataSet, nofeatures.get(), anime)
                writeToReadMe("Reduced Data(MID)   : "+"reducedData.csv")
            anime.updateProgress('Saving Reduced Data..')
            redData = open(saveResults+'reducedData.csv', 'w')
            for eacr in reducedData:
                for eacc in eacr[:-1]:
                    redData.write(str(eacc)+',')
                redData.write(str(eacr[-1])+'\n')
            redData.close()
            time.sleep(1)
        if goforOpt.get() == '1':
            writeToReadMe("Optimal Data Reqd   : Yes")
            anime.updateProgress("Going for Optimal Data..")
            time.sleep(1)
            if dataNature == 'Continuous':
                globals()['optReducedData'] = mrmrFTestPearson(dataSet,0,anime)
                writeToReadMe("Optimal Data(FCD)   : " + "optReducedData.csv")
            if dataNature == 'Discrete':
                globals()['optReducedData'] = mrmrMutualInformation(dataSet,0,anime)
                writeToReadMe("Optimal Data(MID)   : " + "optReducedData.csv")
            anime.updateProgress('Saving Optimal DataSet..')
            optData = open(saveResults + 'optReducedData.csv', 'w')
            for eacr in optReducedData:
                for eacc in eacr[:-1]:
                    optData.write(str(eacc) + ',')
                optData.write(str(eacr[-1]) + '\n')
            optData.close()
        else:
            writeToReadMe("Optimal Data Reqd   : No")
        time.sleep(1)
    else:
        writeToReadMe("mRMR Selected       : No")

    if enableclassify.get() == '1':
        writeToReadMe("Classify Selected   : Yes")
        # clAnime = AnimationApp(animeGui, "robot", 0.2)
        # clAnime = mrAnime
        anime.updateImage("robot")
        if fullDataClassify.get() == '1':
            writeToReadMe("Classification Data : Full DataSet")
            anime.updateProgress("Classifying Full DataSet..")
            time.sleep(1)
            globals()['classAccuracy'] = classifyData(dataSet,splitRatio.get())
            writeToReadMe("Classification Stats: " + "class_fullData.txt")
            classStat = open(saveResults + 'class_fullData.txt', 'w')
            anime.updateProgress('Saving Classification Stats..')
            classStat.write("\n****************************************************************\n\n")
            classStat.write("Total Features      : " + str(dataSet[0][1]) + "\n")
            classStat.write("Number of Samples   : " + str(dataSet[0][0]) + "\n")
            classStat.write("Distinct Classes    : " + str(dataSet[0][2]) + "\n")
            classStat.write("Split Ratio         : " + str(splitRatio.get()) + "\n")
            classStat.write("Naive Bayes         : " + str(classAccuracy['nb']) + "\n")
            classStat.write("k-Nearest Neighbour : " + str(classAccuracy['knn']) + "\n")
            classStat.write("Support Vector      : " + str(classAccuracy['svm']) + "\n")
            classStat.write("Hybrid Classifier   : " + str(classAccuracy['hy']) + "\n")
            classStat.write("\n****************************************************************\n")
            classStat.close()
            time.sleep(1)
        if reduDataClassify.get() == '1':
            writeToReadMe("Classification Data : Reduced DataSet")
            if nofeatures.get() > 0:
                anime.updateProgress("Classifying Reduced DataSet..")
                globals()['classAccuracy'] = classifyData(reducedData,splitRatio.get())
                writeToReadMe("Classification Stats: " + "class_reducedData.txt")
                classStat = open(saveResults + 'class_reducedData.txt', 'w')
                anime.updateProgress('Saving Classification Stats..')
                classStat.write("\n****************************************************************\n\n")
                classStat.write("Total Features      : " + str(reducedData[0][1]) + "\n")
                classStat.write("Number of Samples   : " + str(reducedData[0][0]) + "\n")
                classStat.write("Distinct Classes    : " + str(reducedData[0][2]) + "\n")
                classStat.write("Split Ratio         : " + str(splitRatio.get()) + "\n")
                classStat.write("Naive Bayes         : " + str(classAccuracy['nb']) + "\n")
                classStat.write("k-Nearest Neighbour : " + str(classAccuracy['knn']) + "\n")
                classStat.write("Support Vector      : " + str(classAccuracy['svm']) + "\n")
                classStat.write("Hybrid Classifier   : " + str(classAccuracy['hy']) + "\n")
                classStat.write("\n****************************************************************\n")
                classStat.close()
                time.sleep(1)
            if goforOpt.get() == '1':
                anime.updateProgress("Classifying Optimal DataSet..")
                globals()['classAccuracy'] = classifyData(optReducedData, splitRatio.get())
                writeToReadMe("Classification Stats: " + "class_optReducedData.txt")
                classStat = open(saveResults + 'class_optReducedData.txt', 'w')
                anime.updateProgress('Saving Classification Stats..')
                classStat.write("\n****************************************************************\n\n")
                classStat.write("Total Features      : " + str(optReducedData[0][1]) + "\n")
                classStat.write("Number of Samples   : " + str(optReducedData[0][0]) + "\n")
                classStat.write("Distinct Classes    : " + str(optReducedData[0][2]) + "\n")
                classStat.write("Split Ratio         : " + str(splitRatio.get()) + "\n")
                classStat.write("Naive Bayes         : " + str(classAccuracy['nb']) + "\n")
                classStat.write("k-Nearest Neighbour : " + str(classAccuracy['knn']) + "\n")
                classStat.write("Support Vector      : " + str(classAccuracy['svm']) + "\n")
                classStat.write("Hybrid Classifier   : " + str(classAccuracy['hy']) + "\n")
                classStat.write("\n****************************************************************\n")
                classStat.close()
                time.sleep(1)
    else:
        writeToReadMe("Classify Selected   : No")
    anime.callback()
    time.sleep(1)
    writeToReadMe("\nTest Run Completed..\n")
    writeToReadMe("************************************************************************\n")
    animeGui.destroy()
    animeRoot.destroy()
    if len(mailToList) > 0:
        createZipAndSendMail(saveResults, mailToList)


def setOptions():
    def updateSavePath():
        dpath = askdirectory()
        if dpath != '':
            saveDirPath.set(dpath)
            globals()['saveResults'] = saveDirPath.get()+'/'
            print 'saveResults changed to ',saveResults
    def exitSetoptions():
        if enablemail.get() == '1':
            if maillist.get() == '':
                tkMessageBox.showerror("Alert", " MailList cannot be empty when active. ")
                return
            globals()['mailToList'] = maillist.get().strip().split(' ')
        opt.quit()
        opt.destroy()
        optionsGui.deiconify()
    def togglemail():
        if enablemail.get()=='1':
            mailList.config(state=NORMAL)
        elif enablemail.get()=='0':
            mailList.config(state=DISABLED)

    optionsGui.withdraw()
    opt = Toplevel()
    opt.title("Options")
    opt.geometry("%dx%d+%d+%d" % ((opt.winfo_screenwidth()/3), (opt.winfo_screenheight()/4),
                                  (opt.winfo_screenwidth()/4), (opt.winfo_screenheight()/4)))
    opt.resizable(False,False)
    opt.focus_force()
    opt.protocol('WM_DELETE_WINDOW', exitSetoptions)
    opt.config(padx=20, pady=30)
    slabel = LabelFrame(opt, text="Output Folder")
    slabel.config(font="System 10", relief="flat")
    slabel.pack(anchor=NW)
    saveDirPath = StringVar(opt, 'output/')
    saveDir = Entry(slabel, textvariable=saveDirPath)
    saveDir.config(bd=2, width=40, font="Verdana 10", relief="ridge")
    saveDir.pack(anchor=NW, side=LEFT)
    configSaveDir = Button(slabel, text="Config", command=updateSavePath)
    configSaveDir.config(width=10)
    configSaveDir.pack(anchor=NW, side=LEFT, padx=(5,0))
    enablemail = StringVar(opt)
    enableMail = Checkbutton(opt, text="Send Mail", variable=enablemail,
                     anchor=W, font="System 10", command=togglemail)
    enableMail.deselect()
    enableMail.pack(anchor=W)
    maillist = StringVar(opt, 'None')
    mailList = Entry(opt, textvariable=maillist)
    mailList.config(bd=2,width=65, font="Verdana 10",relief="ridge",state=DISABLED)
    mailList.pack(anchor=NW, fill="x")
    okOptions = Button(opt, text="Done", command=exitSetoptions)
    okOptions.config(width=10, bg="#4863A0")
    okOptions.pack(anchor=E, side=BOTTOM)
    opt.mainloop()

def closeGUI2():
    optionsGui.quit()
    optionsGui.destroy()
    optionsGui.master.destroy()


firstGui = Tkinter.Tk()
firstGui.title("mRMR App")
firstGui.resizable(False, False)
firstGui.focus_force()
firstGui.protocol('WM_DELETE_WINDOW', closeMainGui)
firstGui.geometry("600x300+%d+%d" % ((firstGui.winfo_screenwidth() / 4),
                                     (firstGui.winfo_screenheight() / 4)))
GuiFrame = LabelFrame(firstGui, text="Data File Path")
GuiFrame.config(font="System", padx=10, pady=25, relief="groove", fg="Red")
GuiFrame.pack(padx=10, pady=(60, 30))
fpath = StringVar()
filePath = Entry(GuiFrame, textvariable=fpath)
filePath.config(bd=3, width=65, font="Verdana 10", relief="ridge")
filePath.pack(pady=(15, 5))
importButton = Button(GuiFrame, text="Import", command=importData)
importButton.config(width=12, pady=5, bg="#FF4040")
importButton.pack(side=RIGHT, pady=(0, 10))
browseButton = Button(GuiFrame, text="Browse", command=browseFiles)
browseButton.config(width=12, pady=5)
browseButton.pack(side=RIGHT, padx=10, pady=(0, 10))
aboutButton = Button(firstGui, text="About", command=aboutApp)
aboutButton.config(width=12, pady=2, bg="#4863A0")
aboutButton.pack(side=RIGHT, padx=10, pady=5)
firstGui.mainloop()
firstGui.destroy()


optionsGui = Toplevel()
optionsGui.master.withdraw()
optionsGui.title("mRMR App")
optionsGui.resizable(False, False)
optionsGui.focus_force()
optionsGui.protocol('WM_DELETE_WINDOW', closeGUI2)
optionsGui.geometry("600x300+%d+%d" % ((optionsGui.winfo_screenwidth() / 4),
                                       (optionsGui.winfo_screenheight() / 4)))
L = LabelFrame(optionsGui, bd=0)
mFrame = LabelFrame(L, text="mRMR", bd=3)
mFrame.config(font="System", padx=10, pady=5, relief="groove", fg="Red")
mFrame.pack(side=LEFT, fill="both")
enablemrmr = StringVar()
enableclassify = StringVar()
C1 = Checkbutton(mFrame, text="Enable", variable=enablemrmr, width=20,
                 anchor=NW, font="Times 12 bold", command=togglemrmr)
C1.deselect()
C1.pack(side=TOP, fill="both", pady=(0, 10))
L1 = Label(mFrame, text="No. of Features to select:", anchor=W, font="Verdana 10", state=DISABLED)
L1.pack(fill="x")
nofeatures = IntVar()
nof = Entry(mFrame, textvariable=nofeatures, state=DISABLED)
nof.config(bd=2, relief="ridge", font="Verdana 10")
nof.pack(pady=10, anchor=W)
goforOpt=StringVar()
goforOptimal = Checkbutton(mFrame, text="Go for Optimal", variable=goforOpt, width=20,
                 anchor=NW, font="Verdana 10", state=DISABLED)
goforOptimal.deselect()
goforOptimal.pack(side=TOP, fill="both", pady=(0, 10))
cFrame = LabelFrame(L, text="Classification", bd=3)
cFrame.config(font="System", padx=10, pady=5, relief="groove", fg="Red")
cFrame.pack(side=RIGHT, fill="both")
C2 = Checkbutton(cFrame, text="Enable", variable=enableclassify, width=20,
                 anchor=NW, font="Times 12 bold", command=toggleclassify)
C2.deselect()
C2.pack(fill="both")
fullDataClassify = StringVar()
CfData = Checkbutton(cFrame, text="Use Full Data", variable=fullDataClassify,
                    anchor=NW, font="Verdana 10",state=DISABLED)
CfData.deselect()
CfData.pack(fill="x")
reduDataClassify = StringVar()
CrData = Checkbutton(cFrame, text="Use Reduced Data", variable=reduDataClassify,
                    anchor=NW, font="Verdana 10",state=DISABLED)
CrData.deselect()
CrData.pack(fill="x")
L2 = Label(cFrame, text="Training/Total Data Ratio:", anchor=W, font="Verdana 10", state=DISABLED)
L2.pack(fill="x")
splitRatio = DoubleVar()
sratio = Entry(cFrame, textvariable=splitRatio, state=DISABLED)
sratio.config(bd=2, relief="ridge", font="Verdana 10")
sratio.pack(pady=(5, 30), side=LEFT)
L.pack(padx=50, pady=(40, 0), fill="both")
runButton = Button(optionsGui, text="Run", command=RunTheApp)
runButton.config(width=12, pady=5, bg="#FF4040")
runButton.pack(side=RIGHT, padx=(0, 40))
optionsButton = Button(optionsGui, text="Options", command=setOptions)
optionsButton.config(width=12, pady=5, bg="#4863A0")
optionsButton.pack(side=RIGHT, padx=10)
optionsGui.mainloop()
