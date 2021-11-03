import socket as sock
from threading import Thread
from time import sleep
from random import randint

class ChatOutgoingThread(Thread):
    def __init__(self,incoming_thread):
        Thread.__init__(self)
        self.incoming_thread = incoming_thread
        self.messages = []
        self.kill = False
    
    def sendMessage(self,usr,msg): #Sending clients messages to server 
        if self.kill == False:
            conn = self.incoming_thread.getConn() 
            print("[{}] : {}".format(usr,msg))
            self.botMsg(usr,msg)

    def queueMsg(self,user,msg): #Storing the clients messages in queue 
        data = (user,msg)
        self.messages.append(data)

    def OutKillThread(self):
        self.kill = True

    def botMsg(self,usr,msg): #Sending the client message to all other clients except which send this...
        if self.kill == False:
            conn = self.incoming_thread.getConn() 
            for client in Clients:
                if conn == client:
                    pass
                else:
                    client.sendall("[{}] : {}\nche@server:~$ ".format(usr,msg).encode())
    def run(self):
        while True:
            if self.kill:
                break
            else:
                if len(self.messages) > 0:
                    for message in self.messages:
                        self.sendMessage(message[0],message[1])
                        self.messages.remove(message)

            

class ChatIncomingThread(Thread):
    def __init__(self,conn,addr):
        Thread.__init__(self)
        self.conn = conn
        self.ip = addr[0]
        self.kill = False

    def getConn(self): # get client connection method
        return self.conn

    def isClosed(self): #check if the client connection is closed or not
        return self.conn._closed
    
    def initOutgoingThread(self): #Method for initiate the ChatOutgoingThread class  
        self.Outgoing_thread = ChatOutgoingThread(self)
        self.Outgoing_thread.start()
    
    def sendMessage(self,message): #Sending incoming messages to ChatOutgoingThread sendMessage() method 
        self.Outgoing_thread.queueMsg(self.ip,message)

    def killThread(self): 
        self.kill = True

    def run(self): 
        self.initOutgoingThread() 
        conn.sendall("\nWelcome to chat server:)\nche@server:~$ ".encode())
        while not self.conn._closed:
            data = self.conn.recv(1024)
            data = data.decode().rstrip()
            if data == "quit":
                Clients.remove(self.conn) #remove a client from a clients list, if a client is disconnected
                self.Outgoing_thread.OutKillThread() 
                self.killThread()
                try:
                    self.conn.close()
                except:                #continue
                    pass 
            else:
                self.conn.sendall("che@server:~$ ".encode())
                self.sendMessage(data)  
                
                            
Clients = []   #List for new client connections
s = sock.socket(sock.AF_INET,sock.SOCK_STREAM)
s.setsockopt(sock.SOL_SOCKET,sock.SO_REUSEADDR,1)
s.bind(("",4444))
s.listen()
print("Server Listening ...")
while True:
    conn,addr = s.accept()
    Clients.append(conn)  #Append the client to clients list 
    t1 = ChatIncomingThread(conn,addr) #Starting theard for new connection
    t1.start()
