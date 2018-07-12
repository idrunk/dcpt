import os, sys, glob

def exit(message = None):
    if message != None: print(message)
    os.system('pause')
    sys.exit()

def get(config, key):
    return config[key] if config and key in config else None

def glob_one(path):
    for name in glob.glob(path): return name

def readfile(path):
    fd = open(path, 'r', encoding='utf-8')
    content = fd.read()
    fd.close()
    return content

def writefile(path, content):
    fd = open(path, 'w', encoding='utf-8')
    len = fd.write(content)
    fd.close()
    return len

def popen_read(cmd):
    from subprocess import Popen, PIPE
    stdout, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    return (bytes.decode(stdout), bytes.decode(stderr))

__thread = None
__is_loading = 0
def loading(is_loading = 1):
    global __is_loading, __thread
    __is_loading = is_loading
    if is_loading == 0:
        __thread.join()
        print()
        return
    import time, threading
    def __loading():
        cnt = 0
        while __is_loading == 1:
            cnt += 1
            print('.', end='' if cnt % 60 else '\n', flush=True)
            time.sleep(1)
    __thread = threading.Thread(target=__loading)
    __thread.start()