# PYTHON TERMACT LIB
# INTERACT WITH THE TERMINAL

import os

def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        os.system("clear")

def echo(text):
    text = str(text)
    if os.name == "nt":
        os.system("echo " + text)
    elif os.name == "posix":
        os.system("echo " + text)
    else:
        os.system("echo " + text)