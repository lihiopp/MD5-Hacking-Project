import socket, threading, hashlib, scapy
import Piro
import time

class Patzhan:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(("10.30.58.40",13370))
        print("Connected")
    
    def reconnect(self):
        self.socket.send("Howdy".encode())
        id1 = self.socket.recv(1024).decode()
        print(id1)
        self.socket.close()
        self.socket = socket.socket()
        self.socket.bind(("10.30.56.116",13370+int(id1)))
        print(f"bind {13370+int(id1)}")
        self.socket.listen(4)
        print("listening")
        self.clientSoc, addr = self.socket.accept()
        print("server connected")
        Patzhan.start_hacking(self,id1)

    def start_hacking(self,id1):
        msg = self.clientSoc.recv(1024).decode()
        finished =[True,True]
        while True:
            print(msg)
            md5 = msg.split(',')[2]
            start = msg.split(',')[0]
            stop = msg.split(',')[1]

            
            t1_stop =Patzhan.HandleRanges(stop,start)
            if(t1_stop[7]=='z'):
                t2_start=chr(ord(t1_stop[0])+1)+"aaaaaaa"
            else:
                t2_start =t1_stop[0:7]+chr(ord(t1_stop[7])+1)
        
            results_lst = [None,None] #a list that saves the return values from each thread (true\false, and if true- the found password)
            thread_lst = [None,None]
                
            #starts the threads, each one with it's own range values
            thread_lst[0] = threading.Thread(target=Patzhan.generate, args=(start,t1_stop,md5,results_lst,0,finished))
            thread_lst[1] = threading.Thread(target=Patzhan.generate, args=(t2_start,stop,md5,results_lst,1,finished))
            
            thread_lst[0].start()    
            thread_lst[1].start()  

            for i in thread_lst: #keeps the threads alive until the main thread finishes
                i.join()
        
            answer_str = str(id1) + "," #the string that needs to be returned to the server at the end of the search
            
            if (results_lst[0]==True) or (results_lst[1]==True): #if one of the threads found the password- return true to the server
                answer_str += str(True) + "," + str(md5) + "," + str(results_lst[2])
            else:
                answer_str += str(False) + "," + str(md5) + ","
            
            print(answer_str)
            self.clientSoc.send(answer_str.encode())

            msg1 = self.clientSoc.recv(1024).decode()
            if(msg1.split(",")[0]=="finish"):
                #finish shenanigans- lights and music
                Piro.main()
                msg=self.clientSoc.recv(1024).decode()
            else:
                msg = msg1
            
    
    def generate(start,stop,md5, results_lst,i,finished):
        stop_char='z'
        length=len(start)
        s='a'
        ok=True

        while finished[i]:
            print(hashlib.md5(start.encode()).hexdigest())
            print(start)
            time.sleep(0.5)
            if(hashlib.md5(start.encode()).hexdigest()== md5):
                results_lst[i] = True
                results_lst.append(start) #adds the found password to the result list
                for stop in finished:
                    stop=False
                return 
            index=1
            if  chr(ord(start[length-index]) + 1)>stop_char: 
                flag=True 
                while flag:
                    #print "in while "+start[length-index]
                    start=start[:length-index-1]+chr(ord(start[length-index-1]) + 1)+start[length-index:]
                    #start[length-index-1]+='1'
                    start=start[:length-index]+ s + start[length-index+1:]
                    if (index+1)>=length:
                        flag=False
                    if start[length-index-1]<=stop_char:
                        flag=False
                    index+=1
            
            else:
                start=start[:length-index]+chr(ord(start[length-index]) + 1)+start[length-index+1:]
            if start>stop:
                ok=False
        results_lst[i] = False
        for stop in finished:
            stop=False
        return
        
    
    def HandleRanges(stop,start):
        int_to_char=[ord(stop[0])+ord(start[0]),ord(stop[1])+ord(start[1]),ord(stop[2])+ord(start[2]),ord(stop[3])+ord(start[3]),ord(stop[4])+ord(start[4]),ord(stop[5])+ord(start[5]),ord(stop[6])+ord(start[6]),ord(stop[7])+ord(start[7])]
        change=False
        for i in range(len(int_to_char)):
            x=int_to_char[i]
            if(change==False):
                if(x/2!=int(x/2)):
                    change=True
                x=int(x/2)
            else:
                if(x/2==int(x/2)):
                    change=False
                x=int((x+26)/2)
            int_to_char[i]=x
        return (chr(int_to_char[0])+chr(int_to_char[1])+chr(int_to_char[2])+chr(int_to_char[3])+chr(int_to_char[4])+chr(int_to_char[5])+chr(int_to_char[6])+chr(int_to_char[7]))## end of thread1, to get startof thread2 just add to the ascii +1


if __name__=="__main__":
    pz = Patzhan()
    pz.reconnect()
