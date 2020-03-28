# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as BS
import time
import smtplib
import threading


class CURRENCY():
    DollarRub = "https://www.google.com/search?sxsrf=ALeKk02fgf59mruV4QLACGUX1ca5K5CYCg%3A1584906851515&ei=Y8J3Xu7_HsqLmwWAv4vACQ&q=dollar+to+rub&oq=dolla&gs_l=psy-ab.1.0.0i67l3j0i131i67j0i131i20i263j0i67l2j0i131l2j0i67.4877.6293..8083...0.1..0.178.780.0j5......0....1..gws-wiz.......0i71j35i39j0.MJvTEu-saoo"
    Headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    
    cur_converted_value = 0
    PAUSE = 30 * 60 # 30 minutes by it may be customized while app's running
    
    def __init__(self, difference= 3):
        self.cur_converted_value = float(self.CHECK())
        #by default difference is 3rub, but it may be customized as user need
        self.DIF = difference
        self.date = str(time.ctime())
        
    
    def CHECK(self):
        try:
            self.full_page = requests.get(self.DollarRub, headers=self.Headers)
        except requests.exceptions.ConnectionError:
            print("Check your internet connection")
            print("Will continue working in 10 minutes if connection's ready")
            time.sleep(10 * 60)
            print("Hope conection is all right")
            self.CHECK()
                
        soup = BS(self.full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class":"DFlfde SwHCTb", "data-precision":"2"}) 
        return str(convert[0].text).replace(",", ".")
    
        
    def value_out(self):
        currency = float(self.CHECK())
        
        #Here is warning about changes >= difference
        design = "-" * 100
        if currency >= self.cur_converted_value + self.DIF:
            print("!!! WARNING !!!")
            print("Big fall of ₽")

            t_dif = currency - self.cur_converted_value
            additional_text = "Watch out for $/₽ jumps/falls!\n\n  Since {} price for 1$ has grown by {}₽.\n  For now 1$ equals {}₽\n\n{}\n If you wish to be informed about less or more significant changes in currency\nREPLY to this email and describe size of changes you'd prefer to know about".format(self.date, t_dif, currency, design)
            additional_text = ''.join(additional_text)#.encode('utf-8')
            fall = "-- Big fall of ₽"
            
            self.SEND(additional_text, fall)
            
            self.cur_converted_value = currency
            self.date = str(time.ctime())
            
        elif currency <= self.cur_converted_value - self.DIF:
            print("!!! WARNING !!!")
            print("Big jump of ₽")
            
            t_dif = self.cur_converted_value - currency
            additional_text = "Watch out for $/₽ jumps/falls!\n\n  Since {} price for 1$ has fallen by {}₽.\n  For now 1$ equals {}₽\n\n{}\nIf you wish to be informed about less or more significant changes in currency reply to this email and describe size of changes you'd prefer to know about".format(self.date, t_dif, currency, design)
            additional_text = ''.join(additional_text)#.encode('utf-8')
            jump = "-- Big jump of ₽"
            
            self.SEND(additional_text, jump)
            
            self.cur_converted_value = currency
            self.date = str(time.ctime())
            
        soup = BS(self.full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class":"DFlfde SwHCTb", "data-precision":"2"})
        
        print("-" * 10)
        print(time.ctime())
        print("for now")
        print("1$ equals", str(currency).replace(".", ",") + "₽")
        print()
        print()
        print('Write keyword "Settings" to custom pause between checking currency and value of jumps/falls on that wich you wanna know about')
        print()
        
        
        time.sleep(self.PAUSE)
        self.value_out()

        
        
        
    def SEND(self, text, sub):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        #write your mail adress here  and  put the password that you get from google
        server.login("ix2.evdokimov@gmail.com", "rtcbevadisynmtxg")
        
        #pripare message to warn you about currensy changings 
        subject = "!Currency" + sub
        body = text
        message = 'Subject:{}\n\n{}'.format(subject, body)
        
        server.sendmail("ix2.evdokimov@gmail.com", ["ix2.evdokimov@gmail.com", "i_a_evdokimov@gmail.com", "fedor.ig.evdokimov@gmail.com", "gumbin.maksim@yandex.ru"], message)
        
        server.quit()
        
        
    
    def SETTINGS(self):
        print()
        print()
        print("Settings now: dif={}, pause={}".format(self.DIF, self.PAUSE))
        #print("If you want to change the value of difference to be monitored\nwrite it here (if you don't but you wanna change other options write 0 to continue customization)")
        #print("If you want to change the value of difference to be monitored\nwrite it here, press ENTER to continue customization") 
        print("New difference to be monitored:  (press ENTER to continue customization)")
        resp = input()
        if resp:
            self.DIF = float(resp)
            print("Sucessfully chaged")
            print()
        #print("If you want to change the time of pause time\nwrite it here in seconds (if you don't but you wanna change other options write 0 to continue customization")
        #print("If you want to change the time of pause time\nwrite it here in seconds, press ENTER to end customization")
        print("New pause beetween checking currency:  (press ENTER to end customization)")
        resp = input()
        if resp:
            self.PAUSE = float(resp)
            print("Sucessfully chaged")
            print()
            
        print("Customized")
        
        
    def call_customizing(self):
        response = input()
        if response == "Settings":
            self.SETTINGS()
        
        self.call_customizing() 

            
        
            
        

    
start_app = CURRENCY()
run = threading.Thread(target= start_app.value_out)
change = threading.Thread(target= start_app.call_customizing)

run.start()
change.start()
