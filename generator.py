import time

def gen(start,stop):
    while start<=stop:
        print(start)
        index=1
        time.sleep(0.1)
        if chr(ord(start[-index])+1)<='z':
            start=start[:-1]+chr(ord(start[-index])+1)
        else:
            while start[-index]=='z':
                index=index+1
            start=start[:len(start)-index]+chr(ord(start[-index])+1)+((index-1)*'a')
gen('abhjtdfh','zzzheslz')
                                


        
