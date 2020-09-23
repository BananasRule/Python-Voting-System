#A python two vote voting system based on a Computer Science task 
#Takes two votes for a number of voters for a number of candidates and tallies winner
#Created by BananasRule (Github)
#Check licencing before using, adapting, modifying or distrubuting this code
#Licensing can be found here https://github.com/BananasRule/Python-Voting-System/tree/master
#The code is licenced under Creative Commons Attribution 4.0 International Public License
#It can also be found here https://creativecommons.org/licenses/by/4.0/legalcode


#Import dependancies 
import os, hashlib, secrets, platform

#####################################################################
#####################################################################
#####################################################################
#Initilise variables (Changable)
#Change variables below

#Number of eligable voters
eligablevoters = 317

#Names of candidates 
#Formatting
#Insert name between brackets with '' around the name and a comma afterwards (except for last item)
#e.g. ['Generic', 'Generic2']
candidates = ['Boatie Mac Boatface', 'Bouyonce', 'Pride of Ratentango', 'Black Pearl']

#Set weighting of prefernces
#First preferance 
firstprefweight = 3
#Second preferance 
secondprefweight = 1

#Don't change things past here unless your know what you are doing or are BananasRule (Author)
######################################################################
######################################################################
######################################################################

#Initilise variables (Don't Change)
#Initalise counter
points = [0]*len(candidates)
#Set voting to True
votingongoing = True
#Set voter counter to 0
voters = 0
#Create encryption salt using secure OS random generator
salt = secrets.randbits(64) 

#Check system os
ossystem = platform.system()
#Sets terminal clear command to be comaptable with different host OS 
#Makes it compatbile with linux intergrated systems
if ossystem == 'Windows':
    clearcommand = 'cls'
else:
    clearcommand = 'clear'

#Function to find candidate name from their value (position on list)
def candidatename(candidatevalue):
    return(candidates[candidatevalue])

#System initiallisation function
def initialise():
    #Set password variable to use global variable
    global password
    #Clear current text on terminal 
    os.system(clearcommand)
    #Preamable 
    print("Welcome to the Gensis polling system, operator")
    print("In order to prevent abuse please enter a secret password")
    print("When prompted to enter a first preferance enter the operator password to access operator mode")
    print("From operator mode you can end voting and see current votes")
    #To enter operator mode enter the password when asked for first preferance 
    #Used to improve user flow so users aren't asked of they are operators after every vote becuase there are many more users than opertors

    #Hashed and Salted password of operator
    #Input in hashing algorthim to miminise time of unhashed password
    #The hash uses 500,000 iterations of SHA 512 with a secure random salt (diffrent each run) to generate a secure and unique hash of passwords
    password = hashlib.pbkdf2_hmac('sha512', input("Input operator password: ").encode('utf-8'), salt.to_bytes(64,'big'), 500000)
    #Confimation
    print("Password successfuly set")
    #Wait for operator to enter voting mode
    input("Press enter to begin voting")



#Function that is called when you enter operator mode
#Asks to end voting
def operatormode():
    #Change global variable 
    global votingongoing
    #Clear terminal
    os.system(clearcommand)
    #Asks to continue voting
    print("Has voting finished? (Y/N)")
    #Error check input
    while True:
        #Get input
        officalresponce = input()
        #Lower responce to ignore captial letters
        officalresponce = officalresponce.lower()
        #Check what responce was given
        if officalresponce == 'y':
            #End voting by changing variable
            votingongoing = False
            break
        elif officalresponce == 'n':
            #Ignore
            break
        else:
            #Invalid input
            print("Invalid input. Please enter 'Y' or 'N' to indicate responce.")

