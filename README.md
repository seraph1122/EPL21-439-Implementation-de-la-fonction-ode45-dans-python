This project folder is composed of a series of files and directories. The main directory contains the following files
    -feval.py
    -ntrp45.py
    -odearguments.py
    -odeevents.py
    -odefinalize.py
    -odeget.py
    -odemass.py
    -odemassexplicit.py
    -odenonnegative.py
    -odeoptions.py
    -odezero.py
These files contain their respective functions, the ode.py file contains the main ode45 function. In addition a demo.py file contains a series of demos to show a user the proper utilisation of the ode45 function, as well as it’s capabilities. Some of the demos are examples given by MATLAB. The project folder also contains two directories, the first one odeTests contains the following files:
    -fevalTest.py
    -ntrp45Test.py
    -odeargumentsTest.py
    -odeeventsTest.py
    -odefinalizeTest.py
    -odegetTest.py
    -odemassexplicitTest.py
    -odemassTest.py
    -odenonnegativeTest.py
    -odeoptionsTest.py
These files contain a series of unit tests for their respective helper functions. These files use the functions located in their parent directory. The other directory is testScript which contains the following files:
    -ode45Tests.m
    -ode45Tests.py
    -testScript.m
    -testScript.py
The ode45Tests.* files are unit tests for the main ode45 function. To run the unit tests first the MATLAB ode45Tests.m files should be executed, this will create a ode45.txt file of the expected outputs for a set of inputs. The ode45Tests.py file can then be executed, which will read the text file and ensure the unit tests pass.The testScript.* files are the scripts for the randomised testing.  To run the randomised tests, first the MATLAB testScript.m file should be executed, this will create a text file of the expected outputs for a set of inputs. The user can make a choice of the function to be tested as well as the options which should be randomised. The testScript.py file can then be executed, which will read the text file and print out the differences between the actual output and expected output. These files use the functions located in their parent directory.
