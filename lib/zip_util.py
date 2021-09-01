import zipfile
import os

# Original:
# http://stackoverflow.com/a/6078528
#
# Call `zipit` with the path to either a directory or a file.
# All paths packed into the zip are relative to the directory
# or the directory of the file.

def zip(path, archname):
    archive = zipfile.ZipFile(archname, "w", zipfile.ZIP_DEFLATED)
    if os.path.isdir(path):
        _zippy(path, path, archive)
    else:
        _, name = os.path.split(path)
        archive.write(path, name)
    archive.close()
    
def _zippy(base_path, path, archive):
    paths = os.listdir(path)
    for p in paths:
        p = os.path.join(path, p)
        if os.path.isdir(p):
            _zippy(base_path, p, archive)
        else:
            archive.write(p, os.path.relpath(p, base_path))