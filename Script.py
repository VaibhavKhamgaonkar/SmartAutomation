#Initialise Imports
import string,random; # for string and Random number related operations
import pandas as pd; # for data Frames
import numpy as np; # for numerical computations

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
	#----------------------------************************-------------------------
	
#Chrome Drivers initialisation
chrome_path = r'C:\Users\vikas\Downloads\chromedriver_win32\chromedriver.exe';
driver = webdriver.Chrome(chrome_path);
driver.maximize_window();
#Action Chains instantiate
actionChains = ActionChains(driver)
time.sleep(2)	
	#----------------------------************************-------------------------
#opening URL 
driver.get('https://www.amazon.in')
time.sleep(1)
#----------------------------************************-------------------------

# Task to be performed
Task = "add all the asus laptops below 22000 to cart"
'''"add all the Asus laptop between 20000 to 22000 to cart"
"Add an Asus X540YA-XO106D, Asus X540LA-XX596D, HP 15-AU003TX laptop, HP Pavilion 15-au620TX, Mi 10000mAH Power Bank 2 (Black) and Samsung On7 Pro (Gold) mobile to Cart "'''
#----------------------------************************-------------------------

#adding stemming function 
def Stem (sentense):
    words = sentense.split(' ')
    for text in words:
        if text not in BrandList:
            #the word is not a brand requires stemmer check
            for suffix in ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']:
                if text.endswith(suffix):
                    #replace  the word with stemmed word
                    words[words.index(text)] = text[ : -len(suffix)]                 
    return ' '.join(words)
#----------------------------************************-------------------------

# Creating DB for various activities 
ProductList = ['power bank', 'mp3','dvd','laptop','mobile', 'phone','music player','head phone','headset','charger']
# Creating a Brand List
BrandList = ['asus', 'samsung', 'lenovo','toshiba','sony','dell']
#----------------------------************************-------------------------
#identify single item or multiple items

#--------------------------- product to be added in certain range or min or max range

def SingleMultipleCheck (task,driver):
    #pass the Task through Stemmer first
    task = Stem(task)
    #now perform split and create a list
    item =  task.lower().split(' ')
    #Identify the Type of operation t obe performed
    if 'cart' in item:
        operation = 'cart'
    elif 'wishlist' in item:
        operation = 'wishlist'
    else:
        operation = 'buy'
    
    #print item
    #verifying Multiple products scenarios
    if ('all' in item and item[item.index('all')+1] == 'the') and  ('below' in item or 'greater than' in item or 'above' in item or 'less than' in item):
        print 'multiple Product'
        Task1 = ' '.join(item[item.index([brand for brand in item if brand in BrandList][0]) : item.index('to')])
        print Task1
        # idenifying the min or max range of the product
        if 'below' in Task1 :
            maxValue = Task1.split('below')[1]
            minValue = 0
        elif 'less than' in Task1:
            maxValue = Task1.split('less than')[1]
            minValue = 0
            #print maxValue
        elif 'above' in Task1 :#or 'greater than' in Task1 or 'more than' in Task1:
            minValue = Task1.split('above')[1]
            maxValue = 0
        elif 'more than' in Task1:
            maxValue = Task1.split('more than')[1]
        
        elif 'greater than' in Task1:
            maxValue = Task1.split('greater than')[1]
            minValue = 0
            
        #calling the function to Add the Product of relevant Range to cart/Wishlish
        ProductRange(Task1,minValue, maxValue,driver,operation)   
        
    #products in the Range  
    elif ('all' in item and item[item.index('all')+1] == 'the') and ('between' in item or 'range' in item):
        print 'multiple Product of between range found'
        Task1 = ' '.join(item[item.index([brand for brand in item if brand in BrandList][0]) : item.index(item[-1])-1])
        # min and max values i.e products to be found out between some range
        maxValue = Task1.split(' ')[-1]
        minValue = Task1.split(' ')[-3]
        #Correctly min and max values if order is revered
        if long(minValue) >= long(maxValue):
            maxValue = long(maxValue) + long(minValue)
            minValue = long(maxValue) - long(minValue)
            maxValue = long(maxValue) - long(minValue)
        #calling Function to Add tyhe products between some range
        ProductRange(Task1,minValue, maxValue,driver,operation)
       
    # if mulitple products to be added are mentioned in the task     
    elif (np.count_nonzero( brand ) for brand in item if brand in BrandList) > 1:
        #print 'multiple Product found for brand'
        Task1 = ' '.join(item[item.index([brand for brand in item if brand in BrandList][0]) : item.index('to')]).replace('and',',') # this will filter out the multiple products 
        #print Task1
        #creating the pandas Series  for adding items to cart.
         #print pd.Series((Task1.split(',')))
        AddMultipleProduct(pd.Series((Task1.split(','))), driver)
        
    else:
        print 'single product'
        #Identify the item and perform the relavant action
        Identification(Task,driver)
