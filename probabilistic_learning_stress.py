"""
Created on Tue Mar 27 22:47:37 2018
@author: pablo
"""
from psychopy import core, visual, prefs, event
import random
import sys
import copy
from useful_functions import *
from generateTrials import *
from collections import Counter
import winsound

expName='probabilistic_learning_stress_v1'
preFixationDelay = .75
postFixationDelay = .5
stimDuration = 1.0

postSoundDelayCorrect = 0.1
postSoundDelayIncorrect = 1.0
validKeys = ["left", "right"]
booksGame = ["harry","lord"]

posCenter = (0,0)
posBookLeft =(-200,300)
posBookRight =(200,300)
noises = ['stress1', 'stress2', 'stress3', 'stress4', 'stress5','stress6','stress7', 'stress8', 'stress9','stress10']

def initExperiment():

    while True:
        runTimeVarOrder = ['subjCode','seed','gender','condition']
        runTimeVars = getRunTimeVars({'subjCode':'prob_learning_s_101', 'seed':10, 'gender':['Choose', 'male','female','other'], 'condition': ['Choose', 'hs', 'ls']},runTimeVarOrder,expName)
        if runTimeVars['subjCode']=='':
            popupError('Subject code is blank')                
        elif 'Choose' in runTimeVars.values():
            popupError('Need to choose a value from a dropdown box')
        else:
            try:
                outputFile = openOutputFile('data/'+runTimeVars['subjCode'],expName+'_learning.csv')
                if outputFile: #file(s) were able to be opened
                    break
            except:
                popupError('Output file(s) could not be opened')

    generateTrials(runTimeVars,runTimeVarOrder)
 
    (header,trialInfo) = importTrialsWithHeader('trials/'+runTimeVars['subjCode']+'_trials.csv')

    return (header, trialInfo, outputFile)

def showIntroDisplay(pics,trialInfo):

    picInstructions = visual.TextStim(win=win,text="Many great instructions",color=[1, 1, 1], height=25, alignHoriz='center', wrapWidth=900, pos=(0, -300))
    textIntro1 = "In this game you will have to learn the reading preferences of four people. \n\nPress 'j' to continue"
    textIntro2 = "Sometimes they will want to read 'Harry Potter' and sometimes 'Lord of the Rings'. \n\nPress 'k' to continue "
    textIntro3 = "On each round, you will see one of them and the two books. \n\nYour task is to select one of the books for them to read \n\nIn the keyboard, press the left arrow to select the book on the left and the right arrow to select the book on the right \n\nPress 'l' to continue"
    textIntro4 = "If you select the book that they want to read, you will get 1 'like' from them, otherwise, you will get a 'dislike'. \n\nThe more likes you get, the better the prize you will get at the end of the game \n\nA 'like score' will show how many likes you have collected  \n\nIf you finish the game with a negative score, you will get $5 \n\nIf you finish the game with a score of 0 to 40 likes, you will get $10 \n\nIf you finish the game with more than 40 likes, you will get $20 \n\nPress 'p' to continue"
    textIntro5 = "Now, repeat the rules of the game to the researcher. \n\nGet ready to start. \n\nPress 's' to start the game"

    facesName = {}
    for searchFace in trialInfo:
        facesName[searchFace['face']] = searchFace['face']

    positionsFaceIntro = calculateRectangularCoordinates(400,0,4,1)
    positionsBookIntro = calculateRectangularCoordinates(400,0,2,1)
    
    for faceNumber, faceCode in enumerate(facesName.keys()):
        pics[faceCode]['stim'].setPos(positionsFaceIntro[faceNumber])
        pics[faceCode]['stim'].draw()
    picInstructions.setText(textIntro1)    
    picInstructions.draw()
    win.flip()
    moveScreen0 = event.waitKeys(keyList= ['j'])[0]

    if moveScreen0 == 'j':
        for bookNumber, book in enumerate(booksGame):
            pics[book]['stim'].setPos(positionsBookIntro[bookNumber])
            pics[book]['stim'].draw()
        picInstructions.setText(textIntro2)
        picInstructions.draw()
        win.flip()
        moveScreen1 = event.waitKeys(keyList= ['k'])[0]

    if moveScreen1 == 'k':
        pics['0']['stim'].setPos(posCenter)
        pics['0']['stim'].draw()
        #for bookNumber, book in enumerate(booksGame):
         #   picPositionX, picPositionY = positionsBookIntro[bookNumber]
          #  pics[book]['stim'].setPos(picPositionX, picPositionY)
        pics['harry']['stim'].setPos(posBookLeft)
        pics['lord']['stim'].setPos(posBookRight)        
        pics['harry']['stim'].draw()
        pics['lord']['stim'].draw()
        picInstructions.setText(textIntro3)
        picInstructions.draw()
        win.flip()
        moveScreen2 = event.waitKeys(keyList= ['l'])[0]
    
    if moveScreen2 == 'l':
        picInstructions.setText(textIntro4)
        picInstructions.setPos((0,0))
        picInstructions.draw()
        win.flip()
        moveScreen3 = event.waitKeys(keyList= ['p'])[0]
    
    if moveScreen3 == 'p':
        picInstructions.setText(textIntro5)
        picInstructions.setPos((0,0))
        picInstructions.draw()
        win.flip()
        moveScreen4 = event.waitKeys(keyList= ['s'])[0]
    
    if moveScreen4 == 's':
        for curTrial in trialInfo:
         showLearningTrial(curTrial,header,outputFile,pics,sounds)


