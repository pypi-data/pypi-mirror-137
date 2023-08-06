#contains my classes for my pip
from datetime import date

class charCheck:
    default = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    def messyCheck(inpfile):
        global default
        if(default == ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']):
            inpfile = inpfile.lower()
        for i in default:
            if i not in inpfile:
                return "First to fail: "+str(i)
        return 'All items in file.'

    def inputOwn():
        global default
        default = input('Enter each item you wish to search for, seperated by spaces: ')
        if(default == ''):
            default = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        else:
            default = default.split(' ')

class dateCalc():
    def checkDate(dateToCheck):
        today = date.today()
        today = str(today).split('-')
        bases = dateToCheck.split('/')
        yeardif = int(bases[0]) - int(today[0])
        if yeardif != 0:
            yeardif = yeardif * 365.25
        monthdif = int(bases[1]) - int(today[1])
        if monthdif != 0:
            monthdif = monthdif * 30.416
        daydif = int(bases[2]) - int(today[2])
        var = round((daydif+monthdif+yeardif),0)
        return str(int(var)) 

    x = 1/1/1
    while x != '':
        x = input('enter a date in year/month/day format: ')
        print(str(x)+' is '+str(checkDate(x))+' days away.')