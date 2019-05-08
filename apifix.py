import os
import sys
import subprocess
import glob
from urllib.request import urlopen
from urllib.error import HTTPError
from collections import namedtuple
from warnings import warn

#Remove duplicates of "## Required reading"
def removeDuplicates(someList):
    uniqueList = []

    for elem in someList:
        if elem not in uniqueList:
            uniqueList.append(elem)

    return uniqueList


while True:

    try:

        url = "https://api.github.com/orgs/python-elective-2-spring-2019/repos?per_page=100"
        # Download the wanted URL-html
        #url = input('Please specify the url you want to be downloaded : ')
        res = urlopen(url)
        html = res.read().decode('utf-8', 'ignore')
        

        # opens a file in the current path and writes in the html content
        file = "repository_info.html"
        with open(file, "w", encoding="utf-8") as f:
            f.write(html)
            f.close()
              

        #Save all the repository clone urls in a list
        #clone_url = 'clone_url'
        urlList = []
        with open (file) as f:
            for line in f:
                newLine = line.split(',')
            
                for clone_url in newLine:
                    if clone_url.startswith('"clone_url'):
                        urlList.append(clone_url) 
                        

                    else:
                        pass        
            
        print(urlList)
        print('\n')    
        f.close()
        
        #function that clones the url repositories to the current path 
        def git_clone(url):
            process = subprocess.Popen(['git', 'clone', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return namedtuple('Std', 'out, err')(process.stdout.read(), process.stderr.read())


        #loop though list of repository url's and clone them one after one
        i = 0
        while i < len(urlList):
             git_url = urlList[i][13:-1]
             git_clone(git_url)

             i += 1


        
        readmeList = []
        requiredList = []
        cwd = os.getcwd()
        filenameText = ""

        #Store the readme.md file content in a list
        #glob finds all files with the name "README.md" and reads them
        for filename in glob.glob(cwd + '/**/README.md', recursive=True):
            with open (filename, encoding="utf-8") as text:
                filenameText = text.readlines()
                

                # add content of "## Required reading" to the list reguiredList
                i = 1
                for line in filenameText:
                    if line.startswith('## Required reading'):
                         
                        requiredList.append(line)

                        while filenameText[filenameText.index(line) + i].startswith('* '):
                            requiredList.append(filenameText[filenameText.index(line) + i])
                            i += 1


        requiredList = removeDuplicates(requiredList)
        requiredList = sorted(requiredList, key=str.lower)
        

        #open file for requiredList to be stored
        requiredFile = open("C:/Users/CBjoe/Python/pythonEx/ex7/apifix_repo/required_reading.md", "w+")

        #print list to required_reading.md file
        for item in requiredList:
            requiredFile.write("%s\n" % item)


        #push to github        
        
        pushMessage ="'git push'"
        os.chdir('./apifix_repo')
        subprocess.run(['git', 'commit', '-am', f'{pushMessage}'], shell=True)
        subprocess.run(['git', 'push'], shell=True) 


        break    

        

    # Prints an error if the URL doesn't exist
    except HTTPError as err:
        print('Url does not exist please type in a valid one! ')
        break


        



# def git_clone_test(url):

#     process = subprocess.Popen(['git', 'clone', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     if not process.stdout.read():
#         warn(process.stderr.read())
#         return False

#     return True
sys.exit()