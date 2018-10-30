import os, re, shutil
from lib import func, interface


class cordova:
    def __init__(self, config, platform = 'android'):
        self.c = config
        self.platform = {
            'android' : {'id':'android', 'name':'安卓', 'suffix':'apk', 'build':self.__build_android},
            'ios' : {'id':'ios', 'name':'苹果', 'suffix':'ipa', 'build':self.__build_ios}
        }[platform]
        self.c['www'] = './www'
        self.c['xml'] = "./config.xml"
        self.__xml()

    def version(self):
        if not hasattr(self, 'xml'): return None
        return re.search('widget.+?version="([^"]+)', self.xml).group(1)

    def __xml(self):
        if not 'root' in self.c or not os.path.exists(self.c['root']): return
        os.chdir(self.c['root'])  # 切换工作目录
        self.xml = func.readfile(self.c['xml'])
        self.app_name = re.search(r'[^\\/]+$', self.c['root']).group()

    def __www(self):
        if os.path.exists(self.c['www']): shutil.rmtree(self.c['www'])
        if os.path.exists(self.c['dist']): shutil.copytree(self.c['dist'], self.c['www']) # 有则重新复制

    def __level_up(self):
        if not self.c['is_level_up']: return
        part = int(self.c['is_level_up'])
        version = self.version()
        groups = re.search(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:\.(\d+))?$', version).groups()
        version_next = []
        for k, v in enumerate(groups):
            key = k + 1
            if v: version_next.append(v if key < part else '0' if key > part else str(int(v) + 1))
        version_next = '.'.join(version_next)
        xml = re.sub(r'(widget.+?version=")[^"]+', r'\g<1>' + version_next, self.xml) # 升版本
        func.writefile(self.c['xml'], xml)

    def __build_android(self):
        interface.print('正在打包安卓' + self.c['name'])
        func.loading()
        func.popen_read('cordova prepare android')
        cmd = 'cordova build android'
        if not self.c['is_debug']: # 如果是打发布包
            cmd += ' --release' # 加上发布标签
            if self.c['keystore']: # 如果有配置签名, 则对应用签名
                keystore = self.c['keystore']
                cmd += ' -- --keystore="' + keystore['path'] + '" --storePassword=' + keystore['store_password'] + ' --password=' + keystore['password'] + ' --alias=' + keystore['alias']
        stdout, stderr = func.popen_read(cmd)
        func.loading(0)
        if self.__is_build_failed(stdout): func.exit(self.c['name'] + '安卓打包失败')  # 如果打包失败, 挂起
        interface.print(self.c['name'] + '安卓打包成功')

    def __build_ios(self):
        interface.print('正在打包苹果' + self.c['name'])
        func.loading()
        func.popen_read('cordova prepare ios')
        if self.c['is_export_distribute']: # 苹果暂不自动打发布包
            func.loading(0)
        elif func.get(self.c, 'is_semi_automatic'): # 如果是半自动, 则等待手动打包后继续操作
            func.loading(0)
            is_continue = interface.wait_package()
            if not is_continue: func.exit(self.c['name'] + '苹果打包失败') # 用户终止, 退出程序
        else:
            cmd = 'cordova build ios --device'
            if not self.c['is_debug']: cmd += '' # 如果是打发布包
            if self.c['build_config']: cmd += ' --buildConfig' # 如果有配置创建配置, 则补上创建配置
            stdout, stderr = func.popen_read(cmd)
            func.loading(0)
            if self.__is_build_failed(stdout): func.exit(self.c['name'] + '苹果打包失败')  # 如果打包失败, 挂起
        interface.print(self.c['name'] + '苹果打包成功')

    def __export(self):
        if not self.c['output']: return
        output = self.c['output']
        app = self.__get_ipa_path(output)
        export = output['distribute'] if self.c['is_export_distribute'] else output['export']
        if not os.path.exists(app) or not os.path.exists(os.path.dirname(export)): return interface.print('源包路径不对或导出目录不存在, 未导出')
        shutil.copy(app, export) # 将应用复制到目标目录
        self.__clear_source() # 清除所打包
        interface.print(self.c['name'] + self.platform['name'] + '已导出到:' + export)

    def __get_ipa_path(self, output):
        # 若为半自动模式则源路径为半自动路径, 否则为debug或release路径
        self.package = output['semi_automatic'] if func.get(self.c, 'is_semi_automatic') else output['debug'] if self.c['is_debug'] else output['release']
        app = func.glob_one(self.package + '/*.' + self.platform['suffix']) # 尝试在输出目录匹配应用文件
        if app: self.package = app # 如果匹配到应用文件, 则包即为应用文件
        if app or self.platform['id'] == 'android': return self.package # 若为安卓, 则本来就是单文件
        self.package = func.glob_one(self.package + '/*') # 记录包目录以供之后清除
        return self.package if self.c['is_export_distribute'] else func.glob_one(self.package + '/*.' + self.platform['suffix']) # 如果是发布包, 则源路径为整个包, 否则为包中匹配的ipa文件

    def __clear_source(self):
        os.remove(self.package) if os.path.isfile(self.package) else shutil.rmtree(self.package) # 如果是包目录, 则删除目录, 否则删除文件

    def __is_build_failed(self, stream):
        return not stream or not re.search(r'^BUILD\s+SUCCESSFUL\b|\bEXPORT\s+SUCCEEDED\b', stream, re.M)

    def __build(self):
        if not 'root' in self.c or not os.path.exists(self.c['root']): func.exit('\n' + self.c['name'] + self.platform['name'] + '打包环境不存在')
        self.__www()
        self.__level_up()
        self.platform['build']()
        self.__export()

    @staticmethod
    def build(config, name = None, dist = None):
        config['name'] = name
        config['dist'] = dist
        if (config['platform'] & 1) and 'android' in config: cordova(dict(config.pop('android'), **config), 'android').__build() # 打包安卓
        if (config['platform'] & 2) and 'ios' in config: cordova(dict(config.pop('ios'), **config), 'ios').__build() # 打包苹果