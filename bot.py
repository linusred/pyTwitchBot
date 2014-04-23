import time
from time import localtime, strftime
from collections import Counter, defaultdict
import sys
import socket
import string
import urllib2
from random import randint


HOST="199.9.250.229"
PORT=6667
NICK="" #Give your bot a name, it sohuld be the same as thetwitch username you use for your bot
CHANNEL= "" #Give a channel here, it needs to have a "#" in front of it's name example: "#destiny"
readbuffer=""
count = 0
s=socket.socket( )
s.connect((HOST, PORT))
s.send("PASS %s\r\n" % "") #supply your oAuth token here
s.send("NICK %s\r\n" % NICK)
s.send("JOIN %s\r\n" % CHANNEL) 


user = ""
counter = 2
message = ""
users = 0


def find_between( s, first, last ): #This function finds words between characters
 try:
     start = s.index( first ) + len( first )
     end = s.index( last, start )
     return s[start:end]
 except ValueError:
     return ""    
def Quote(user): #This function parses a log file for interesting quotes from a given username
    quotes = []
    choose = ""
    user += ":"
    print user
    text_file = open("Log.txt", "r")
    exists = False
    for line in text_file:
        if user in line and len(line) > 70:
            quotes.append(line)
            exists = True
    if(exists == False):
        text_file.close()
        s.send("PRIVMSG %s\r\n" % (channelog + " : User has no quotes, or they are too general to quote. ;-; Sorry"))
        print "nope"
    else:
        text_file.close()
        choose = quotes[randint(0,(len(quotes)-1))]
        
        s.send("PRIVMSG %s\r\n" % (channelog + " : " + choose))
        choose=string.rstrip(choose)
        choose=string.split(choose)
        length = len(choose)
        print choose
        print (length)

def QuoteTotal(user): #I never bothered to finish this
    quotes = []
    choose = ""
    user += ":"
    print user
    text_file = open("Log.txt", "r")
    exists = False
    for line in text_file:
        if user in line:
            quotes.append(line)
            exists = True
    if(exists == False):
        s.send("PRIVMSG %s\r\n" % (channelog + " : User has no quotes, or they are too general to quote. ;-; Sorry"))
        print "nope"
    else:
        text_file2 = open("user.txt", "w")
        for line in quotes:
            text_file2.write(line)
        text_file2.close()
        choose = quotes[randint(0,(len(quotes)-1))]
        
        choose=string.rstrip(choose)
        choose=string.split(choose)
        length = len(choose)
        print choose
        print (length)

def WordCount(word): #Counts the number of times something has been said in a given log
    print("yes")
    count = 0;
    text_file = open("Log.txt", "r")
    for line in text_file:
        if word in line:
            count += 1
    s.send("PRIVMSG %s\r\n" % (channelog + " : '" + word + "' has been said:" + str(count) + " times since 2013-06-13 16:19:48 in log"))
    return()


while 1:

    readbuffer=s.recv(4096)
    print(str(count) + ":" + readbuffer)


    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )
    for line in temp:

        line=string.rstrip(line)
        line=string.split(line)
        length = len(line)
        if( "PING" in line):
            s.send("PONG %s\r\n" % line[1])
            print ("ping pong ping pong ping pong")

        if "PRIVMSG" in line and ":HISTORYEND" not in line:
            user = find_between(line[0],"!","@")
            message = ""
            counter = 3
            while(counter < length):
                message += line[counter] + " "
                counter += 1
            channelog = line[2]
            print channelog
            print ( strftime("%Y-%m-%d %H:%M:%S", localtime())+ " " + user + message)
            text_file = open("Log.txt", "a")
            
            text_file.write(strftime("%Y-%m-%d %H:%M:%S", localtime())+ " " + channelog + " " + user + message + "\n")
            text_file.close()
        
        if("JOIN" in line):
            users += 1
        if("PART" in line):
            users -= 1
           #Add commands here. My bot is a weird anime maid, yours doesnt have to be.
           #if a word is in a message, do something. You can also add "and user="twitchUSername", 
           #and it will respond only to that specific user.
        if("!status" in message):
            s.send("PRIVMSG %s\r\n" % (channelog + " :Online and ready to serve, my master!"))
            
        if("!time" in message):
            s.send("PRIVMSG %s\r\n" % (channelog + " :" + strftime("%Y-%m-%d %H:%M:%S", localtime()) + " Is the current CST time, my master."))

            
        if("!viewers" in message):
            s.send("PRIVMSG %s\r\n" % (channelog + " : The current number of viewers is: " + str(users) + " users"))
            
        if("!quote" in message): 
            userz = find_between(message,"@","%")
            print message
            if userz.lower() == user.lower():
                s.send("PRIVMSG %s\r\n" % (channelog + " : Arrogant! Don't quote yourself silly."))
            else:
                userz = userz.lower()
                print userz
                Quote(userz)
                
        if("!usertotal" in message): 
            userz = find_between(message,"@","%")
            print message
            if userz.lower() == user.lower():
                s.send("PRIVMSG %s\r\n" % (channelog + " : Arrogant! Don't quote yourself silly."))
            else:
                userz = userz.lower()
                print userz
                QuoteTotal(userz)

        
        if("!comfort" in message):
            user = find_between(message,"@","%")
            s.send("PRIVMSG %s\r\n" % (channelog + " : It's okay " + user + " <3 ;-; linuskun cares about you. Robots feel pain too. I understand you."))

        if("!wordcount" in message): 
            word = find_between(message,"@","%")
            WordCount(word)
        #if("ヽ༼ຈل͜ຈ༽ﾉ" in message):
         #   s.send("PRIVMSG %s\r\n" % (channelog + " : Hey, " + user+ " please don't post that donger shit. It makes us robots fucking hate you. <3"))
    message = ""

         

      

