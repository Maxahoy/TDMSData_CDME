#!/usr/bin/env python
# coding: utf-8

# Install npTDMS to actually pull in the TDMS files.
# 
# 

# In[ ]:


import sys
get_ipython().system('{sys.executable} -m pip install nptdms')
get_ipython().system('{sys.executable} -m pip install numpy')
# At least on my system, requirements already satisfied.


# Import the tdmsfile reader capabilities from nptdms

# In[16]:



import time as time
import numpy as np
from nptdms import TdmsFile
from pprint import pprint
import os
from os import walk
import shutil
import pathlib
from pathlib import Path
import csv
from itertools import chain

startTime = time.time()


# 
# ## Actually reading things in:
# 
# The file structure currently isn't really nested the way we want it to be. We need to know:
# 
# 1. How many parts are in our TDMS group.
# 2. How many layers total are in our TDMS group.
# 
# Ideally, I'd like to be able to work with zipped folders, but there are no guarantees on that one.
# 
# First goal: Write a method that can find all of our folders witih TDMS files included.
# 
# Folder needs to have Slice00000#.tdms inside
# 
# So: 
# Slice000001.tdms
# Slice000002.tdms
# Slice000003.tdms ...
# 
# ...
# Slice00000N.tdms
# for N slices
# 
# The result will be a directory called "NAME, DATE, TDMS Files"
# Inside: 
# \*PART 1 NAME\*, \*PHD OR CAMERA\* TDMS Files
# \*PART 2 NAME\*, \*PHD OR CAMERA\* TDMS Files
# \*PART 3 NAME\*, \*PHD OR CAMERA\* TDMS Files
# ...
# \*PART 1 NAME\*, \*PHD OR CAMERA\* TDMS Files
# 
# Inside each one of those will be:
# Slice0001.csv
# Slice0002.csv
# ...
# Slice000N.csv
# 
# For the N slices.
# 

# In[3]:


#print("Example directory path: \nC:/Users/maxah/Documents/CDME/Sept 9 2019 TDMS Parts/TDMS\n")
testPath = "C:\\Users\\maxah\\Documents\\CDME\\Sept 9 2019 TDMS Parts\\TDMS"

print("Enter directory path. Forward or backward slash doesn't matter.\n")

time.sleep(.1)
#just so that the output makes sense to the user in the correct order; otherwise,
#                     the input prompt would come first and be confusing.
yesNoChar = 'n'
dir_path = ""
numFiles = 0
firstFileName = ""
tdmsFiles = []

while( 'y' not in yesNoChar and 'Y' not in yesNoChar):
    
    #C:\\Users\\maxah\\Documents\\CDME\\Sept 9 2019 TDMS Parts\\TDMS
    #/home/maxwell/Documents/CDME/TestDataATRQ
    if(yesNoChar == 'n' or yesNoChar == "N"):
        dir_path = input("Example path: " + "C:\\Users\\maxah\\Documents\\CDME\\Sept 9 2019 TDMS Parts\\TDMS" + "\n")  
        if("testpath" in dir_path or "TESTPATH" in dir_path):
            dir_path = testPath
    
    #dir_path = testPath
    root = os.path.abspath(os.sep)
    cwd = Path.cwd()

    if('\\' in dir_path):
        newPath = dir_path.replace("\\","/")
        dir_path = newPath
    
    
    sourceTDMSDirectory = root / Path(dir_path)        

    print("The chosen directory is: " + dir_path)   
    
    fileNames = []
    for (dirpath, dirnames, filenames) in walk(sourceTDMSDirectory):
        fileNames.extend(filenames)
        break


    for fileName in sorted(fileNames):
        if ".tdms_index" not in fileName:
            tdmsFiles.append(fileName)
            numFiles = numFiles + 1
    print("Here are the contents of that directory: \n")
    length = len(tdmsFiles)
    if(length > 0):
        firstFileName = tdmsFiles[0]
    pprint(tdmsFiles)
    
    yesNoChar = input("If that is not the directory you want, hit 'n'. If that is the directory you want, hit 'y'.\n")
    
print("What are you going to call this project?\nEX: \"Nov 21 Build TDMS\"")
taskName = "Processed Stacks " + input("")
sourceTDMSDirectory = Path(dir_path)

"""
print("What do you want the batch size to be?\nRecommended values: 5 or 10. Higher batch size means higher memory usage.")
batchSize = int(input("Please enter a number: "))

"""
batchSize = 1

