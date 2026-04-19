# up to step 3. Line 44


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


    # if target doesn't exist, return error 

    if os.path.isfile(target_file) == False: 
        return 'Error: Target file does not exist'


