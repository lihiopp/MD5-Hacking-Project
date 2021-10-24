password = ['A','A','A','A','A','A']
for p1 in range(26):
    ch1 = ord(password[0]) + p1
    for p2 in range(26):
        ch2 = ord(password[1]) + p2
        for p3 in range(26):
            ch3 = ord(password[2]) + p3
            for p4 in range(26):
                ch4 = ord(password[3]) + p4
                for p5 in range(26):
                    ch5 = ord(password[4]) + p5
                    for p6 in range(26):
                        ch6 = ord(password[5]) + p6
                        print(chr(ch1), chr(ch2), chr(ch3), chr(ch4), chr(ch5), chr(ch6))
                        
                        