firstSliceNum = firstFileName[-6:-5]
#C:\\Users\\maxah\\Documents\\CDME\\Sept 9 2019 TDMS Parts\\TDMS
#/home/maxwell/Documents/CDME/TestDataATRQ
# /home/maxwell/Documents/CDME/ATRQTestFolder


# ### Filepath now stored. 
# 
# Filepath is now stored and we have a handy dandy conversion from Windows file structure to a python readable format.
# Let's create a list of everything in the directory.
# 
# Any ".tdms_index" files are created by using the National Instruments' "TDMS To Excel" tool, and can be ignored.
# They will just be removed from the list.

# In[8]:


# Make a map of the file names to new file locations; 

#Make a "Processed" directory as a subdirectory one folder up

directoryBuildTime = time.time()

#sourceTDMSDirectory is where we are collecting these files

# I know these parentheses are ugly, but lemme explain.
#TdmsFile only takes a string, but I want it to work on Linux or Windows. So I'm using the Path library
# to concatenate these strings together in a way that works on both OS's. 
#   The Path lib takes a "/" as an operator to concatenate filepaths.
# Then, after I concatenate the paths, I turn them back into a string.
firstObject = TdmsFile(str(Path(str(sourceTDMSDirectory)) / Path(str(tdmsFiles[0]))))

parentDir = sourceTDMSDirectory.parent
newFolder = parentDir / str(taskName)
newFolder.mkdir(exist_ok=True, parents=True)

#Now that we have the folder: let's go in and make a subfolder for every group we've got in the TDMS files.
FolderDictionary = dict()
groups = firstObject.groups()
for part in groups:
    folderName = str(part)
    newDir = newFolder / folderName
    newDir.mkdir(exist_ok=True, parents=True)
    #print("\n \n" + str(part) + " \n" + str(newDir))
    
    FolderDictionary[str(part)] = str(newDir)
    
#pprint(FolderDictionary)
#Boom: we've now got a folder for every part, and a mapping of group name (part name) to folder name.

#Next step is to go into every TDMS's item, and write the
#associated data to a CSV inside of the folder for that name, with a good name for the slice.
#sourceTDMSDirectory

directoryBuildTime = time.time() - directoryBuildTime
print("Time to build directories was " + str(directoryBuildTime) + " seconds.\n")


# In[13]:


#print(str(sourceTDMSDirectory) + "\\" + tdmsFiles[0])
#testTime = time.time()
openedSoFar = 0
numLayers = 0
tdmsObjects = []
numBatches = 0
populatedList = set()
sliceCounter = int(firstSliceNum) - 1
#Outermost loop: controls the number of files written, total.
while numLayers < numFiles:
    
    #Gets files from TDMS files
    #   This one isn't the outermost because I want to manage memory better.
    for file in tdmsFiles:
        
        #opens a TDMS file. Doing the same weird path-trick as before, to be OS independent.
        tdmsObjects.append( TdmsFile( str( Path(str(sourceTDMSDirectory)) / Path(str(file)) ) ) )
        numLayers+=1
        
        #Once we've got a few of the TDMS files open, transform them into CSV's.
        #   Happens every time a batch is fill (IE: every 5th file)
        if(numLayers % batchSize == 0 or numLayers == numFiles):
            
            #all of the actual file writing will happen in here
            
            processTime = time.time()
            #print("Block " + str(numBatches))
            #print(str(tdmsObjects) + "\n")
            
            
            colNames = []
            populatedList = set()
            
            #print(tdmsObjects)
            #print(numLayers)
            
            for tdms in tdmsObjects:
                sliceCounter = sliceCounter + 1
                groups = tdms.groups()
                #print(tdms)
                for part in groups:
                    #get the data from each group's channel and make a CSV
                    channels = tdms.group_channels(part)
					
                    #make a 2D array, and populate it with the arrays in this loop.
                    groupCSV = []
                    areaCol = []
                    xCol = []
                    yCol = []
                    paramCol = []
                    intensityCol = []
                    laserCol = []
                    csvCount = 0
                    #copy each channel's data to its respective frame
        
                    for channel in channels:
            
                        names = []
                        for i in channels:
                            wordList = str(i).split("/")
                            name = wordList[-1]
                            name = name.strip(">")
                            name = name.strip("'")
                            names.append(name)
                        colNames = names    
                        #pprint(channel.data)
                        name = channel.channel
                        data = channel.data
            
                        if(names[0] in name):
                            areaCol = data
                        elif(names[1] in name):
                            xCol = data
                        elif(names[2] in name):
                            yCol = data
                        elif(names[3] in name):
                            paramCol = data
                        elif(names[4] in name):
                            intensityCol = data
                        elif(names[5] in name):
                            laserCol = data
                        groupCSV.append(data)
                        csvCount += 1
            
                    csvFileLocation = FolderDictionary[str(part)]
                
                    #I tried avoiding this earlier, but here I'm just checking the os. If unix, then use
                    #  the unix file delimiter (forwardslash). If windows, then use the backslash delimiter.
                    if(os.name is "posix"):
                        sliceFileName = str(csvFileLocation) + "/Slice000" + str(sliceCounter) + ".csv"
                    elif(os.name is "nt"):
                        sliceFileName = str(csvFileLocation) + "\\Slice000" + str(sliceCounter) + ".csv"
                        
                    
                    with open(sliceFileName, mode="w", newline = "") as csvfile:
                        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL, dialect="excel")
                        wr.writerow(names)
                        
                        #if len(areaCol) > 1 means:
                        #if there are data points in here
                        # But what if there straight up aren't any columns to begin with??
                        
                        # IN that case then I need to identify if there are no rows
                        
                        if(len(areaCol > 1)):
                            for rows in range(0,len(areaCol - 1) ):#- 1):
                                #print(str(len(areaCol)) + "\n")
                                
                                # THIS IS A PROBLEM LINE
                                # With this line: I need to check if there are things here,
                                #   and not write the row if that's the case.
                                # Alternative: a try / catch on this bad boy?
                                
                                try:
                                    #print("Writing file: " + str(sliceFileName) + "\n")
                                    row = [areaCol[rows], xCol[rows], yCol[rows], paramCol[rows], intensityCol[rows], laserCol[rows]]
                                    wr.writerow(row)
                                except IndexError: 
                                    print("IndexError. Possibly no data for that part anymore?")
                                    print("While writing file: " + str(sliceFileName) + "\n")
                            populatedList.add(part)
                
            
            processTime = time.time() - processTime
            print("\nTime for this batch was " + str(processTime) + " seconds.")
            print("Or " + str(processTime / (sliceCounter - int(firstSliceNum) + 1)) + " seconds per layer.\n")

            
            #end operation space
            #this declaration clears the memory for the tdms objects
            tdmsObjects = []
            numBatches = numBatches + 1
        
    

    
