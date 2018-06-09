# import Tkinter
# from Tkinter import *
# from ScrolledText import *
# import tkFileDialog
# import tkMessageBox
#[25, 877, 248, 305, 46, 30, 821, 0, 285, 8]
# root = Tkinter.Tk(className=" Just another Text Editor")
# textPad = ScrolledText(root, width=100, height=80)
#
# # create a menu & define functions for each menu item
#
# def open_command():
#         file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file')
#         if file != None:
#             contents = file.read()
#             textPad.insert('1.0',contents)
#             file.close()
#
# def save_command(self):
#     file = tkFileDialog.asksaveasfile(mode='w')
#     if file != None:
#     # slice off the last character from get, as an extra return is added
#         data = self.textPad.get('1.0', END+'-1c')
#         file.write(data)
#         file.close()
#
# def exit_command():
#     if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
#         root.destroy()
#
# def about_command():
#     label = tkMessageBox.showinfo("About", "Just Another TextPad \n Copyright \n No rights left to reserve")
#
#
# def dummy():
#     print "I am a Dummy Command, I will be removed in the next step"
# menu = Menu(root)
# root.config(menu=menu)
# filemenu = Menu(menu)
# menu.add_cascade(label="File", menu=filemenu)
# filemenu.add_command(label="New", command=dummy)
# filemenu.add_command(label="Open...", command=open_command)
# filemenu.add_command(label="Save", command=save_command)
# filemenu.add_separator()
# filemenu.add_command(label="Exit", command=exit_command)
# helpmenu = Menu(menu)
# menu.add_cascade(label="Help", menu=helpmenu)
# helpmenu.add_command(label="About...", command=about_command)
#
#
# textPad.pack()
# root.mainloop()


# C:/Users/Prince/PycharmProjects/mrmr/checkmark.gif

# from threading import Thread
# from Tkinter import *
# import time
# import os
#
# class Application(Frame):
#     exitFlag = 0
#     def __init__(self, parent):
#         Frame.__init__(self,parent)
#         self.pack(fill="both")
#         self.num = 0
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.label = Label(self, bd=0)
#         self.label.pack(fill="both")
#         Thread(target=self.animate).start()
#
#     def stop(self):
#         self.exitFlag=1
#
#     def animate(self):
#         while True:
#             try:
#                 time.sleep(0.1)
#                 img = PhotoImage(file="imgsrc/gears4/gears4.gif", format="gif - {}".format(self.num))
#                 self.label.config(image=img)
#                 self.label.config(bg="white")
#                 self.label.image=img
#                 self.num += 1
#             except:
#                 self.num = 0
#             if self.exitFlag:
#                 try:
#                     Frame.destroy()
#                     break
#                 except:
#                     pass
#                 break
#
# # root.()
# # app = Application(root)
# # root.mainloop()
#
# from Tkinter import *
# import ttk
# root = Tk()
# progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
# progressbar.pack(side="bottom")
# progressbar.start()
# progressbar.step(50)
# root.mainloop()