#Main function that handles voting
def voting():

    #Set up function variables
    firstselection = ""
    operatorauthed = False
    #Use global variables
    global voters, votingongoing
    votingongoing = True
    #Checking that voting has not ended
    while votingongoing == True: 
        os.system(clearcommand)
        #Initial message for each voter
        print("Welcome to the Ratentango polling software")
        print("You are voter " + str(voters + 1) + "\n")
        print("The candidates for boat name are: \n")
        #Goes through candiates list and print name and number
        for candidatecounter in range(len(candidates)):
            print(str(candidatecounter + 1) + ". " + candidates[candidatecounter])
        #Gives dynamic example and instructions
        print("\nPlease select a candidate for first prefrence by entering their number (i.e. Enter 2 to vote for " + candidates[1] + ")")
        #Takes first selection
        firstselection = input()
        #Error checking
        while True:
            try:
                #Checks to see if it is the operator password
                if hashlib.pbkdf2_hmac('sha512', firstselection.encode('utf-8'), salt.to_bytes(64,'big'), 500000) == password:
                    #Auths Operator
                    operatorauthed = True
                else:
                    #Checks that number in interger and is an candidate
                    firstselection = int(firstselection) - 1
                    candidates[firstselection]
                break
            except:
                #If it fails it re-requests selection and asks for new input
                print("Invalid Input. Please re-enter your selection")
                firstselection = input()
        #Checks that operator is authed and rechecks hash to ensure variable has not been changed manually 
        if operatorauthed == True and hashlib.pbkdf2_hmac('sha512', firstselection.encode('utf-8'), salt.to_bytes(64,'big'), 500000):
            #Opens operator mode
            operatormode()
        else:
            #Adds points to selected candidate based on weighting
            points[firstselection] = points[firstselection] + firstprefweight
            #Voter counter increases
            voters = voters + 1
            #Confims Vote and asks for second preferance
            print("Thank you. Your first preferance for " + candidatename(firstselection) + " has been recorded.")
            print("Please select a candidate for second prefrence by entering their number (i.e. Enter 2 to vote for " + candidates[1] + ")")
            while True:
                try:
                    #Checks that number in interger and is an candidate
                    secondselection = int(input()) - 1
                    candidates[secondselection]
                    #Checks second selection is not same as first
                    if firstselection == secondselection:
                        print("Invalid Input. Second selection is the same as first. Please make a different selection.")
                    else:
                        break
                except:
                    #If it fails it re-requests selection and asks for new input
                    print("Invalid Input. Please re-enter your selection")
            #Adds points to selected candidate based on weighting
            points[secondselection] = points[secondselection] + secondprefweight
            #Confims Vote and displays voter totals
            print("Thank you. Your second preferance for " + candidatename(secondselection) + " has been recorded.")
        #Check if all voters have voted
        if voters >= eligablevoters:
            votingongoing = False

#Function I created to find locations of elements in lists (element is elemet you want to find (any type), list is list you want to find element in (list type))
def elementfinder(element, list):
    #Initilises local variables
    listofelements = []
    liststagecounter = 0
    #Checks each element in list against searching element
    for listelement in list:
        if element == listelement:
            #If found appends search list value to list
            listofelements.append(liststagecounter)
        liststagecounter = liststagecounter + 1
    #Returns list containing elements
    return(listofelements)

#Main function to tally preferances 
def tally():
    #Clear terminal
    os.system(clearcommand)
    #Creates sorted list of points
    sortedpoints = sorted(points, reverse=True)
    #Uses elementfinder() to search unsorted points list for highest score
    winnerid = elementfinder(sortedpoints[0], points)
    #Check number of items
    if len(winnerid) == 1:
        #Not a tie (Not more than one)
        #Uses candidatename() function to find candiate name
        winner = (candidatename(winnerid[0]))
        #Prints winner
        print("The winner is " + winner + ".")
        #Caculates percentage of wins
        #Works out total votes cast based on number of voters times total preferance weights
        totalvotescast = voters * (firstprefweight + secondprefweight)
        #Caculates pecentage
        winningpecent = sortedpoints[0] / totalvotescast * 100
        #Round to 2dp
        winningpecent = round(winningpecent, 2)
        #Print pecentage
        print("With " + str(winningpecent) + "% of the votes")
        print(str(voters) + " voters voted")
    
    elif len(winnerid) == 0:
        #If there has been no votes recorded
        #I can already see this being a test :)
        print("No votes recorded")

    else:
        #Tie or zero votes (More than one winner)
        totalvotescast = voters * (firstprefweight + secondprefweight)
        #Works out total votes cast based on number of voters times total preferance weights
        #Checks to see if no votes were cast 
        if totalvotescast == 0:
            #If no votes cast displays no votes cast
            print("No votes cast")
        else:
            #If tie
            #Caculates pecentage
            winningpecent = sortedpoints[0] / totalvotescast * 100
            #Round to 2dp
            winningpecent = round(winningpecent, 2)
            #Announce tie
            print("There is a tie between:")
            #Print list of winners
            for id in winnerid:
                print(candidatename(id))
                #Print tied percentage
            print("With " + str(winningpecent) + "% of the votes")
            print(str(voters) + " voters voted")
    #Wait for input to exit
    input("Press enter to exit")
    
    
#Main code
#Calls functions above
initialise()
voting()
tally()