#----------------------------************************-------------------------    

# Creating a function to Add products between certain range
# Add Products in certain range
def ProductRange(item, minValue, maxValue, driver,operation): # operation variable id to perform cart or whishlist operation
   # Filtering the Search text
    if 'between' in item : 
        searchText = item.split('between')[0].strip()
    elif 'range' in item:
        searchText = item.split('range')[0].strip()
    elif 'below' in item:
        searchText = item.split('below')[0].strip()
    elif 'less than' in item:
        searchText = item.split('less than')[0].strip()
    elif 'more than' in item:
        searchText = item.split('more than')[0].strip()
    elif 'greater than' in item:
        searchText = item.split('greater than')[0].strip()
    elif 'above' in item:
        searchText = item.split('above')[0].strip()
    else:
        pass
    main_window = driver.current_window_handle;
    #Identifying seach location
    elements_input = driver.find_elements_by_tag_name('input')
    elements_input[1].clear()
    elements_input[1].send_keys(searchText) # Searching the Product
    elements_input[0].submit()
    try:
        assert searchText in driver.page_source # verifying the product on search screen
    except:
        print("your product is not availble into the list. Please refine the Search")
        exit();
    
    #---------------------------------- filtering min and max values based on range provided
    #finding the location of min - max Range field
    driver.find_element_by_id('low-price').clear()
    driver.find_element_by_id('low-price').send_keys(minValue)
    
    driver.find_element_by_id('high-price').clear()
    driver.find_element_by_id('high-price').send_keys(maxValue)
    #Click on Go button 
    driver.find_element_by_xpath("""//input[@class ='a-button-input'][@value = 'Go']""").click()
    
    #wait untill result is on the page
    WebDriverWait(driver,4).until(ec.presence_of_element_located((By.XPATH,"//*[@id='s-result-count']")))
    
    #Print the  Results obtained
    results = driver.find_element_by_xpath("""//*[@id='s-result-count']""").text
    if 'of' in results:
        showingResults = results.split('of')[0].split('-')[-1] # results appearing on screen
        maxResults = results.split(' ')[2] # total results found
    else:
        showingResults = results[0:2]
        maxResults = showingResults
    
	#verifying whether next page is required to for addition of the product
    if long(showingResults) <= long(maxResults):
        #print 'only single page to be added'  ----------------------------------------------------- need checking again
        #Now getting all the prodcuts
        elements = driver.find_elements_by_xpath("//a[@title]")
        #searching and adding only the valid product
        for prod in  elements:
            print searchText.split(' ')[0] + ' -:- '+searchText.split(' ')[-1]
            print prod.text
            if (searchText.split(' ')[0] in prod.text.lower() and searchText.split(' ')[-1] in prod.text.lower()):
                driver.execute_script("arguments[0].focus();", prod) # focusing on element using javascript 
                prod.click() #this will open product in new tab
                #print "Wow Clicked on Product"
                #verifying the multipletabs are present or not
                if len (driver.window_handles) > 1:
                    driver.switch_to_window (driver.window_handles[1])
                else:
                    driver.switch_to_window (driver.window_handles[0])
                #Find the Cart button and Click it
                try:
                    WebDriverWait(driver,10).until(ec.presence_of_element_located((By.ID,'add-to-'+ operation +'-button')))
                    driver.find_element_by_id('add-to-'+ operation +'-button').click() # clicking on Cart button
                    WebDriverWait(driver,10).until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT,'Proceed to checkout')))
                    print ("Bingo : added to cart")
                except:
                    print " for this product located at : " + str(driver.find_element_by_xpath(""".//span[@id='productTitle']""").text) + '  cart option is not availble'
                driver.close()
                #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + "w")
                driver.switch_to_window (main_window)
                time.sleep(1)
                print driver.current_url + ' : ' + driver.current_window_handle
        
    else:
        print 'items from next page need to be added'
 #----------------------------************************-------------------------    

#fucntion to add multiple products to Cart
def AddMultipleProduct(prodList, driver):
    for product in prodList:
        print product.strip() + " : to be added Next" 
        ExecuteCart(product.strip(),driver)
        print product + ": Added to cart Successfully "
#----------------------------************************-------------------------

