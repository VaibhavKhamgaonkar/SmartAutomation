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

		
		
		