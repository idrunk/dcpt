data = {
    "a" : {
        "b" : 123,
    },
    "c" : 456
}

print(dict(data.pop("a") , ** data))

print(data['a'] if 'a' in data else data['c'])

class t:
    def __tttt(self):
        return 'dsadsadas'

    def __getitem__(self, *args):
        print(args)

    def var(self):
        map = {'aaa':self.__tttt}
        print(map['aaa']())

t().var()

import glob

def glob_one(path):
    for name in glob.glob(path): return name

print(glob_one(glob_one(r'Y:\Users\drunk\Documents\*') + '/*.ipa'))

print(1 if 0 else 2 if 0 else 3)

import re

groups = re.search(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:\.(\d+))?$', r'1.4.1.5').groups()
type = 2
version = []
for k, v in enumerate(groups):
    key = k + 1
    if v: version.append(v if key < type else '0' if key > type else str(int(v) + 1))

print(".".join(version))