# from PIL import Image
#
# class ImageSequence:
#         def __init__(self, img):
#             self.img = img
#         def __getitem__(self, ix):
#             try:
#                 if ix:
#                     self.img.seek(ix)
#                 return self.img
#             except EOFError:
#                 raise IndexError # end of sequence
#
#
# # load an animated GIF file you have
# # you may need to change the subdirectory
# img = Image.open("imgsrc/work/work.gif")
#
# # optional, create a list of the frames's filenames
# fname_list = []
#
# # create individual frames and save them in sequence
# count = 1
# # pick a name you like for your individual gifs
# name = "work"
# for frame in ImageSequence(img):
#     # create the sequenced file name
#     # eg. A_Dog01.gif  A_Dog02.gif  ...
#     fname = "imgsrc/work/{}{:02d}.gif".format(name, count)
#     # frame.save(fname)
#     count += 1
#     fname_list.append(fname)
#
# # import pprint
# # pprint.pprint(fname_list)
#
# ''' possible result ...
# ['../image/A_Dog01.gif',
#  '../image/A_Dog02.gif',
#  '../image/A_Dog03.gif',
#  '../image/A_Dog04.gif',
#  '../image/A_Dog05.gif',
#  '../image/A_Dog06.gif',
#  '../image/A_Dog07.gif']
# '''
#
# ''' tk_animate_GIF_sequence.py
# play a sequence of gifs to create an animation effect
# the gif sequence was create with PIL_animatedGif_frames.py
# note:  Tkinter cannot display animated gifs directly
# (dns)
# '''
#
# seq = 0
# import itertools as it
# try:
#     # Python2
#     import Tkinter as tk
# except ImportError:
#     # Python3
#     import tkinter as tk
#
# def animate():
#     """ cycle through """
#     global seq
#     seq += 1
#     img = next(pictures)
#     label["image"] = img
#     # if seq > count:
#     #     root.destroy()
#     # else:
#     root.after(delay, animate)
#
#
# # root = tk.Tk()
# # root.geometry("500x300+%d+%d" %((root.winfo_screenwidth()/4),(root.winfo_screenheight()/4)))
#
# label = tk.Label(root)
# label.config(bg="white")
# label.pack(fill="both")
# # this list created with the PIL program
# # it may be different in your case
# # fname_list = \
# # ['../image/A_Dog01.gif',
# #  '../image/A_Dog02.gif',
# #  '../image/A_Dog03.gif',
# #  '../image/A_Dog04.gif',
# #  '../image/A_Dog05.gif',
# #  '../image/A_Dog06.gif',
# #  '../image/A_Dog07.gif']
#
# # store as tk img_objects
# pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in fname_list)
#
# # milliseconds
# delay = 100
#
# animate()
#
# root.mainloop()

# import Tkinter
# import threading
#
# class AnimationApp(threading.Thread):
#     frameNo = 1
#     exitFlag = 0
#     def __init__(self,parent,imgFile,delay=0.2):
#         self.parent=parent
#         self.image=imgFile
#         self.interval=delay
#         threading.Thread.__init__(self)
#         self.daemon=True
#         self.start()
#
#     def callback(self):
#         self.exitFlag = 1
#         self.animeWin.quit()
#         # self.root.destroy()
#         # time.sleep(5)
#
#     def run(self):
#         self.animeWin = Toplevel(self.parent)
#         self.animeWin.title("3")
#         self.animeWin.protocol("WM_DELETE_WINDOW", self.callback)
#         label = Tkinter.Label(self.animeWin)
#         while True:
#             time.sleep(self.interval)
#             try:
#                 label.config(bg="white")
#                 label.pack(fill="x", pady=20)
#                 img = PhotoImage(file="imgsrc/"+self.image+".gif",format="gif - {}".format(self.frameNo))
#                 label.config(image=img)
#                 label.image = img
#                 self.frameNo += 1
#             except:
#                 self.frameNo=0
#             self.animeWin.update()
#             if self.exitFlag:
#                 break
#
#
# gui = Tkinter.Tk()
# # t=Toplevel(gui)
# button = Button(gui, text="Quit", command=lambda :gui.quit())
# button.pack(fill="x")
# gui.mainloop()
# # t.destroy()
# gui.destroy()
#
# gui = Tkinter.Tk()
# gui.title("1")
# t=Toplevel(gui)
# t.title("2")
# app = AnimationApp(t,"brain")
# print('Now we can continue running code while mainloop runs!')
#
# for i in range(30):
#     print(i)
#     if i==20:
#         app.callback()
#     time.sleep(0.5)
# # gui.update()
# top=Toplevel(gui)
# button = Button(top, text="Quit", command=lambda :top.quit())
# button.pack(fill="x")
# top.mainloop()
# # gui.mainloop()


# Back-Propagation Neural Networks
#
# Written in Python.  See http://www.python.org/
# Placed in the public domain.
# Neil Schemenauer <nas@arctrix.com>

