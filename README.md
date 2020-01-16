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
    
This script transforms the file arrangement to be in a folder hierarchy with CSV storage. (HDF5 coming)

TODO: Update to use HDF5 instead of CSV storage, and add a csv mode when run with that option. But preferably HDF5.
        This will enable better computation and data analysis on the results, such as summary statistics, visualizations (histograms) or even 3-dimensional array visualizations.
        
        
