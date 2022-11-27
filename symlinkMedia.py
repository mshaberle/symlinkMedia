import os
import re

movieSources: list = ['/home/miller/files/movies/', '/home/miller/files2/movies', '/home/miller/files3/movies', '/home/miller/files4/movies', '/home/miller/files5/movies']
movieTarget: str = '/home/miller/.bin/movies/'
badExtensions: list = ['.nfo', '.jpg', '.png']

def main():
    
    for source in movieSources:

        filesAndDirs: list = os.listdir(source)

        files: list = []
        dirs: list = []
        errors: list = []

        goodFiles: list = []

        for name in filesAndDirs:
            if(name[0] == '.'):
                filesAndDirs.remove(name)
            if('.' in name[-4:]):
                files.append(name)
            else:
                dirs.append(name)

        goodFiles = cleanFiles(files)
        
        makeLinks(source, goodFiles)

        for directory in dirs:
            goodDirFiles: list = []

            workingDir = f"{source}/{directory}"

            dirContents: list = os.listdir(workingDir)
           
            dirFiles, dirDirs  = siftDir(dirContents)

            goodDirFiles = cleanFiles(dirFiles)

            makeLinks(workingDir, goodDirFiles)

def makeLinks(currSource: str, fileList: list):
    for file in fileList:
        sourceFile = currSource+"/"+file[0]
        targetDirectory = movieTarget+file[1]
        movieFile = file[1]+os.path.splitext(file[0])[1]

        if not os.path.exists(targetDirectory):
            os.makedirs(targetDirectory)
            os.symlink(sourceFile, f"{targetDirectory}/{movieFile}")

def siftDir(directoryContents):
    files: list = []
    dirs: list = []

    for name in directoryContents:
        if(name[0] != '.'):
            if('.' in name[-4:]):
                if name[-4:] not in badExtensions:
                    files.append(name)
            else:
                dirs.append(name)

    return files, dirs

def cleanFiles(fileList):
    cleanedFiles: list = []

    for file in fileList:
        result = re.search(r"((?<!\[)(?:\b\w*\b)(?!\])).+([0-9]{4}(?!\w))", file)
        if result:
            s: str = result.group()
            s = s.replace(".", " ")
            s = s.replace("_", " ")
            
            t1: str = s[-4:]
            s = s.replace(s[-4:], f"({t1})")

            cleanedFiles.append((file, s))
    
    return cleanedFiles

if __name__ == '__main__':
    main()
    print("Done linking")
