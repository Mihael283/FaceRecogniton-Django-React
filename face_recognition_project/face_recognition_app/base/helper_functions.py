import os
import tempfile


def create_temp(file):
    ### write the data to a temp file
    tup = tempfile.mkstemp() # make a tmp file
    f = os.fdopen(tup[0], 'wb') # open the tmp file for writing
    f.write(file.read()) # write the tmp file
    f.close()
    ### return the path of the file
    filepath = tup[1] # get the filepath
    return filepath

def delete_file(file):
    if os.path.isfile(file):
        os.remove(file)

def create_dir(static_path,name):
    path = os.path.join(static_path, name)
    path_exists = os.path.exists(path)
    if(path_exists is False):
        os.mkdir(path)
        