def showLearningTrial(curTrial,header,output_file,pics,sounds):

    for curTrial in  trialInfo:

        #score game
        global points
        print points
        score = 'likes: %s' %(points)
        scoreText = visual.TextStim(win=win,text=score,color="blue",height=40, pos=(0,-300))

        core.wait(preFixationDelay) 
        fixationCross.draw() #fixation 
        win.flip()
        core.wait(postFixationDelay)

        win.flip()
        core.wait(.5)

        if curTrial['soundStress'] == '1':
            noise = random.choice(noises)
            soundStress = pathSound+noise
            print soundStress
            winsound.PlaySound(soundStress, winsound.SND_FILENAME)
            #soundsStress['stress1']['stim'].play()
        
        #face
        curFace = curTrial['face'] #pic for that trial 
        pics[curFace]['stim'].setPos((0,-75))
        pics[curFace]['stim'].draw()
        
        #books
        bookLeft = curTrial['leftPos']
        bookRight = curTrial['rightPos']
        pics[bookLeft]['stim'].setPos(posBookLeft)
        pics[bookRight]['stim'].setPos(posBookRight)
        pics[bookLeft]['stim'].draw()
        pics[bookRight]['stim'].draw()
        
        #score
        if points<0:
            scoreText.setColor("red")
        scoreText.draw()
        
        win.flip()

        #time for response
        if curTrial['condition'] == 'hs':
        	waitTime = 1.5
        else:
        	waitTime = 3.0

        responseTimer = core.Clock()
        responseTimer.reset()
        
        results = event.waitKeys(maxWait=waitTime, keyList=validKeys, timeStamped=responseTimer) # example results = [['x', 0.34243]]
        
        if results == None:
            #too late feedback
            tooLate.draw()
            win.flip()
            core.wait(1)

            #write data
            curTrial['RT'] = 'NA'
            curTrial['isRight'] = 'NA'
            curTrial['score'] = 'NA'
            trialData = []
            for colName in header:
                trialData.append(curTrial[colName])
            writeToFile(output_file,trialData,writeNewLine=True)

            #skip to next trial 
            continue
        
        print 'after if', results

        key, RT = results[0] #split key and RT as independent variables
        isRight = int(key == curTrial['expectedKey']) #check if response is expected respose; retunr boolean 1,0
        RT = RT*1000.0 #reaction time in ms to output file

        #checking if right, wrong, and feedback
        if isRight:
            points +=1
            novelObject= str(random.choice(range(40)))
            objects[novelObject]['stim'].draw()
            sounds['bleep']['stim'].play()
            correctFeedback.draw()
        else:
            points -=1
            novelObject= str(random.choice(range(40)))
            objects[novelObject]['stim'].draw()
            sounds['buzz']['stim'].play()
            incorrectFeedback.draw()

        win.flip()
        core.wait(.5)
        
        #write data to output file
        curTrial['RT'] = RT
        curTrial['isRight'] = isRight
        curTrial['score'] = points
        trialData = []
        for colName in header:
            trialData.append(curTrial[colName])
        writeToFile(output_file,trialData,writeNewLine=True)
    
if __name__ == '__main__':

    (header, trialInfo, outputFile) = initExperiment() #get runtime variables, create trial lists, etc.
   
    header.extend(['isRight', 'RT', 'score']) #adding isRight and RT to header for output
    writeToFile(outputFile, header, writeNewLine=True)
   
    win = visual.Window(fullscr=True,allowGUI=False, color="gray", units='pix', size=(1400, 900))
    pics =  loadFiles('stimuli/visual','.jpg','image', win=win) #can now access ImageStim objects as pics['filename']['stim']
    objects =  loadFiles('stimuli/objects','.jpg','image', win=win) #can now access ImageStim objects as objects['filename']['stim']
    sounds = loadFiles('stimuli/sounds', '.wav', 'sound', win=win) #acces sounds
    fixationCross = visual.TextStim(win=win,text="+",color="white",height=40)
    correctFeedback = visual.TextStim(win=win,text="Thank you!",color="blue",height=50, pos=(0,320))
    incorrectFeedback = visual.TextStim(win=win,text="Not this time...",color="red",height=50, pos=(0,320))
    tooLate = visual.TextStim(win=win,text="Too slow!",color="red",height=50, pos=(0,0))
    pathSound = ("C:/Users/pablo/Documents/GitHub/project2/stimuli/sounds/")
    
    if trialInfo[0]['condition'] == 'hs':
        points = -10 #if high stress condition, start with -10 
    else:
        points = +10 #if low stress condition, start with +10
        
    showIntroDisplay(pics,trialInfo)    
