# TDMSData_CDME
Transforms TDMS data from the CDME's Metal 3D Printers to a more readable file format

The original problem: The TDMS file outputs from the metal 3d printers here at the lab come with the following hierarchy:

A build will be made of hundreds to thousands of slices, all printed onto the same build plate.
  Each slice of the build has dozens of parts on it, that all occur at the same height on the Y axis.
    Each part has some associated data inside of a TDMS file.
    
This is pretty understandable at a conceptual level but not very easy to machine read in for visualization purposes.

For visualization purposes, we would prefer to have:

A build will be made of dozens of parts
  Each part is made of hundreds to thousands of slices
    Each slice has some associated data located inside a file.
    
This script transforms the file arrangement to be in a folder hierarchy with CSV storage.

Original versions were terrible with memory management but that's been alleviated in the uploaded version.
