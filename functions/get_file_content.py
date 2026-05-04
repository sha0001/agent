import os

#importing types for schema 

from google.genai import types

def get_file_content(working_directory,file_path): 


    #get absolute path of wd

    try: 
        abs_path = os.path.abspath(working_directory)
    except: 
        return 'Error: getting absolute path'

    #construct full path to target file

    try: 
        full_path = os.path.join(abs_path,file_path) 
    except: 
        return 'Error: constructing full path' 

    #protect against shenanigans

    try: 
        target_file = os.path.normpath(full_path)
    except: 
        return 'Error: shenanigans' 


    #check if target_file is within absolute working dir

    try: 
        valid_target_file = os.path.commonpath([abs_path,target_file]) == abs_path

    except: 
        return 'Error: checking validity' 

    # if target not in wd, return error

    if valid_target_file == False: 
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

   # if target doesn't exist, return error 

    if os.path.isfile(target_file) == False: 
        return 'Error: Target file does not exist'



    # read the file and return contents as a string. Limit to 10,000 characters. 
    try: 
        with open(target_file, "r") as f: 
            content = f.read(10000)
            if f.read(1): 
                content += f'[...File "{file_path}" truncated at 10,000 characters]'
            print(f'length of content = {len(content)}') 
            
    except:
        return 'Error: reading contents'

    return content

#end of main function


# declaration schema

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content in a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file to be read, relative to the working directory",
            ),
        },
    ),
)





