"""Created on Sun Mar 25 00:19:47 2018
@author: pablo
"""
import random
from useful_functions import *

''''''''''''''''''''''''''''''''''''''
'''Parameters High Stress Condition'''
''''''''''''''''''''''''''''''''''''''

'''Number of trials per face (4 faces)'''
numTrials = 40
'''Seed'''
r = 5
random.seed(r) #random seed set up to 5
'''face'''
facesTrials = range(4) #face number ("blocks")
'''trials per image'''
trailsPerImage = range(numTrials)
'''Position books'''
InTargetBooks = [['harry','lord']]*numTrials 
leftPos = []
rightPos = []
for pair in InTargetBooks:
    left, right = random.sample(pair, len(pair))
    leftPos.append(left)
    rightPos.append(right)
'''FeedbackPic'''
feedbackPics = range(numTrials) #list of novel objects
feedbackPic = random.sample(feedbackPics,len(feedbackPics))
   
trials= []
def generateTrials(runTimeVars,runTimeVarOrder):
    addedColumns=['face','leftPos', 'rightPos', 'targetBook', 'feedbackPic', 'soundStress','probRewardB1','probRandomStress', 'expectedKey','trialIndex']
    runTimeVarOrder.extend(addedColumns)
    trialsFile = open('trials/'+runTimeVars['subjCode']+'_trials.csv','w')
    writeToFile(trialsFile,[colName for colName in runTimeVarOrder if colName is not 'gender' and colName is not 'expName'])
    
    try:
        random.seed(runTimeVars['seed']) #set random seed
    except:
        print 'make sure to set the random seed'
    
    #'''if HIGH stress condition'''
    if runTimeVars['condition'] == 'hs':
        '''target book'''
        probBook1 = .6
        probBook2 = .4
        targetBooks = ['book1']*int(numTrials*probBook1) + ['book2']*int(numTrials*probBook2) #prob(book1) = .6 / prob(book2) = .4
        #targetBook = random.sample(targetBooks, len(targetBooks))
        '''Probabilities reward and random stress'''
        probRewardB1 = .6
        probRandomStress = .2 
        '''Stressful sound'''  
        probSound = .2
        probNoSound = .8
        sounds = [1]*int(numTrials*probSound) + [0]*int(numTrials*probNoSound) # prob(display stressful sound) = .2 
        soundStress = random.sample(sounds,len(sounds)) 
        '''if LOW stress condition'''
    elif runTimeVars['condition'] == 'ls':
        '''target book'''
        probBook1 = .8
        probBook2 = .2
        targetBooks = ['book1']*int(numTrials*probBook1) + ['book2']*int(numTrials*probBook2) #prob(book1) = .6 / prob(book2) = .4
        #targetBook = random.sample(targetBooks, len(targetBooks))                
        '''Probabilities reward and random stress'''
        probRewardB1 = .8
        probRandomStress = .2
        '''Stressful sound'''  
        probSound = .1
        probNoSound = .9
        sounds = [1]*int(numTrials*probSound) + [0]*int(numTrials*probNoSound) # prob(display stressful sound) = .2 
        soundStress = random.sample(sounds,len(sounds)) 

    for face in facesTrials: #swap target books according to faces to counterbalance probabilities between book1/book2 and faces1-4
        targetBook = random.sample(targetBooks, len(targetBooks)) #re-do random sample of list of 40 books to change names again
        if face == 0 or face ==1:
            targetBook = [book.replace('book1', 'harry').replace('book2','lord') for book in targetBook]#harry as harry, lord as lord
        elif face == 2 or face == 3:
            targetBook = [book.replace('book1', 'lord').replace('book2','harry') for book in targetBook] #lord as harry, harry as lord

        for i in trailsPerImage:
            if leftPos[i] == targetBook[i]: # book on the left == to target book?
                expectedKey = 'left' # yes: left key expected
            else:
                expectedKey = 'right' #no: right key expected
            trials.append([runTimeVars['subjCode'], str(runTimeVars['seed']), runTimeVars['condition'],face,leftPos[i],
                           rightPos[i],targetBook[i],feedbackPic[i],soundStress[i],probRewardB1,probRandomStress,expectedKey])

    random.shuffle(trials)
    for count, item in enumerate(trials):
        trials[count].append(str(count)) #append trial index 
        print trials[count]
        trialsPrint = ','.join(str(v) for v in item)
        trialsFile.write("%s\n" % trialsPrint)

if __name__ == '__main__':
    #this is what's executed if you run generateTrials.py from the terminal
    generateTrials({'subjCode':'testSubj1', 'seed':'15', 'gender':'male','condition':'hs'}, ['subjCode', 'seed','condition'])    

