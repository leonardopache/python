import os
import readDirectory

def main():

    path = input("Project path:")
    dir= readDirectory.ReadDirectory()

    if os.path.exists(path):
        dir.find('mutations.csv',path)
        return True
    else:
        print("Please verify the path...")
        return False


    if __name__ == '__main__':
        if len(sys.argv) > 1:
            main(sys.argv[1])
    else:
        sys.exit(-1)
        sys.exit(0)