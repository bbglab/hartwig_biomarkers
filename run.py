import sys
import os

print("Move to launch directory..") 
wd = os.getcwd() + '/launch_pad/'
os.chdir(wd)

print("Convert notebooks to scripts..")
os.system('python prepare_the_engines.py')

print("Go!")
os.system('./go.sh') 
