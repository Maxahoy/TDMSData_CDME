"""
Contract:

Inputs:
array of part names (TDMS file part names)
target folder locations
source file directory
number of files to write (numFiles)

batchSize (defaults to 1, don't bother changing it.)
first slice number (optional; defaults to 1, but changes if the starting slice number is
    not one. IE, segmenting your work or doing testing.)

Outputs:
the folder with all the written files. No return object necessary, just the action performed.

"""


# TODO: HDF5



import time as time
from nptdms import TdmsFile
from pprint import pprint
import os
from os import walk
import shutil
from pathlib import Path
import csv
import h5py


def writeFiles(folderDictionary, tdmsFiles, sourceTDMSDirectory, numFiles, batchSize=1, firstSliceNum=1, mode="csv"):

    # print(str(sourceTDMSDirectory) + "\\" + tdmsFiles[0])
    # testTime = time.time()
    openedSoFar = 0
    numLayers = 0
    tdmsObjects = []
    numBatches = 0
    populatedList = set()
    sliceCounter = int(firstSliceNum) - 1
    # Outermost loop: controls the number of files written, total.
    while numLayers < numFiles:

        # Gets files from TDMS files
        #   This one isn't the outermost because I want to manage memory better.
        for file in tdmsFiles:

            # opens a TDMS file. Doing the same weird path-trick as before, to be OS independent.
            tdmsObjects.append(TdmsFile(str(Path(str(sourceTDMSDirectory)) / Path(str(file)))))
            numLayers += 1
            print("Printing slice " + str(numLayers) + " out of " + str(int(firstSliceNum) + int(numFiles) - 1) + ".")
            # Once we've got a few of the TDMS files open, transform them into CSV's.
            #   Happens every time a batch is fill (IE: every 5th file)
            if numLayers % batchSize == 0 or numLayers == numFiles:

                # all of the actual file writing will happen in here

                processTime = time.time()
                # print("Block " + str(numBatches))
                # print(str(tdmsObjects) + "\n")

                colNames = []
                populatedList = set()

                # print(tdmsObjects)
                # print(numLayers)

                for tdms in tdmsObjects:
                    sliceCounter = sliceCounter + 1
                    groups = tdms.groups()
                    # print(tdms)
                    for part in groups:
                        # get the data from each group's channel and make a CSV
                        channels = tdms.group_channels(part)

                        # make a 2D array, and populate it with the arrays in this loop.
                        groupCSV = []
                        areaCol = []
                        xCol = []
                        yCol = []
                        paramCol = []
                        intensityCol = []
                        laserCol = []
                        csvCount = 0
                        # copy each channel's data to its respective frame

                        for channel in channels:

                            names = []
                            for i in channels:
                                wordList = str(i).split("/")
                                name = wordList[-1]
                                name = name.strip(">")
                                name = name.strip("'")
                                names.append(name)
                            colNames = names
                            # pprint(channel.data)
                            name = channel.channel
                            data = channel.data

                            if names[0] in name:
                                areaCol = data
                            elif names[1] in name:
                                xCol = data
                            elif names[2] in name:
                                yCol = data
                            elif names[3] in name:
                                paramCol = data
                            elif names[4] in name:
                                intensityCol = data
                            elif names[5] in name:
                                laserCol = data
                            groupCSV.append(data)
                            csvCount += 1

                        writeFileLocation = folderDictionary[str(part)]

                        # I tried avoiding this earlier, but here I'm just checking the os. If unix, then use
                        #  the unix file delimiter (forwardslash). If windows, then use the backslash delimiter.
                        if os.name is "posix" and mode is "csv":
                            sliceFileName = str(writeFileLocation) + "/Slice000" + str(sliceCounter) + ".csv"
                        elif os.name is "nt" and mode is not "csv":
                            sliceFileName = str(writeFileLocation) + "\\Slice000" + str(sliceCounter) + ".csv"

                        with open(sliceFileName, mode="w", newline="") as writeFile:
                            wr = csv.writer(writeFile, quoting=csv.QUOTE_ALL, dialect="excel")
                            wr.writerow(names)

                            # if len(areaCol) > 1 means:
                            # if there are data points in here
                            # But what if there straight up aren't any columns to begin with??

                            # IN that case then I need to identify if there are no rows

                            if len(areaCol > 1):
                                for rows in range(0, len(areaCol - 1)):  # - 1):
                                    # print(str(len(areaCol)) + "\n")

                                    # NOTE: the try catch isn't the best way to do this, I know.
                                    # HOWEVER, I can't deduce what the actual problem is here.
                                    # It's the best I can do -- Maxwell, Jan 15 2019.
                                    try:
                                        # print("Writing file: " + str(sliceFileName) + "\n")
                                        row = [areaCol[rows], xCol[rows], yCol[rows], paramCol[rows], intensityCol[rows],
                                               laserCol[rows]]
                                        wr.writerow(row)
                                    except IndexError:
                                        print("IndexError. Possibly no data for that part anymore?")
                                        print("While writing file: " + str(sliceFileName) + "\n")
                                populatedList.add(part)

                processTime = time.time() - processTime
                print("\nTime for this batch was " + str(processTime) + " seconds.")
                print("Or " + str(processTime / (sliceCounter - int(firstSliceNum) + 1)) + " seconds per layer.\n")

                # end operation space
                # this declaration clears the memory for the tdms objects
                tdmsObjects = []
                numBatches = numBatches + 1

    return numLayers

