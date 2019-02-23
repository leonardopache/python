import os
import readDirectory

path = input("Project path:")
dir= readDirectory.ReadDirectory()
if os.path.exists(path):
    dir.find('mutations.csv',path)
else:
    print("Please verify the path...")








