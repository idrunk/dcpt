import os, re
from lib import func, interface


class frontend:
    def __init__(self, config, name):
        self.c = config
        self.name = name
        os.chdir(self.c['root'])

    def __checkout(self):
        for cmd in self.c['vcs']['checkout']: func.popen_read(cmd)

    def __pull(self):
        self.__checkout()
        stdout, stderr = func.popen_read(self.c['vcs']['pull'])
        if self.__is_git_failed(stdout): func.exit(self.name + '拉取失败') # 如果拉取失败, 挂起
        interface.print(self.name + '拉取成功')

    def __pre_build(self):
        file = self.c['conf']['path']
        script = func.readfile(file)
        source = self.c['conf']['development'] if self.c['is_production'] else self.c['conf']['production']
        target = self.c['conf']['production'] if self.c['is_production'] else self.c['conf']['development']
        script = str.replace(script, source, target)
        func.writefile(file, script)

    def __build(self):
        interface.print('正在打包' + self.name + '前端代码')
        func.loading()
        stdout, stderr = func.popen_read('npm run build')
        func.loading(0)
        if self.__is_build_failed(stdout): func.exit(self.name + '前端代码打包失败') # 如果打包失败, 挂起
        interface.print('前端代码打包成功')

    def __is_git_failed(self, stream):
        return not stream or re.search(r'^(?:fatal|error):|\bfailed;', stream)

    def __is_build_failed(self, stream):
        return not stream or not re.search(r'\bBuild\s+complete\.', stream)

    def build(self):
        self.__pull()
        self.__pre_build()
        self.__build()