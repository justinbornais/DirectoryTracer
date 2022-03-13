import os

def indexFolder(directory):
    folder_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))] # Source: https://www.codegrepper.com/code-examples/python/get+list+of+folders+in+directory+python
    if len(folder_list) > 0:
        
        for i in range(len(folder_list)):
            indexFolder(os.path.join(directory, folder_list[i]))
    
    returned_value = os.system("tree -H . > index.html")
    print(returned_value)


indexFolder(os.curdir)