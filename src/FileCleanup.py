import shutil
import os


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def count_files(start_path="."):
    total_files = 0
    return len(os.listdir(start_path))


def cleanFiles(folderDictionary):
    partsDeleted = 0
    partsRemaining = 0
    minimumBytes = 0
    mode = 'csv'
    for k, v in folderDictionary.items():

        print(str(v))
        print(str(v)[-5:])
        if "hdf5" in v[-5:]:
            lastSlash = v.rfind("/")
            v = v[0:lastSlash]
            mode = "hdf5"

        byteSize = get_size(v)
        fileCount = count_files(v)
        if "c" in mode:
            minimumBytes = 62 * int(fileCount)  # 61 is the number of bytes contained in the headers, if CSV
        elif "h" in mode:
            minimumBytes = 9024 * int(fileCount) + 1
        # If a folder has less than 62 bytes per file, then delete the folder.
        # Note: if there are some empty files in a folder, leave the entire thing for now.
        if byteSize < minimumBytes:
            # delete the directory v, since many of the folders don't actually contain any data
            partsDeleted = partsDeleted + 1
            shutil.rmtree(v)
        else:
            partsRemaining = partsRemaining + 1

    return partsDeleted, partsRemaining



