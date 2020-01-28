import time as time
from nptdms import TdmsFile
from pathlib import Path

# Make a "Processed" directory as a subdirectory one folder up

"""
Contract for buildDirectories:

input:

takes in:
    path to the TDMS directory
    the memory array of the TDMS files

return:

returns a dictionary of every part and its file location

"""


def buildDirectories(sourceTDMSDirectory, tdmsFiles, taskName):
    directoryBuildTime = time.time()

    # sourceTDMSDirectory is where we are collecting these files

    # I know these parentheses are ugly, but lemme explain.
    # TdmsFile only takes a string, but I want it to work on Linux or Windows. So I'm using the Path library
    # to concatenate these strings together in a way that works on both OS's.
    #   The Path lib takes a "/" as an operator to concatenate filepaths.
    # Then, after I concatenate the paths, I turn them back into a string.
    firstObject = TdmsFile(str(Path(str(sourceTDMSDirectory)) / Path(str(tdmsFiles[0]))))

    parentDir = sourceTDMSDirectory.parent
    newFolder = parentDir / str(taskName)
    newFolder.mkdir(exist_ok=True, parents=True)

    # Now that we have the folder: let's go in and make a subfolder for every group we've got in the TDMS files.
    folderDictionary = dict()
    groups = firstObject.groups()
    for part in groups:
        folderName = str(part)
        newDir = newFolder / folderName
        newDir.mkdir(exist_ok=True, parents=True)
        # print("\n \n" + str(part) + " \n" + str(newDir))

        folderDictionary[str(part)] = str(newDir)

    # pprint(FolderDictionary)
    # Boom: we've now got a folder for every part, and a mapping of group name (part name) to folder name.

    # Next step is to go into every TDMS's item, and write the
    # associated data to a CSV inside of the folder for that name, with a good name for the slice.
    # sourceTDMSDirectory

    directoryBuildTime = time.time() - directoryBuildTime
    print("Time to build directories was " + str(directoryBuildTime) + " seconds.\n")

    return folderDictionary
