# autoGos
Scans diagonal and transitional matrix element planes for intensity ratio matches

DESCRIPTION
------------

autoGos takes a Gosia input file for a projectile with OP,INTI and calculates the intensity ratio for a given range of diagonal and transitional matrix elements.
It outputs a list of diagonal and tranistional matrix elements for which the difference between the intensity ratio calculated with Gosia and the
intensity ratio calculated experimentally is smaller then a user defined value.

REQUIREMENTS
------------

autoGos is written in Python and any python compiler is sufficient.
The yields are summed using a perl scrpit which is also provided
Gosia also needs to be installed with the name "gosia" and the $PATH varible pointing to the installation directory

USAGE
------------
```
Usage: autoGos.py <Inputfile>
```

FILE FORMAT
------------

autoGos requires a Gosia input file at the OP,INTI step. Note that autoGos assumes that the gosia input file is correct and executes without any errors.
Run Gosia with your input file and confirm that it executes correctly.

OUTPUT
------

The program outputs a text file with 3 coloums, these are:

Diagonal matrix element	|	Transitional matrix element | residual

The matrix elements are the points at which the match in the intensity ratios occured. The residual is the difference between the calculated and 
the measured intensity ratio. 
