lminstreloc is short for LMMS instrument (file) relocator

LMMS is a program I use(d) to build music with.

It used files where samples and soundfounts are stored, and after reorganizing them it can't find them anymore.
So I created this program, to change things all at once instead of having to do it for each instrument separately in the user interface.

basically it searches a module for the files used, checks if they exist, and presents the results in a GUI so I can make changes and have them written back to the module. 

To help me in this process I partly reused the logic to build a utility that can list all the samples and soundfonts used in all LMMS modules. 
To help in reorganizing my samples collection and removing duplicates another utility can list all the samples in the user directories with some essential attributes, ordered by filename (not path).
