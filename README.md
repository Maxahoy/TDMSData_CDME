# TDMSData_CDME
Transforms TDMS data from the CDME's Metal 3D Printers to a more readable file format. This is part of the Ohio State University Center for Design and Manufacturing Excellence Additive Manufacturing lab efforts.

The original problem: The TDMS file outputs from the metal 3d printers here at the lab come with the following hierarchy:

A build is made of hundreds to thousands of slices, all printed onto the same build plate. Each slice has a TDMS file.
    Each slice of the build has dozens of parts on it, that all occur at the same height on the Y axis. 
        Each part has some associated data inside of a TDMS file. All parts are contained in 1 file.
    
This is pretty understandable at a conceptual level but not very easy to machine read in for visualization purposes.
For one, we can't easily grab multiple layers from one part; instead, we have to grab many parts.
I'm going ahead and separating these manually.

For visualization purposes, we would prefer to have:

A build will be made of dozens of parts
  Each part is made of hundreds to thousands of slices
    Each slice has some associated data located inside a file.
    
This script transforms the file arrangement to be in a folder hierarchy with CSV or HDF5 storage.

***USAGE INSTRUCTIONS***

The repository linked contains a src folder and a README. Download the src folder or clone the repository to your local machine to use it.

Software prerequisites: 
    Python interpreter & IDLE: https://www.python.org/downloads/
        Make sure to install Pip. 
All of the project was written with Python 3.8 in mind, but the most recent Python 3 version should work.
    
After installing Pip: open your command line (On windows, run cmd.exe. On Linux, you should know how to do that.)
    Run the following to install some python libraries:

    pip install nptdms
    pip install numpy
    pip install h5py

These three libraries are required. If these don’t work because you don’t have admin permissions, install locally by appending the --user flag to the commands.

Ok, so I’ve got Python downloaded, the three libraries installed, and the src folder downloaded. What now?

Locate the folder of tdms files you want to transform. If they’re in a zip folder, extract them out of the archive.

Run the “main.py” file in the src folder by right clicking & selecting “Run with IDLE”. Alternatively, start a command line, navigate to the folder with main.py, and run it in python with the commands python then Main.py.

I’ve got it running, now what?

You will receive several prompts:
    
First, enter the directory path for the file folder you want to transform. You can copy & paste this in. Don’t worry about either forward or backward slashes, either works.
        The contents of the selected directory will be shown so you can confirm yes/no.
        If you’re sure, then hit “y” and continue. Otherwise, hit “n” to re-enter your choice.
If you enter “TESTPATH” or “testpath”, a special case occurs. This was only for testing, but you can change the testpath in the code if you need to test things.



Second, what will you call the project? 
The result folder will be called <project name> Processed Stacks, and will be located in the same root folder as the TDMS folder you’ve chosen.
If <testpath>, then you won’t be asked this question.

Third, what file-saving mode to use?
    CSV is by default. Press enter or “c” to select “csv”.
    Press “h” and enter to use HDF5 mode. 

That’s it! If you choose CSV, then you’ll get occasional messages about index errors. These can be safely ignored and only mean that I have some off-by-one errors somewhere that I failed to pin down.
If you choose HDF5 these will be a non-issue.

Be prepared to wait a while depending on how much data needs transformed -- it might be worthwhile to run this overnight or when doing other work.   
