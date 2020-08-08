from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import urllib
import openpyxl
import os
import random

#Written in Python 3.8
#Written By Eric Byam @therealericny

#Randomizes user agent
ua = UserAgent()
userAgent = ua.random 
print(userAgent)

#Chrome Options Below
options = webdriver.ChromeOptions()
options.headless = False #Creates a headless browser if true, works better when False
options.add_argument(f'user-agent={userAgent}') #Should randomize the user-agent

Link = input('Copy and Paste the Link of the Comment you wish to send Comment Likes to here: ')
print ('')
#Link of the comment on Instagram we're going to like. #Ask for link of the comment here

def LikeComment(user, passw):
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('https://www.instagram.com/')
    driver.implicitly_wait(10)
    print(userAgent)

    driver.find_element_by_name('username').send_keys(user)
    driver.find_element_by_name('password').send_keys(passw)
    Login = "//button[@type='submit']"
    sleep(2) #Sometimes problem logging in, might do a while loop for NoSuchElementException
    driver.find_element_by_xpath(Login).submit()
    sleep(1)
    #Logs into Instagram
    print ('Logged In')

    NotNow = "//button[contains(text(),'Not Now')]"
    driver.find_element_by_xpath(NotNow).click()
    #Clicks Pop Up
    print ('Close Pop Up')

    driver.get(Link)
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span/div/button/div[*[local-name()='svg']/@aria-label='Like']"))) #May change overtime
    #Correct xpath was created by writing the 3 element sections before the main section which was local name 'svg' and including an astribute that was in 'svg'
    element.click()
    print ('Likes Comment')
    driver.quit() #Changed to quit instead of close() to avoid all the boxes opening up

#-----Extracting Usernames and Passwords from an Excel Sheet Below-----

#print ("Example Paste As Is: r'C:\Users\John Doe\Desktop\IG Acc for Comment Likes.xlsx'")
print ('')
inputdirectory = input("Please type in the full path of the folder containing your files:    ")
print ('')
print ('Example Should Look Like This: IG Acc for Comment Likes.xlsx')
inputfileextensions = input("Please type in the file name with extension of your files:    ")
pathToExcel = os.path.join(inputdirectory, ""+inputfileextensions)
print (pathToExcel)
#pathToExcel = input('Paste the path of your Excel/SpreadSheet containing all of your account(s) information: ')
#ATTENTION - User should be able to input excel sheet path


#Ask for excel sheet here inside of a while loop along with the amount of accounts equaling or less than amount of likes asked for
wb_obj = openpyxl.load_workbook(pathToExcel)
sheet_obj = wb_obj.active



#--------------------------------------------------------------------
#While loop for likes being sent below using excel sheet
Accounts = sheet_obj.max_row
Accounts -= 1 #This is to reflect the accuracy of accounts in the excel sheet
#              and omit the first row being Username and Password

#-----------------------Randomize Accounts being Used to Login for Likes----------------------

TheUser = []
ThePass = []

sh = wb_obj["Sheet1"]
for cell in sh['A'][1:]:
    TheUser.append(cell.value) #Adds all usernames to list TheUser; [1:] Makes it so the first rowis omitted

for cell in sh['B'][1:]:
    ThePass.append(cell.value) #Adds all usernames to list ThePass; [1:] Makes it so the first rowis omitted

temp = list(zip(TheUser, ThePass))
random.shuffle(temp)
UserVault, PassVault = zip(*temp) #Two New list were created and randomize with usernames and passwords being the same index

#----------------------------------------------------------------------

print ('Total Amount of Comment Likes available: ', Accounts)
Likes = int(input('How many likes would you like to send: '))
while Likes > Accounts:
    print ('Not enough accounts. Enter an accurate amount')
    Likes = int(input('How many likes would you like to send: '))

LikeSent = 0
while LikeSent < Likes:
    print ('Using Account: ', UserVault[LikeSent]) #just added
    LikeComment(UserVault[LikeSent], PassVault[LikeSent])
    #print (usernames) was here first
    LikeSent += 1
    print ('Likes Sent: ', LikeSent)
    print ('')
    
    



