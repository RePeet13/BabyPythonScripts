import os, pprint, shutil
 
cwd = os.getcwd()
onlyfiles = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
 
sep = ' - '
season = 1
offset = 0
## TODO pad zeros based on length of onlyfiles

for f in onlyfiles:
    print '------'
    print f
    if any(i in f for i in sep):
        parts = f.split(sep)
        newf = '.'.join([parts[0], 'S'+str(season)+'E'+str(int(parts[1])-offset), parts[3]])
        print newf
#       shutil.move(f, newf)