# import math
# import random
# import string
#
# random.seed(0)
#
# # calculate a random number where:  a <= rand < b
# def rand(a, b):
#     return (b-a)*random.random() + a
#
# # Make a matrix (we could use NumPy to speed this up)
# def makeMatrix(I, J, fill=0.0):
#     m = []
#     for i in range(I):
#         m.append([fill]*J)
#     return m
#
# # our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
# def sigmoid(x):
#     return math.tanh(x)
#
# # derivative of our sigmoid function, in terms of the output (i.e. y)
# def dsigmoid(y):
#     return 1.0 - y**2
#
# class NN:
#     def __init__(self, ni, nh, no):
#         # number of input, hidden, and output nodes
#         self.ni = ni + 1 # +1 for bias node
#         self.nh = nh
#         self.no = no
#
#         # activations for nodes
#         self.ai = [1.0]*self.ni
#         self.ah = [1.0]*self.nh
#         self.ao = [1.0]*self.no
#
#         # create weights
#         self.wi = makeMatrix(self.ni, self.nh)
#         self.wo = makeMatrix(self.nh, self.no)
#         # set them to random vaules
#         for i in range(self.ni):
#             for j in range(self.nh):
#                 self.wi[i][j] = rand(-0.2, 0.2)
#         for j in range(self.nh):
#             for k in range(self.no):
#                 self.wo[j][k] = rand(-2.0, 2.0)
#
#         # last change in weights for momentum
#         self.ci = makeMatrix(self.ni, self.nh)
#         self.co = makeMatrix(self.nh, self.no)
#
#     def update(self, inputs):
#         if len(inputs) != self.ni-1:
#             raise ValueError('wrong number of inputs')
#
#         # input activations
#         for i in range(self.ni-1):
#             #self.ai[i] = sigmoid(inputs[i])
#             self.ai[i] = inputs[i]
#
#         # hidden activations
#         for j in range(self.nh):
#             sum = 0.0
#             for i in range(self.ni):
#                 sum = sum + self.ai[i] * self.wi[i][j]
#             self.ah[j] = sigmoid(sum)
#
#         # output activations
#         for k in range(self.no):
#             sum = 0.0
#             for j in range(self.nh):
#                 sum = sum + self.ah[j] * self.wo[j][k]
#             self.ao[k] = sigmoid(sum)
#
#         return self.ao[:]
#
#
#     def backPropagate(self, targets, N, M):
#         if len(targets) != self.no:
#             raise ValueError('wrong number of target values')
#
#         # calculate error terms for output
#         output_deltas = [0.0] * self.no
#         for k in range(self.no):
#             error = targets[k]-self.ao[k]
#             output_deltas[k] = dsigmoid(self.ao[k]) * error
#
#         # calculate error terms for hidden
#         hidden_deltas = [0.0] * self.nh
#         for j in range(self.nh):
#             error = 0.0
#             for k in range(self.no):
#                 error = error + output_deltas[k]*self.wo[j][k]
#             hidden_deltas[j] = dsigmoid(self.ah[j]) * error
#
#         # update output weights
#         for j in range(self.nh):
#             for k in range(self.no):
#                 change = output_deltas[k]*self.ah[j]
#                 self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
#                 self.co[j][k] = change
#                 #print N*change, M*self.co[j][k]
#
#         # update input weights
#         for i in range(self.ni):
#             for j in range(self.nh):
#                 change = hidden_deltas[j]*self.ai[i]
#                 self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
#                 self.ci[i][j] = change
#
#         # calculate error
#         error = 0.0
#         for k in range(len(targets)):
#             error = error + 0.5*(targets[k]-self.ao[k])**2
#         return error
#
#
#     def test(self, patterns):
#         for p in patterns:
#             print(p[0], '->', self.update(p[0]))
#
#     def weights(self):
#         print('Input weights:')
#         for i in range(self.ni):
#             print(self.wi[i])
#         print()
#         print('Output weights:')
#         for j in range(self.nh):
#             print(self.wo[j])
#
#     def train(self, patterns, iterations=1000, N=0.5, M=0.1):
#         # N: learning rate
#         # M: momentum factor
#         for i in range(iterations):
#             error = 0.0
#             for p in patterns:
#                 inputs = p[0]
#                 targets = p[1]
#                 self.update(inputs)
#                 error = error + self.backPropagate(targets, N, M)
#             if i % 100 == 0:
#                 print('error %-.5f' % error)
#
#
# def demo():
#     # Teach network XOR function
#     pat1 = [
#         [[1,3], [1]],
#         [[4,6], [0]],
#         [[7,9], [1]],
#         [[3,5], [1]],
#         [[6,8], [0]],
#         [[2,4], [0]],
#         [[1,9], [1]],
#         [[6,8], [0]]
#     ]
#     pat2 = [
#         [[8,6], [0]],
#         [[3,9], [1]],
#     ]
#
#     # create a network with two input, two hidden, and one output nodes
#     n = NN(2, 2, 1)
#     # train it with some patterns
#     n.train(pat1)
#     # test it
#     n.test(pat2)
#
#
#
# if __name__ == '__main__':
#     demo()


