#code to Generate the Forename of specific legth
def ForeName(length = 1,forename = ''):
    vowel = list('a e i o u'.split(' '))
    for char in range(length):
        forename = forename + str(random.choice(string.ascii_letters).lower()) + str(vowel [np.random.randint(0,5)])
        
    if len(forename)>15:
        return forename[0:15] #+ str(random.choice(string.ascii_letters).lower())
    else:
        return forename

		
#code to Generate the Surname of specific legth
def Surname(length = 1,surname = ''):
    vowel = list('a e i o u'.split(' '))
    for char in range(length):
        surname = surname + str(random.choice(string.ascii_letters).lower()) + str(vowel [np.random.randint(0,5)])
        
    if len(surname)>20:
        return surname[0:20] #+ str(random.choice(string.ascii_letters).lower())
    else:
        return surname

#--------------------------------------------------------code for generating DOB for specific age ----------------	

#more format can be added if required
# for more details (https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)
#this function will give the random date of a birth of a child who is of certain age on specific date.
def DOB (FORMAT = "DD/MM/YYYY", AgeOnDate = str(datetime.datetime.strftime(datetime.datetime.now(), '%d/%m/%Y')), age = 2):
   
    year = random.randint(datetime.datetime.now().year - age , datetime.datetime.now().year);
    
    #below  code will ensure the correct yrs which wil corressponds to proper age 
    if (int(AgeOnDate[-4:]) -year) == age:
        year = year;
    else :
        year = int(AgeOnDate[-4:]) - age;

    #-------- generating the DOB of child 
    # identifying leap year
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                   LeapYrsFlag = "yes";#print("{0} is a leap year".format(year))
            else:
                print("{0} is not a leap year".format(year))
        else:
            LeapYrsFlag = "yes";#print("{0} is a leap year".format(year))
    else:
        LeapYrsFlag = "no";#print("{0} is not a leap year".format(year))
    
#-------------------------------------------------------   
    #generating random Month
    month = random.randint(1, 12);
    
    # Generating random date ad also verifying the leap year day 
    if month == 2 and LeapYrsFlag == 'yes':
        day = random.randint(1, 29);
        
    elif month == 2 and LeapYrsFlag == 'no':
        day = random.randint(1, 28);
        
    elif month in [4,6,9,11]: # if identifying the 30 days months
        day = random.randint(1, 30);
        
    else :
        day = random.randint(1, 31); # rest are 31 days month
    
    # now verifing the Age of child with generated date
    
    #------------------- Day month and year and genrated now forattig them according the requirement
    
    if FORMAT.upper() == "DD/MM/YYYY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%d/%m/%Y'); # DD/MM/YYYY format (%d = 2 digit day, %m = 2 digitt month, %Y = 4 digit year)
        
    elif FORMAT.upper() == "MM/DD/YYYY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%m/%d/%Y');
    
    elif FORMAT.upper() == "MM-DD-YYYY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%m-%d-%Y');
    
    elif FORMAT.upper() == "DD-MM-YYYY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%d-%m-%Y');
    
    elif FORMAT.upper() == "DD-MMM-YYYY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%d-%b-%Y');
    
    elif FORMAT.upper() == "DD/MMM/YYYY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%d/%b/%Y');
    
    elif FORMAT.upper() == "MM/DD/YY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%m/%d/%y');
    
    elif FORMAT.upper() == "MM-DD-YY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%m-%d-%y');
    
    elif FORMAT.upper() == "DD-MM-YY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%d-%m-%y');
    
    elif FORMAT.uuper() == "DD/MM/YY":
        return datetime.datetime.strftime(datetime.datetime(year,month,day) , '%d/%m/%y');
    else:
        return datetime.datetime.strftime(datetime.datetime.now(), '%d/%d/%Y');
    
		
