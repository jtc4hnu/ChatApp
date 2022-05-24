#Jack Chandler
#16 January 2020
#ChatApp

from tkinter import *
from tkinter import ttk
from datetime import datetime
import time
import threading
import socketScript as sks

class MainWindow:
    def __init__(self):
        print("\n")
        self.__root = Tk()
        version = "0.5.2"
        self.__root.title("ChatApp_v_"+version)
        
        #User Settings
        self.__autoScroll = True
        self.__username = "Guest"

        #Socket
        self.__socket = sks.NewSocket()

        #Variables
        self.__textPos = 3;
        self.__connected = False
        self.__thread = threading.Thread(target = self.ReceiveThread)
        
        #Labels
        Label(self.__root, text = "ChatApp", font = ("courier", 30)).grid(
            row = 0, columnspan = 4, pady = 4, padx = 20)

        Label(self.__root, text = "In conversation with host:", font = ("veranda", 14)).grid(
            row = 1, column = 1, sticky = "w")
        
        self.__hostLabel = Label(self.__root, text = "NO HOST", font = ("veranda", 14))
        self.__hostLabel.grid(row = 1, column = 2, padx = 10, sticky = "w")
        
        Label(self.__root, text = "Version " + version, font = ("veranda", 14)).grid(
            row = 1, column = 0, padx = 5, sticky = "w")
        
        self.__usernameLabel = Label(self.__root, text = "Guest", font = ("veranda", 14))
        self.__usernameLabel.grid(row = 1, column = 3, padx = 10, sticky = "e")

        #Chat Display
        scrollBar = Scrollbar(self.__root)
        scrollBar.grid(row = 2, column = 3, sticky = "ns")

        self.__displayChat = Text(self.__root, wrap=WORD, yscrollcommand=scrollBar.set)
        self.__displayChat.insert("1.0", "Welcome to ChatApp! Please be nice!\n")
        self.__displayChat.insert("2.0", "Use /help to get a list of available functions.\n")
        self.__displayChat.grid(row = 2, column = 0, columnspan = 3, padx = 5)

        scrollBar.config(command=self.__displayChat.yview)

        #Command Line
        self.__commandLine = Entry(self.__root, width = 100)
        self.__commandLine.grid(row = 3, columnspan = 4)
        self.__commandLine.bind("<Return>", self.__Input)

        self.__thread.start()
        mainloop()

        
    def ReceiveThread(self):
        time.sleep(0.5)
        self.__thread = threading.Thread(target = self.ReceiveThread)
        self.__thread.start()
        if self.__connected:
            self.Receive()
        
    def SystemLog(self, msg):
        current_time = datetime.now().strftime("%H:%M:%S")
        print("[" + current_time + "] " + msg)
        
        mainloop()
    def __Display(self, text):
        self.__displayChat.insert(str(self.__textPos) + ".0", text + "\n")
        self.__textPos += 1
        if self.__autoScroll:
            self.__displayChat.see("end")
        
    def Receive(self):
        data = self.__socket.SocketReceive()
        print(data)
        if data != None:
            self.__Display(data)
            
    def Send(self, msg):
        if self.__connected:
            self.__socket.SocketSend(self.__username + "|__|" + msg)
        else:
            self.__Display("Please use /connect to connect to a host!")
        
    def __ProcessCommand(self, cmd):
        if len(cmd) == 0:
            self.__Display("No Command Input")
        elif len(cmd) == 1:
                 
            if cmd[0] == "help":
                self.__Display("Help is currently not avilable")
            elif cmd[0] == "autoscroll":
                self.__autoscroll = not self.__autoscroll
            else:
                self.__Display("Command not recognized")

        elif len(cmd) == 2:
            
            if  cmd[0] == "connect":
                try:
                    self.__socket.Connect(cmd[1])
                    self.__connected = True
                    self.__hostLabel["text"] = cmd[1]
                except:
                    self.__Display("Cannot connect to provided host")
                    self.SystemLog("SocketError: host: " + cmd[1])

            else:
                self.__Display("Command not recognized")

        elif len(cmd) == 3:
            
            if cmd[0] == "set":
                if cmd[1] == "username":
                    self.__username = cmd[2]
                    self.__usernameLabel["text"] = cmd[2]
            else:
                self.__Display("Command not recognized")
   
        else:
            self.__Display("Command not recognized")
            
    def __Input(self, uinput):        
        uinput = self.__commandLine.get()
        self.__commandLine.delete(0,len(uinput))
        
        if uinput[0] == "/":
            self.__Display(uinput)
            self.__ProcessCommand(uinput[1:len(uinput)].split())
        else:
            self.Send(uinput)
            
        self.SystemLog("UIR_Call: '" + uinput + "'")

MainWindow()


