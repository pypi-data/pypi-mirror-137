#contains my classes for my pip

class wordCheck:
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