#Task identification Function
def Identification(Task, driver):
    item =  Task.lower().split(' ')
    #filter the important product 
    for brand in item:
        #print brand
        if brand in BrandList:
            print 'Brand Availble'
            #BrandList: 
            product = brand
            break
        else:
            print "Redifine your Search"
            exit()
    if 'buy' in item:
         product = item[item.index(brand) : -1]  # string will not have 'to cart or to wishlist'
    else:    
        product = item[item.index(brand) : -3] 
    # get the string for search
    product = ' '.join(product)
    print 'final product to search is : ', product
    if 'add' and 'wishlist' in item:
 #-------       #perform Wishlist
        ExecuteWishlist(product, driver)
 
    elif 'add' or 'cart' in item:
        #Checking whether it has Multiple items to Add to cart 
	#-----------#perform Adding to Cart Operation
        ExecuteCart(product, driver)

    elif 'add' and 'buy' in item:
        #perform Buying
        ExecuteCart(product, driver)
        
    elif 'compare' in item:
        print "compare Method"
    
    else:
        pass
# ---------------------------------------------------------Task Execution Function-----------------------

# Wishlisht Function
def ExecuteWishlist(item, driver):
    main_window = driver.current_window_handle;
    #Identifying seach location
    elements_input = driver.find_elements_by_tag_name('input')
    elements_input[1].clear()
    elements_input[1].send_keys(item) # Searching the Product
    elements_input[0].submit()
    time.sleep(2)
    try:
        assert item in driver.page_source # verifying the product on search screen
    except:
        print("your product is not availble into the list. Please refine the Search")
        exit();
    #    print 'itemis: '+ item
    #Storing all the search elements and  then filtering the Specific required element  
    elements = driver.find_elements_by_xpath("//a[@href]")
    #filtering the Specified element
    for prod in  elements:
        #print (item).upper() + ' : ' + prod.text.upper().encode('utf-8')
        if (item[0]).upper() in prod.text.upper().encode('utf-8') and (item[1]).upper() in prod.text.upper().encode('utf-8') and (item[2]).upper() in prod.text.upper().encode('utf-8'):
            print (item).upper() + ' : ' + prod.text.upper().encode('utf-8')
            # add Wait
            time.sleep(2)
            #driver.find_element_by_partial_link_text(str(item[3]).upper()).click() # this will open product in new tab
            prod.click() #this will open product in new tab
            #verifying the multipletabs are present or not
            if len (driver.window_handles) > 1:
                driver.switch_to_window (driver.window_handles[1])
            else:
                driver.switch_to_window (driver.window_handles[0])
            #Find the Wishlist button and Click it
		    
            WebDriverWait(driver,3).until(ec.presence_of_element_located((By.ID,'add-to-wishlist-button-submit')))
            driver.find_element_by_id("add-to-wishlist-button-submit").click() # clicking on Cart button
            #WebDriverWait(driver,3).until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT,'Proceed to checkout'))) # not required for Wishlist option
            driver.close()
            '''WebDriverWait(driver,4).until(ec.presence_of_element_located((By.ID,'add-to-wishlist-button-submit')))
            driver.find_element_by_id("add-to-wishlist-button-submit").click() # clicking on Wishlist button'''
            break;
            
# Adding Cart Function-----------------------------------------------
def ExecuteCart(item, driver):
    print item
    main_window = driver.current_window_handle;
    #Identifying seach location
    elements_input = driver.find_elements_by_tag_name('input')
    elements_input[1].clear()
    elements_input[1].send_keys(item) # Searching the Product
    elements_input[0].submit()
    time.sleep(2)#WebDriverWait(driver,4).until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT,item)))	
    try:
        assert item in driver.page_source # verifying the product on search screen
    except:
        print("your product is not availble into the list. Please refine the Search")
        exit();
    #Storing all the search elements and  then filtering the Specific required element  
    elements = driver.find_elements_by_xpath("//a[@title]")
    #filtering the Specified element
    for prod in  elements:
        #print (item).upper() + ' : ' + prod.text.upper().encode('utf-8')
        if (item[0]).upper() in prod.text.upper().encode('utf-8') and (item[1]).upper() in prod.text.upper().encode('utf-8') and (item[2]).upper() in prod.text.upper().encode('utf-8'):
            print (item).upper() + ' : ' + prod.text.upper().encode('utf-8')
            # add Wait
            time.sleep(2)
            #driver.find_element_by_partial_link_text(str(item[3]).upper()).click() # this will open product in new tab
            prod.click() #this will open product in new tab
            print "Wow Clicked on Product"
			#verifying the multipletabs are present or not
            if len (driver.window_handles) > 1:
                driver.switch_to_window (driver.window_handles[1])
            else:
                driver.switch_to_window (driver.window_handles[0])
            #Find the Cart button and Click it
            WebDriverWait(driver,3).until(ec.presence_of_element_located((By.ID,'add-to-cart-button')))
            driver.find_element_by_id("add-to-cart-button").click() # clicking on Cart button
            WebDriverWait(driver,3).until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT,'Proceed to checkout')))
            driver.close()
            #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + "w")
            driver.switch_to_window (main_window)
            time.sleep(1)
            print driver.current_url + ' : ' + driver.current_window_handle
            break;

SingleMultipleCheck(Task,driver)
