from lib.config import set as cset
from lib.config import data as config
from lib.cordova import cordova

py_input = input
py_print = print

def action():
    cset('action', input('''欢迎使用Drunk Cordova打包工具\n\n请选择您要执行的操作\n
1:创建发行版包
2:创建调试包
0:不创建\n
您要执行的是[1]:''', {1,2,0}, 1, '')) # 记录要执行的操作

def platform():
    import platform as pf
    if 'Windows' in pf.uname(): return cset('platform', 1) # 如果是Windows平台, 则无需选择, 只能打包Android应用
    cset('platform', input('''\n请选择应用平台\n
1:安卓
2:苹果
3:全部\n
您要打包[3]:''', {1, 2, 3}, 3)) # 记录要打包的平台

def frontend():
    cset('frontend_action', input('''\n请选择前端项目打包方式\n
1:打包为生产版
2:打包为开发环境版
0:不打包\n
您要打包为[2]:''', {0,1,2}, 2))  # 记录是打生产版包还是开发测试版
    cset('is_export_distribute', 0 if config['frontend_action'] == 2 else input('是否导出到发行目录(1/0)[1]:', {0, 1}, 1))

def apps():
    print('''\n您的应用信息\n''')
    for item in config['apps']:
        version = cordova(item['cordova']['android']).version() if 'android' in item['cordova'] else None  # 取APP当前版本
        if not version and 'ios' in item['cordova']: version = cordova(item['cordova']['ios']).version() # 若未取到安卓的, 则尝试取苹果
        py_print(item["name"] + ' (v' +version+ ')')
    for index,item in enumerate(config['apps']):
        app_input(config['apps'][index])

def app_input(item):
    item['is_build'] = input('是否创建' +item['name']+ '(1/0)[1]:', {0, 1}, 1)
    if item['is_build']: item['cordova']['is_level_up'] = input('是否升级版本(1/0)[0]:', {0, 1}, 0, '') # 创建才可能更新版本
    item['cordova']['platform'] = config['platform']
    item['cordova']['is_debug'] = config['action'] == 2
    item['cordova']['is_export_distribute'] = config['is_export_distribute']
    item['frontend']['is_production'] = config['frontend_action'] == 1

def wait_package():
    return input('请打包并导出应用到对应目录后按回车继续或者输入0终止(1/0)[1]:', {0, 1}, 1)

def input(label, allow = set(), default = None, pre = "\n"):
    value = py_input(pre + label)
    if str.isnumeric(value): value = int(value) # 若输入的数字字符串, 则强转整型
    if value == '': value = default # 若未输入值, 则设为默认值
    if allow: # 若设置了安全输入值, 则输入值必须在此范围, 否则需重新输入
        if not value in allow: input(label, allow, default, pre)
    return value

def print(string, pre='\n'):
    py_print(pre + string)

def build():
    print('\n开始执行打包操作')
    from lib.frontend import frontend
    for item in config['apps']:
        if not item['is_build']: continue
        py_print('')
        if config['frontend_action']: frontend(item['frontend'], item['name']).build() # 是否打包前端项目
        if config['action']: cordova.build(item['cordova'], item['name'], item['frontend']['root'] + item['frontend']['dist'].lstrip('.')) # 是否打包Cordova应用
    print('脚本执行完毕')