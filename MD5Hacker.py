import socket, threading, hashlib
import piro

#check if the code works!!!
class Patzhan:
    def __init__(self,port):
        self.socket = socket.socket()
        self.socket.bind(("127.0.0.1",port))
        self.socket.connect(("127.0.0.1",13370))
        print("Connected")
    
    def reconnect(self,port):
        self.socket.send("Howdy".encode())
        id = self.socket.recv(1024).decode()
        self.socket.close()
        self.socket = socket.socket()
        self.socket.bind(("127.0.0.1",port+int(id)))
        self.socket.listen(1)
        self.clientSoc, addr = self.socket.accept()
        Patzhan.start_hacking(self,id)

    def start_hacking(self,id):
        msg = self.clientSoc.recv(1024).decode()
        while True:                
            md5 = msg.split(',')[2]
            start = msg.split(',')[0]
            stop = msg.split(',')[1]

            #add the new stop and start for the different threads
            #you need to split the range into two different ones
            t1_stop ='bbb'
            t2_start ='bbc'
        
            results_lst = [None,None] #a list that saves the return values from each thread (true\false, and if true- the found password)
            thread_lst = [None,None]
                
            #starts the threads, each one with it's own range values
            thread_lst[0] = threading.Thread(target=Patzhan.find_password, args=(start,t1_stop,md5,results_lst,0))
            thread_lst[1] = threading.Thread(target=Patzhan.find_password, args=(t2_start,stop,md5,results_lst,1))
            
            thread_lst[0].start()    
            thread_lst[1].start()  

            for i in thread_lst: #keeps the threads alive until the main thread finishes
                i.join()
        
            answer_str = str(id) + "," #the string that needs to be returned to the server at the end of the search
            
            if (results_lst[0]==True) or (results_lst[1]==True): #if one of the threads found the password- return true to the server
                answer_str += str(True) + "," + str(md5) + "," + str(results_lst[2])
            else:
                answer_str += str(False) + "," + str(md5) + "," + ""
            
            print(answer_str)
            self.clientSoc.send(answer_str.encode())

            msg1 = self.clientSoc.recv(1024).decode()
            if(msg1.split(",")[0]=="FINISH"):
                #finish shenanigans- lights and music
                piro.main()
                msg=self.clientSoc.recv(1024).decode()
            else:
                msg = msg1
            
      
    def to_ascii_list(str):
        lst = []
        for c in str:
            lst.append(ord(c))
        return lst

    def to_str(ascii_list):
        str = ''
        for c in ascii_list:
            str += chr(c)
        return str

    #this function searches for the password and returns true or false. if found it appends the password to the result list
    def find_password(start,stop,md5,results_lst,i):
        password = start
        pass_ascii = []
        find = md5
        
        while password != '' and password != stop:
            print(password)
            
            if hashlib.md5(password.encode()).hexdigest() == find:
                results_lst[i] = True
                results_lst.append(Patzhan.to_str(pass_ascii)) #adds the found password to the result list
                return 
            
            pass_ascii = Patzhan.to_ascii_list(password)

            for n in reversed(range(len(pass_ascii))):
                pass_ascii[n] += 1

                if pass_ascii[n] > ord('z'):                    
                    if n == 0:
                        pass_ascii = ''
                        break
                
                    pass_ascii[n] = ord('a')

                else:
                    break

            password = Patzhan.to_str(pass_ascii)
        
        results_lst[i] = False
        return 

if __name__=="__main__":
    pz = Patzhan(12345)
    while True:
        pz.reconnect(12345)
