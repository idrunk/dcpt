import sys, os, json
from lib import func

cwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(cwd)
file = '../data/config-' +sys.argv[1]+ '.json' if sys.argv and len(sys.argv) > 1 else '../data/config.json'
if not os.path.exists(file): func.exit('配置文件不存在')

content = func.readfile(file)
data = json.loads(content)

del file,content

def set(key, value):
    data[key] = value

def get(key):
    return data[key] if key in data else None