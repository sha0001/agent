import os 
from google.genai import types

def write_file(working_directory, file_path, content): 
    

    # get absolute path of wd

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
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'


    # if file_path points to an existing directory return an error
    if os.path.isdir(target_file): 
        return f'Error: Cannot write to "{file_path}" as it is a directory' 

    # make sure that all parent directories for file_path exist. 
    # exist_ok means that it won't do anything if they already exist

    os.makedirs(os.path.dirname(target_file), exist_ok=True) 
    

    #write content variable to file
    try: 
        with open(target_file, "w") as f: 
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except: 
        return 'Error writing to file' 


#end of main function


# declaration schema

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite content in a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file where content is to be written, relative to the working directory",
            ),
        },
    ),
)