# from pybrain.datasets            import ClassificationDataSet
# from pybrain.utilities           import percentError
# from pybrain.tools.shortcuts     import buildNetwork
# from pybrain.supervised.trainers import BackpropTrainer
# from pybrain.structure.modules   import SoftmaxLayer
# from sklearn import datasets
#
#
# iris = datasets.load_iris()
# X, y = iris.data, iris.target
# # print X
# # print '--------------------------'
# # print y
# ds = ClassificationDataSet(4, 1, nb_classes=3)
# for i in range(len(X)):
#     ds.addSample(X[i],y[i])
#
# # print ds['input']
# # print ds['target']
# # print len(ds), len(ds['input']), len(ds['target'])
#
# # trndata,partdata = ds.splitWithProportion (0.70)
# # tstdata,validata = partdata.splitWithProportion(0.50)
# trndata,tstdata = ds.splitWithProportion (0.70)
#
# trndata._convertToOneOfMany()
# tstdata._convertToOneOfMany()
# # validata._convertToOneOfMany()
#
#
# net = buildNetwork(4,5,3, outclass=SoftmaxLayer)
# trainer =BackpropTrainer(net,dataset=trndata,momentum=0.1,verbose=False,weightdecay=0.01)
# # trnerr,valerr = trainer.trainUntilConvergence(dataset=trndata,maxEpochs=50)
# # pl.plot(trnerr,'b',valerr,'r')
# trainer.trainOnDataset(trndata,100)
# # exit(0)
# # print trainer.totalepochs
# # out = net.activateOnDataset(tstdata).argmax(axis=1)
# out = net.activateOnDataset(tstdata)
# out = out.argmax(axis=1)
# # for i in tstdata['class']:
# #     print i[0],
# # print ''
# # print out
# print percentError( out, tstdata['class'] )
# # output = net.activateOnDataset(validata)
# # output = output.argmax(axis=1)
# # print percentError( output, validata['class'] )

