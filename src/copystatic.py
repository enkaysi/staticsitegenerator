import os
import shutil

def copy_static(static, public):
    if not os.path.exists(public):
        os.mkdir(public)
   
    for file in os.listdir(static):
        full_path = os.path.join(static, file)
        dest_path = os.path.join(public, file)
        if os.path.isfile(full_path):
            shutil.copy(full_path, dest_path)
        else:
            copy_static(full_path, dest_path)