# Drunk Cordova Package Tool

Drunk Cordova打包工具(DCPT)是一款Cordova自动打包工具，它能帮您从前端打包到APP打包，再到部署测试版或导出到待发布目录，当我们项目比较多，或测试比较频繁时，此工具能帮你自动完成繁琐的操作流程。

Cordova打包流程
* 拉取最新前端项目
* 将接口改为线下测试版或发布版
* 打包前端代码
* 将前端包拷到Cordova项目
* 更新App版本等
* 打包签名
* 导出到测试环境或待发布目录

DCPT能自动帮你完成上述流程，有效降低人员操作的出错率，提高工作效率。当然，本工具仅仅帮你将手工活自动化，你需要自己搭建配置好各种环境（前端环境、cordova环境、android环境、xcode环境等），至少手动完成一次打包流程。

## 使用说明

首先你得配置好Python3的环境以及各种打包工具的环境。

#### 以默认配置打包
```bash
python3 main.py
```
此命令会读取data目录下的config.json配置

#### 以特定配置文件打包(如ios)
```bash
python3 main.py ios
```
加上ios参数，则会读取data目录下的config-ios.json配置

#### 参数说明
```json
{
    "apps" : [
        {
            "name" : "微窝房产", // 应用名
            "frontend" : { // 前端项目配置
                "root" : "F:/App/sale-app-vue", // 前端根目录
                "dist" : "./dist", // 前端打包目录
                "vcs" : { // 版本控制配置
                    "pull" : "git pull", // 拉取新代码命令
                    "checkout" : [ // 拉取新代码前可选的项目目录整理命令
                        "git reset --hard head",
                        "git checkout develop"
                    ]
                },
                "conf" : {
                    "path" : "./src/config/index.js", // 接口配置文件
                    "production" : "weiwo.info", // 发布版接口主机地址
                    "development" : "192.168.1.2:9001" // 线下开发版接口主机地址
                },
                "npm" : {
                    "build" : "npm run build" // 前端打包命令
                }
            },
            "cordova" : { // cordova打包配置
                "android" : { // 打包安卓配置
                    "root" : "F:/App/#package/weiwo-fangchan", // cordova项目根目录
                    "keystore" : { // 签名配置
                        "path" : "./weiwo-fangchan.keystore", // 签名密匙路径
                        "store_password" : "123456", // 签名密匙密码
                        "password" : "123456",
                        "alias" : "weiwo"
                    },
                    "output" : {
                        "release" : "./platforms/android/build/outputs/apk/release/android-release.apk", // 发布版cordova打包默认导出路径
                        "debug" : "./platforms/android/build/outputs/apk/debug/android-debug.apk", // 调试版cordova打包默认导出路径
                        "export" : "X:/App/Weiwo/web/public/temp/app/debug/fangchan/app.apk", // 导出到线下测试环境的路径
                        "distribute" : "F:/App/#release/#app/fangchan.apk" // 导出到待发布路径
                    }
                },
                "ios" : { // 打包ios配置
                    "root" : "/App/weiwo-fangchan", // 项目根目录
                    "build_config" : "./build.json", // ios相关证书配置(详见cordova build ios)
                    "is_semi_automatic" : 0, // 是否全自动打包
                    "output" : {
                        "release" : "./platforms/ios/build/device", // cordova打包默认导出路径
                        "semi_automatic" : "/Users/drunk/Documents/#app", // 半自动打包xcode导出ipa路径
                        "export" : "/Volumes/F/App/Weiwo/web/public/temp/app/debug/fangchan/app.ipa", // 导出到线下测试环境的路径
                        "distribute" : "/Users/drunk/Library/Developer/Xcode/Archives" // 导出到待发布路径
                    }
                }
            }
        }
    ]
}
```

Windows环境不能打包ios，OSX环境可以打包苹果和安卓，所以可以在OSX上配置XCode与android环境，即可同时打包打包安卓与苹果，当然也可以安卓苹果分别打包。

## 工具预览图
![DCPT](https://www.xinwen1.com/res/temp/dcpt-screen.png)