# from __future__ import division
# from numpy import array, shape, where, in1d
# import math
# import time
#
# class InformationTheoryTool:
#
#     def __init__(self, data):
#         # Check if all rows have the same length
#         assert (len(data.shape) == 2)
#         print data.shape
#         # Save data
#         self.data = data
#         self.n_rows = data.shape[0]
#         self.n_cols = data.shape[1]
#
#     def single_entropy(self, x_index, log_base, debug = False):
#         """
#         Calculate the entropy of a random variable
#         """
#         # Check if index are into the bounds
#         assert (x_index >= 0 and x_index <= self.n_rows)
#         # Variable to return entropy
#         summation = 0.0
#         # Get uniques values of random variables
#         values_x = set(data[x_index])
#         # Print debug info
#         if debug:
#             print 'Entropy of'
#             print data[x_index]
#         # For each random
#         for value_x in values_x:
#             px = shape(where(data[x_index]==value_x))[1] / self.n_cols
#             if px > 0.0:
#                 summation += px * math.log(px, log_base)
#             if debug:
#                 print '(%d) px:%f' % (value_x, px)
#         if summation == 0.0:
#             return summation
#         else:
#             return - summation
#
#
#     def entropy(self, x_index, y_index, log_base, debug = False):
#         """
#         Calculate the entropy between two random variable
#         """
#         assert (x_index >= 0 and x_index <= self.n_rows)
#         assert (y_index >= 0 and y_index <= self.n_rows)
#         # Variable to return MI
#         summation = 0.0
#         # Get uniques values of random variables
#         values_x = set(data[x_index])
#         values_y = set(data[y_index])
#         # Print debug info
#         if debug:
#             print 'Entropy between'
#             print data[x_index]
#             print data[y_index]
#         # For each random
#         for value_x in values_x:
#             for value_y in values_y:
#                 pxy = len(where(in1d(where(data[x_index]==value_x)[0],
#                                 where(data[y_index]==value_y)[0])==True)[0]) / self.n_cols
#                 if pxy > 0.0:
#                     summation += pxy * math.log(pxy, log_base)
#                 if debug:
#                     print '(%d,%d) pxy:%f' % (value_x, value_y, pxy)
#         if summation == 0.0:
#             return summation
#         else:
#             return - summation
#
#     def mutual_information(self, x_index, y_index, log_base, debug = True):
#         """
#         Calculate and return Mutual information between two random variables
#         """
#         # Check if index are into the bounds
#         assert (x_index >= 0 and x_index <= self.n_rows)
#         assert (y_index >= 0 and y_index <= self.n_rows)
#         # Variable to return MI
#         summation = 0.0
#         # Get uniques values of random variables
#         values_x = set(data[x_index])
#         values_y = set(data[y_index])
#         print values_x
#         print values_y
#         # Print debug info
#         if debug:
#             print 'MI between'
#             print data[x_index]
#             print data[y_index]
#         # For each random
#         for value_x in values_x:
#             for value_y in values_y:
#                 px = shape(where(data[x_index]==value_x))[1] / self.n_cols
#                 py = shape(where(data[y_index]==value_y))[1] / self.n_cols
#                 pxy = len(where(in1d(where(data[x_index]==value_x)[0],
#                                 where(data[y_index]==value_y)[0])==True)[0]) / self.n_cols
#                 if pxy > 0.0:
#                     summation += pxy * math.log((pxy / (px*py)), log_base)
#                 if debug:
#                     print '(%d,%d) px:%f py:%f pxy:%f' % (value_x, value_y, px, py, pxy)
#         return summation
#
#
#
# # Define data array
# myList=[[1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
#         [0, 0, 2, 2, 4, 4, 0, 0, 4, 2, 0, 4],
#         [7, 8, 8, 8, 7, 7, 0, 8, 0, 0, 8, 7]]
# data = array(myList)
#
# # Create object
# it_tool = InformationTheoryTool(data)
#
# # --- Checking entropy between two random variables
# # entropy of  X_0 (0, 0, 1, 1, 0, 1, 1, 2, 2, 2) and X_1 (3, 4, 5, 5, 3, 2, 2, 6, 6, 1)
# # t_start = time.time()
# # print 'Entropy(X_0, X_1): %f' % it_tool.entropy(0, 1, 10)
# # print 'Elapsed time: %f\n' % (time.time() - t_start)
#
# # entropy of  X_3 (7, 7, 7, 7, 7, 7, 7, 7, 7, 7) and X_3 (7, 7, 7, 7, 7, 7, 7, 7, 7, 7)
# # t_start = time.time()
# # print 'Entropy(X_3, X_3): %f' % it_tool.entropy(3, 3, 10)
# # print 'Elapsed time: %f\n' % (time.time() - t_start)
#
# # ---Checking Mutual Information between two random variables
#
# # Print mutual information between X_0 (0,0,1,1,0,1,1,2,2,2) and X_1 (3,4,5,5,3,2,2,6,6,1)
# t_start = time.time()
# print 'MI(X_0, X_1): %f' % it_tool.mutual_information(0, 2, 2)
# # print 'MI(X_0, X_2): %f' % it_tool.mutual_information(0, 2, 2)
# # print 'MI(X_1, X_2): %f' % it_tool.mutual_information(1, 2, 2)
#
# # Print mutual information between X_1 (3,4,5,5,3,2,2,6,6,1) and X_2 (7,2,1,3,2,8,9,1,2,0)
# # t_start = time.time()
# # print 'MI(X_1, X_2): %f' % it_tool.mutual_information(1, 2, 10)
# # print 'Elapsed time: %f\n' % (time.time() - t_start)
#
#
# # --- Checking results
# # Checking entropy results
# for i in range(0,data.shape[0]):
#     assert(it_tool.entropy(i, i, 10) == it_tool.single_entropy(i, 10))
#
# # Checking mutual information results
# # MI(X,Y) = H(X) + H(Y) - H(X,Y)
# n_rows = data.shape[0]
# i = 0
# while i < n_rows:
#     j = i + 1
#     while j < n_rows:
#         if j != i:
#             # print (it_tool.mutual_information(i, j, 10),
#             #             it_tool.single_entropy(i, 10)+it_tool.single_entropy(j, 10)-it_tool.entropy(i, j, 10))
#             pass
#         j += 1
#     i += 1