#endTime = time.time()

#timeLength = endTime - testTime
#this block takes roughly 13.49 seconds on my machine -- 
#print("All TDMS objects read in, took " + str(timeLength) + " seconds.\n" + str((timeLength)/5) + " seconds per layer.\n")
#or roughly 2.7 seconds per layer. That isn't ideal, 
#since it's the price we can stand to pay for every access of a TDMS object.


# Time information:
# It's taking roughly 30 seconds per layer, but that's probably pretty variable.
# If you want to do 800 layers then, we're looking at 2400 seconds or 40 minutes.
# This might be the kind of script you set up and run and leave overnight once it's finished.
# Speed may also depend on the computer it's being performed on -- the slowdown is likely the read/writes happening, so the 
# hard disk in the desktops here at the CDME could be slower than my machine's SSD.

# In[14]:


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def count_files(start_path = "."):
    total_files = 0
    return(len(os.listdir(start_path)))
    

#print(get_size(), 'bytes')


# In[15]:


partsDeleted = 0
partsRemaining = 0
for k, v in FolderDictionary.items():
    byteSize = get_size(v)
    fileCount = count_files(v)
    minimumBytes = 62 * int(fileCount) #61 is the number of bytes contained in the headers.
    #If a folder has less than 62 bytes per file, then delete the folder.
    #Note: if there are some empty files in a folder, leave the entire thing for now.
    if (byteSize < minimumBytes):
        #delete the directory v, since many of the folders don't actually contain any data
        partsDeleted = partsDeleted + 1
        shutil.rmtree(v)
    else:
        partsRemaining = partsRemaining + 1

# Boom: now it only keeps those which have items inside.
print("Finished.\n")
pprint(populatedList)
        
endTime = time.time()
runTime = endTime - startTime
print("\n***FINISHED REPORT***")
print("\n" + "Runtime was: " + str(runTime) + " seconds.")
print("Number of layers written was: " + str(numLayers) + " layers.")
print("Number of parts with no data was: " + str(partsDeleted) + " parts.")
print("Number of parts with data was: " + str(partsRemaining) + " parts.")
print("Parts with data: ")

#input hold; causes the program to freeze before exiting.
exit = input("Finished: type the X key to exit.")
time.sleep(.01)
if("x" not in exit and "X" not in exit):
    input()

