#file operations

#file = open("p_file.txt")

with open("p_file.txt","r") as file:
    file_content = file.read() #read all the file content
    print(file_content)