# import smtplib
#
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login("mrmrapp.auto@gmail.com", "mrmr12345")
#
# msg = "YOUR MESSAGE! \n Hi there.."
# server.sendmail("mrmrapp.auto@gmail.com", "nphard12@gmail.com", msg)
# server.quit()

# import os
# import zipfile
#
# def zipdir(path, ziph):
#     # ziph is zipfile handle
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             # root = root.split('\\')[-1]
#             # print os.path.join(root, file)
#             ziph.write(os.path.join(root, file), arcname=root.split('\\')[-1]+'\\'+file)
#             # print root+file+''
#
# if __name__ == '__main__':
#     zipf = zipfile.ZipFile('mRMRStats.zip', 'w', zipfile.ZIP_DEFLATED)
#     zipdir('outPut\\mRMR_12-May-2016_2347', zipf)
#     zipf.close()


# import smtplib
# import platform
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
#
#
# msg = MIMEMultipart()
# msg['From'] = "mrmrapp.auto@gmail.com"
# msg['To'] = "nphard12@gmail.com"
# msg['Subject'] = "SUBJECT OF THE EMAIL"
#
# dirName = "mRMR_14-May-2016_0710"
# body = ("\nHi\n\nThe details for mRMR App run you initiated are as follows.\n\n"
#     "  Date        : " + dirName.split('_')[1] + "\n"
#     "  Time        : " + dirName.split('_')[2] + " Hrs\n"
#     "  System Name : " + platform.node() + "\n"
#     "  System Info : " + platform.system()+" "+platform.release()+"\n\n"
#     "The detailed Statistics are also enclosed hereby.Extract the file in your system \n"
#     "to view the results.\n\n"
#     "Have a great day..!\n\n"
#     "*****************************************************************************************\n"
#     "    This is a script generated mail. Please mail to the admin at krprince16@gmail.com    \n"
#     "    in case of any queries.\n\n"
#     "*****************************************************************************************\n")
#
# msg.attach(MIMEText(body, 'plain'))
#
# filename = "mRMRStats.zip"
# attachment = open("mRMRStats.zip", "rb")
#
# part = MIMEBase('application', 'octet-stream')
# part.set_payload(attachment.read())
# encoders.encode_base64(part)
# part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#
# msg.attach(part)
#
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login("mrmrapp.auto@gmail.com", "mrmr12345")
# text = msg.as_string()
# # print text
# server.sendmail("mrmrapp.auto@gmail.com", "nphard12@gmail.com", text)
# server.sendmail("mrmrapp.auto@gmail.com", "krprince16@gmail.com", text)
# server.quit()


