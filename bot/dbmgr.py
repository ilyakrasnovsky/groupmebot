'''
module : dbmgr

features firebase wrapper class called Dbmgr

'''

from firebase import firebase
from requests import HTTPError
from django.conf import settings

#import localcreds

'''
class: Dbmgr

description:
    - database manager class

attributes:
    fdb : instance of the FirebaseApplication class    

initializer input:
    None

functions:
    addUser()
    getUser()
    removeUser()
    addMessage()
    getMessage()
    removeMessage()
'''

class Dbmgr():
    def __init__(self):
        #Authentication 
        FIREBASE_URL = settings.FIREBASE_URL #"https://groupmebot-4104f.firebaseio.com/" 
        FIREBASE_KEY = settings.GROUPMEBOT_FIREBASE_SECRET_KEY #localcreds.get_credentials(firebase=True) 
        authentication = firebase.FirebaseAuthentication(FIREBASE_KEY, 'ilyakrasnovsky@gmail.com', admin = True)
        self.fdb = firebase.FirebaseApplication(FIREBASE_URL, authentication=authentication)

    '''
    function: addUser()

    description:
        -Adds a groupMe user to the database from a dictionary
        of values

    inputs: 
        username : A string of username

    outputs:
        status : True if addition was successful,
                False if name of offender already taken,
                "ERROR" (string) in the case of connection
                issue or authentication problem.
    '''
    def addUser(self,username):
        isPresent = self.getUser(username)
        if (isPresent == None):
            try:
                self.fdb.put('/users/', username, {"messages" : [""]})
                return True
            except HTTPError:
                return "ERROR"
        elif (isPresent == "ERROR"):
            return "ERROR"
        else:
            return False

    '''
    function: getUser()

    description:
        -Searches for a user in the database from a name,
        DEFAULT gets all users

    inputs: 
        username : name (string) of a user to look for (optional, if None,
            returns all users)

    outputs:
         If found, returns dictionary representing an user
         (or dictionary of dictionaries of many users by name
            if name was None, None if not found, and "ERROR" if 
                connection/authentication issue)
    '''
    def getUser(self,username=None):
        try:
            return self.fdb.get('/users/', username)
        except HTTPError:
            return "ERROR"

    '''
    function: removeUser()

    description:
        -Removes an offender from the database by name

    inputs: 
        username : name (string) of offender to delete
        
    outputs:
        status : True if delete was successful,
                False if selected offender not in database,
                "ERROR" (string) in the case of connection
                issue or authentication problem.
    '''
    def removeUser(self, username):
        isPresent = self.getUser(username)
        if (isPresent != None):
            try:
                self.fdb.delete('/users/', username)
                return True
            except HTTPError:
                return "ERROR"
        elif (isPresent == "ERROR"):
            return "ERROR"
        else:
            return False

    '''
    function: addMessage()

    description:
        -Adds a message (string) to the database.

    inputs: 
        username: a string of user name
        message : a string of the message to be added

    outputs:
        status : True if addition was successful,
                False if name of word already taken,
                "ERROR" (string) in the case of connection
                issue or authentication problem.
    '''
    def addMessage(self, username, message):
        isPresent = self.getUser(username)
        if (isPresent != None):
            try:
                isPresent['messages'].append(message)
                self.fdb.patch('/users/' + username, isPresent)
                return True
            except HTTPError:
                print ("wtf")
                return "ERROR"
        elif (isPresent == "ERROR"):
            return "ERROR"
        else:
            temp = self.addUser(username)
            if (temp != "ERROR"):
                self.addMessage(username, message)
                return True

    '''
    function: getCrassWord()

    description:
        -Searches for a crass word in the database from a name,
        DEFAULT gets all crasswords

    inputs: 
        word : name (string) of crassword to look for (optional, if None,
            returns all crasswords)

    outputs:
         If found, returns the crassword
         (or dictionary of many crasswords by name
            if name was None, None if not found, and "ERROR" if 
                connection/authentication issue)
    '''
    def getCrassWord(self, word=None):
        try:
            return self.fdb.get('/crasswords/', word)
        except HTTPError:
            return "ERROR"

    '''
    function: removeCrassWord()

    description:
        -Removes a crassword from the database by name

    inputs: 
        word : name (string) of crassword to delete
        
    outputs:
        status : True if delete was successful,
                False if selected crassword not in database,
                "ERROR" (string) in the case of connection
                issue or authentication problem.
    '''
    def removeCrassWord(self, word):
        isPresent = self.getCrassWord(word)
        if (isPresent != None):
            try:
                self.fdb.delete('/crasswords/', word)
                return True
            except HTTPError:
                return "ERROR"
        elif (isPresent == "ERROR"):
            return "ERROR"
        else:
            return False
    
#Tester client
def main():
    dbmgr1 = Dbmgr()
    
    status = dbmgr1.addUser("ilya")
    print ("dbmgr1.addUser(ilya) status : " + str(status))
    
    status = dbmgr1.addUser("dorothy")
    print ("dbmgr1.addUser(dorothy) status : " + str(status))
    
    status = dbmgr1.addUser("dorothy")
    print ("dbmgr1.addUser(dorothy) (again) status : " + str(status))

    status = dbmgr1.getUser("dorothy")
    print ("dbmgr1.getUser(dorothy) status : " + str(status))
    
    status = dbmgr1.getUser("lol")
    print ("dbmgr1.getUser(lol) status : " + str(status))

    status = dbmgr1.getUser()
    print ("dbmgr1.getUser() status : " + str(status))

    status = dbmgr1.removeUser("ilya")
    print ("dbmgr1.removeUser(ilya) status : " + str(status))

    status = dbmgr1.removeUser("lol1")
    print ("dbmgr1.removeUser(lol1) status : " + str(status))

    status = dbmgr1.getUser("ilya")
    print ("dbmgr1.getUser(ilya) status : " + str(status))

    status = dbmgr1.addMessage("dorothy", "hi")
    print ("dbmgr1.getUser(dorothy, hi) status : " + str(status))

    status = dbmgr1.addMessage("dorothy", "hi")
    print ("dbmgr1.getUser(dorothy, hi) status : " + str(status))

    status = dbmgr1.addMessage("lol", "hi")
    print ("dbmgr1.getUser(lol, hi) status : " + str(status))


if __name__ == '__main__':
    main()