import asyncio
import subprocess

from os import listdir
from os.path import isfile, join

# mypath = "/home/aschieb/Desktop/out_perso/McrLive/out"
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


# Using system() method to
# execute shell commands


def convert(tmpdir, f):
    subprocess.run(f'ffmpeg -loglevel error -fflags +discardcorrupt -i {tmpdir}/{f} -vn -ar 44100 -ac 2 -b:a 192k {tmpdir}/unc_{f}', shell=True)
    


def convert_folder(tmpdir):
    ret = -1
    onlyfiles = [f for f in listdir(tmpdir) if isfile(join(tmpdir, f))]
    for i,f in enumerate(onlyfiles):
        if not f.startswith('unc_'):
            convert(tmpdir, f)
    