# import numpy as np
#
# def sigmoid(x):
#     return 1.0/(1.0 + np.exp(-x))
#
# def sigmoid_prime(x):
#     return sigmoid(x)*(1.0-sigmoid(x))
#
# def tanh(x):
#     return np.tanh(x)
#
# def tanh_prime(x):
#     return 1.0 - x**2
#
#
# class NeuralNetwork:
#
#     def __init__(self, layers, activation='tanh'):
#         if activation == 'sigmoid':
#             self.activation = sigmoid
#             self.activation_prime = sigmoid_prime
#         elif activation == 'tanh':
#             self.activation = tanh
#             self.activation_prime = tanh_prime
#
#         # Set weights
#         self.weights = []
#         # layers = [2,2,1]
#         # range of weight values (-1,1)
#         # input and hidden layers - random((2+1, 2+1)) : 3 x 3
#         for i in range(1, len(layers) - 1):
#             r = 2*np.random.random((layers[i-1] + 1, layers[i] + 1)) -1
#             self.weights.append(r)
#         # output layer - random((2+1, 1)) : 3 x 1
#         r = 2*np.random.random( (layers[i] + 1, layers[i+1])) - 1
#         self.weights.append(r)
#
#     def fit(self, X, y, learning_rate=0.001, epochs=500):
#         # Add column of ones to X
#         # This is to add the bias unit to the input layer
#         ones = np.atleast_2d(np.ones(X.shape[0]))
#         X = np.concatenate((ones.T, X), axis=1)
#
#         for k in range(epochs):
#             if k % 10000 == 0: print 'epochs:', k
#
#             i = np.random.randint(X.shape[0])
#             a = [X[i]]
#
#             for l in range(len(self.weights)):
#                     dot_value = np.dot(a[l], self.weights[l])
#                     activation = self.activation(dot_value)
#                     a.append(activation)
#             # output layer
#             error = y[i] - a[-1]
#             deltas = [error * self.activation_prime(a[-1])]
#
#             # we need to begin at the second to last layer
#             # (a layer before the output layer)
#             for l in range(len(a) - 2, 0, -1):
#                 deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_prime(a[l]))
#
#             # reverse
#             # [level3(output)->level2(hidden)]  => [level2(hidden)->level3(output)]
#             deltas.reverse()
#
#             # backpropagation
#             # 1. Multiply its output delta and input activation
#             #    to get the gradient of the weight.
#             # 2. Subtract a ratio (percentage) of the gradient from the weight.
#             for i in range(len(self.weights)):
#                 layer = np.atleast_2d(a[i])
#                 delta = np.atleast_2d(deltas[i])
#                 self.weights[i] += learning_rate * layer.T.dot(delta)
#
#     def predict(self, x):
#         a = np.concatenate((np.ones(1).T, np.array(x)), axis=0)
#         for l in range(0, len(self.weights)):
#             a = self.activation(np.dot(a, self.weights[l]))
#         return a

import numpy as np

def tanh(x):
    return np.tanh(x)

def tanh_deriv(x):
    return 1.0 - np.tanh(x)**2

def logistic(x):
    return 1/(1 + np.exp(-x))

def logistic_derivative(x):
    return logistic(x)*(1-logistic(x))

