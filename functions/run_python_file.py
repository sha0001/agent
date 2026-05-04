import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, *args ): 

    
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
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'


    # if file_path doesnt point to a file  return an error
    try: 
        if os.path.isfile(target_file) == False: 
            return f'Error: "{file_path}" does not exist or is not a regular file' 
    except: 
        return 'Error: checking if a file' 
    
    # if file name doesn't end with .py, return an error
    try:
        if file_path.endswith('.py') == False: 
            return f'Error: "{file_path}" is not a Python file' 
    except: 
        return f'Error: checking file extension'

    # build the command to run 
    command = ["python", target_file]
    for arg in args: 
        command.extend(*args)

    # use subprocess to run command 
    try: 
        sub_output = subprocess.run(command, capture_output=True, timeout=30, text = True)
        output_str = []
        if sub_output.returncode != 0: 
            "\n".join(output_str,f'Process exited with code {sub_output.returncode}')
        if sub_output.stdout==None:
            if sub_output.stdin==None: 
                sub_output.append('No output produced') 
        else: 
            output_str.append(f'STDOUT:{sub_output.stdout}')
            output_str.append(f'STDERR: {sub_output.stderr}') 

        return "\n".join(output_str)
    except Exception as e: 
        return f'Error: executing Python file {e}' 


# End of main function


# declaration schema

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files in a specified directory relative to the working directory, using provided optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the python file to be run, relative to the working directory",
            ),
        },
    ),
)






