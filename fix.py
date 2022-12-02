import subprocess, shlex
import sys, os.path

filelist = set()
for path in (sys.argv[1:] or [os.path.curdir]):
    if os.path.isfile(path) or os.path.islink(path):
        filelist.add(os.path.relpath(path))
    elif os.path.isdir(path):
        for root, subdirs, files in os.walk(path):
            if '.git' in subdirs:
                subdirs.remove('.git')
            for file in files:
                filelist.add(os.path.relpath(os.path.join(root, file)))

mtime = 0
gitobj = subprocess.Popen(shlex.split('git whatchanged --pretty=%at'),
                          stdout=subprocess.PIPE)
for line in gitobj.stdout:
    line = line.decode('ascii').strip()
    if not line: continue

    if line.startswith(':'):
        file = os.path.normpath(line.split('\t')[-1])
        if file in filelist:
            filelist.remove(file)
            #print mtime, file
            os.utime(file, (mtime, mtime))
    else:
        mtime = int(line)

    # All files done?
    if not filelist:
        break