class NeuralNetwork:
    def __init__(self, layers, activation='tanh'):
        """
        :param layers: A list containing the number of units in each layer.
        Should be at least two values
        :param activation: The activation function to be used. Can be
        "logistic" or "tanh"
        """
        if activation == 'logistic':
            self.activation = logistic
            self.activation_deriv = logistic_derivative
        elif activation == 'tanh':
            self.activation = tanh
            self.activation_deriv = tanh_deriv

        self.weights = []
        for i in range(1, len(layers) - 1):
            self.weights.append((2*np.random.random((layers[i - 1] + 1, layers[i]
                                + 1))-1)*0.25)
        self.weights.append((2*np.random.random((layers[i] + 1, layers[i +
                            1]))-1)*0.25)

    def fit(self, X, y, learning_rate=0.001, epochs=1000):
        X = np.atleast_2d(X)
        temp = np.ones([X.shape[0], X.shape[1] + 1])
        temp[:, 0:-1] = X  # adding the bias unit to the input layer
        X = temp
        y = np.array(y)

        for k in range(epochs):
            i = np.random.randint(X.shape[0])
            a = [X[i]]

            for l in range(len(self.weights)):
                a.append(self.activation(np.dot(a[l], self.weights[l])))
            error = y[i] - a[-1]
            deltas = [error * self.activation_deriv(a[-1])]

            for l in range(len(a) - 2, 0, -1):  # we need to begin at the second to last layer
                deltas.append(deltas[-1].dot(self.weights[l].T) * self.activation_deriv(a[l]))
            deltas.reverse()
            for i in range(len(self.weights)):
                layer = np.atleast_2d(a[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += learning_rate * layer.T.dot(delta)

    def predict(self, x):
        x = np.array(x)
        temp = np.ones(x.shape[0] + 1)
        temp[0:-1] = x
        a = temp
        for l in range(0, len(self.weights)):
            a = self.activation(np.dot(a, self.weights[l]))
        return a






from myUtilities import read_DataFile
myData = read_DataFile("data\\iris.csv")
nn = NeuralNetwork([myData[0][1],myData[0][1],1])
lim = int(myData[0][0]*0.7)
X = [i for i in [r[:-1] for r in myData[1:lim]]]
# X = np.array([[0, 0],
#               [0, 1],
#               [1, 0],
#               [1, 1]])
X = np.array(X)
# print [r[-1] for r in myData[1:]]
y = np.array([r[-1] for r in myData[1:lim]])
# print y
# print X.shape
# print y.shape
# exit(0)

# nn.fit(X, y)
# print len(X)
# X = np.array([i for i in [r[:-1] for r in myData[lim:]]])
# print len(X)
# tot = 0
# cor = 0
# for e in X:
#     # print(e,nn.predict(e))
#     p = nn.predict(e)
#     print p, myData[lim+tot][-1]
#     if p[0] > 0.5 and myData[lim+tot][-1] == 1:
#         cor += 1
#     if p[0] <=0.5 and myData[lim+tot][-1] == 0:
#         cor += 1
#     tot += 1
# print tot
# print cor
# print float((cor*100)/tot)


# Back-Propagation Neural Networks
#
# Written in Python.  See http://www.python.org/
# Placed in the public domain.
# Neil Schemenauer <nas@arctrix.com>

import math
import random
import string

random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2

class NN:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1 # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.ni-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)

        # output activations
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print N*change, M*self.co[j][k]

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, patterns):
        for p in patterns:
            print(p[0], '->', self.update(p[0]))

    def weights(self):
        print('Input weights:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('Output weights:')
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations=1000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 100 == 0:
                print('error %-.5f' % error)


def demo():
    # Teach network XOR function
    pat = [[[]]]
    for i in myData[1:]:
        # pat.insert(0,[[]])
        # pat[-1] = [i[:-1], [i[-1]]]
        # print [i[:-1], [i[-1]]]
        pat.append([i[:-1], [i[-1]]])
    pat = pat[1:]
    # print pat[0]
    #
    # pat = [
    #     [[0,0], [0]],
    #     [[0,1], [1]],
    #     [[1,0], [1]],
    #     [[1,1], [0]]
    # ]
    # print pat[0]

    # create a network with two input, two hidden, and one output nodes
    n = NN(int(myData[0][1]), int(myData[0][1]), 1)
    # train it with some patterns
    n.train(pat)
    # test it
    n.test(pat)

demo()