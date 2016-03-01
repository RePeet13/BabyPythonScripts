import os, pprint, shutil
 
cwd = os.getcwd()
onlyfiles = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
 
sep = ' - '
offset = 0
 
for f in onlyfiles:
  parts = f.split(sep)
  nnewf = '.'.join([parts[0], str(int(parts[1])-offset), parts[2]])
  # shutil.move(f, newf)