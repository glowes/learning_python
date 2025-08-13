
fileReader = "currentMem.txt"
fileWritter  = "exMem.txt"



def cleanFiles(currentMem, exMem):
    # TODO: Open the currentMem file as in r+ mode
        #TODO: Open the exMem file in a+ mode
    
        with open(currentMem,"r+") as currentMFile:
            with open(exMem,"w+") as exMFile:
                #first line  goes in
                a_line = currentMFile.readline()
                exMFile.write(a_line)
           
                for a_line in currentMFile:
                    if "no" in a_line:
                        exMFile.write(a_line)
                
                exMFile.seek(0,0)
                with open(exMem,"r+") as exMemFile:
                    print(f"exM result:\n\n {exMFile.read()}")


cleanFiles(fileReader,fileWritter)