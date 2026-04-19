import os 


def get_files_info(working_directory,directory="."):
    
# get absolute path of working directory
    try: 
        abs_path = os.path.abspath(working_directory)    
    except: 
        return 'Error: getting absolute path' 

    #construct full path to target directory
    
    try: 
        full_path = os.path.join(abs_path,directory)
    except: 
        return 'Error: constructing full path'


    #protect against shenanigans
    try: 
        target_dir = os.path.normpath(full_path)
    except: 
        return 'Error: shenanigans'

    #check if target_path is within absolute working dir. 
    
    try: 
        valid_target_dir = os.path.commonpath([abs_path,target_dir]) == abs_path
    except: 
        return 'Error: checking validity' 

    #if target not in wd, return an error string

    if valid_target_dir == False: 
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # if directory is not a directory, return error string

    try: 
        is_dir = os.path.isdir(target_dir) 
    except: 
        return 'Error: checking is_dir'

    if is_dir == False: 
        return f'Error: "{directory}" is not a directory'
    
    # initialise contents_string

    contents_string = "" 


    # get directory contents
    
    try: 
        contents = os.listdir(target_dir)
    except: 
        return 'Error: getting contents'

    # gather name file size and whether a directory. 

    for item in contents: 
        #try:
        file_size = os.path.getsize(f'{target_dir}/{item}') 
        #except: 
        #    return 'Error: getting size'

        contents_string += f'- {item}: file_size={file_size} bytes, is_dir={os.path.isdir(f'{target_dir}/{item}')}\n'
    return contents_string
        
