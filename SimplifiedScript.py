#Initialise Imports
import string,random; # for string and Random number related operations
import pandas as pd; # for data Frames
import numpy as np; # for numerical computations
import re; # regular expression

#for Autoamtion related purpose
from selenium import webdriver ;
from selenium.webdriver.common.keys import Keys;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as ec;

from selenium.webdriver import ActionChains

# for Time related operations
import time;
import datetime;

# function to write data frame to Excel file 
def WriteExcel(df):
    writer = pd.ExcelWriter(r'C:\Users\vaibhao12320\Desktop\PyProj\Amazon Automation\Database.xlsx', engine="xlsxwriter");
    df.to_excel(writer, sheet_name='Task')
    writer.save()
	
	
#Chrome Drivers initialisation
chrome_path = r'E:\chromedriver_win32\chromedriver.exe';
driver = webdriver.Chrome(chrome_path);
driver.maximize_window();
#Action Chains instantiate
actionChains = ActionChains(driver)
time.sleep(1)


# get Url :
driver.get('https://www.amazon.in')
time.sleep(1)


# getting data from database
BrandList = pd.read_excel(r'C:\Users\vaibhao12320\Desktop\PyProj\Amazon Automation\Database.xlsx', 'Database')
Task = pd.read_excel(r'C:\Users\vaibhao12320\Desktop\PyProj\Amazon Automation\Target.xlsx', 'Task')



#adding stemming function 
def Stem (sentense):
    words = sentense.encode('utf-8').split(' ')
    for text in words:
        if text not in [brands for brands in BrandList['Brands']]:
            #the word is not a brand requires stemmer check
            for suffix in ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 's', 'ment']:
                if text.endswith(suffix):
                    #replace  the word with stemmed word
                    words[words.index(text)] = text[ : -len(suffix)]                 
    return ' '.join(words)
	
	
	
# executing the Task one by one 
for task in Task['Task']:
    print task
    if Execute(task) == "Success": # if the execution returns success then Update the Results colum wit Pass or else Fail 
        Task['Result'][Task['Task'][ Task['Task']== task].index.tolist()] = "Pass"
        #Task.set_value(1,Task['Result'],"Pass")
        #Task.set_value(1,'Result',"Pass")
    else:
        Task['Result'][Task['Task'][ Task['Task']== task].index.tolist()] = 'Fail'
       
	   
	   
	   
def Execute(task, operation = 'cart', Brands = set([]),price = []): #Add all the asus and dell laptops below 22000 to cart
    task = Stem(task) #Add all the asus and dell laptop below 22000 to cart
    print task
    
    # finding the Operation required to be performed
    regexps = [re.compile(p) for p in ['cart','whishlist','buy']]
    for regexp in regexps:
        #print regexp
        if regexp.search(task):
            operation = regexp.pattern
    
    # Identifying the varios brands in the Task
    regBrands = [re.compile(p) for p in map(str,(BrandList['Brands'].values.reshape(1,len(BrandList['Brands']))[0]))]
    for br in regBrands:
        if br.search(task,re.IGNORECASE):
            Brands.add(br.pattern)
    print Brands 
    if not re.search('^[below|above|lower than|more than|greater than|smaller than]',task):
        price = re.findall('[0-9]+', task)
    print price
    
    #task = task.lower().split(' '); #['add','all', 'the', 'asus','and','dell', 'laptop',' below', '22000', 'to', 'cart']
    
    
    del(Brands);
    return 'Success'
