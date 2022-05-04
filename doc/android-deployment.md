# 安卓手机部署

优势:

- 自动定时运行
- 没有开销

缺点:

- 需要占用手机后台，耗电
- 需要学习一点点东西

## 安装Termux

可以在[F-Droid](https://f-droid.org/zh_Hans/)上下载，或Github仓库[termux-app](https://github.com/termux/termux-app/releases/)

其他来源请自行辨别

## F-Droid换源(可选)

[清华源F-Droid镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/fdroid/)

复制该页面的第一个链接，打开F-Droid

设置->存储库->"+"->启用

关闭官方镜像即可

## Github加速(可选)

[FastGithub](https://github.com/dotnetcore/FastGithub/releases/)

在Windows下很方便使用，解决Github时常无法访问的问题。如果直接在Github Release下载Termux的apk太慢可以考虑一下。

## 学习Linux基本操作

[看完这篇Linux基本的操作就会了-知乎](https://zhuanlan.zhihu.com/p/36801617)

## 学习Vim基本操作

[Linux Vim基本操作(文件的打开和编辑)](http://c.biancheng.net/view/805.html)

## 安装Vim

```bash
pkg install vim
```

修改默认编辑器

```bash
vim ~/.bashrc
```

添加这一行

```bash
export EDITOR="/data/data/com.termux/files/usr/bin/vim"
```

添加环境变量至当前Shell  (或者直接重启Termux也可以, 就不用输这个了)

```bash
source ~/.bashrc
```

## Termux换源(可选)

[清华源 Termux 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/termux/)

## 安装必要环境和工具

```bash
pkg update
pkg install python git openssl cronie
```

## pip换源(可选)

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 克隆仓库

```bash
git clone https://github.com/yaaprogrammer/zzu-helper.git
```

## 安装项目依赖

```bash
pip install -r ./zzu-helper/requirements.txt
```

## 配置定时任务

[学习crontab语法](https://www.runoob.com/linux/linux-comm-crontab.html)  

```bash
crontab -e
```

示例: 每天4:20执行一次填报

```cronie
20 4 * * * /data/data/com.termux/files/usr/bin/python /data/data/com.termux/files/home/zzu-helper/main.py -n
```

## 启动定时任务服务

```bash
vim ~/.bash_profile
```

添加以下内容:

```bash
if ! pgrep -f "crond" >/dev/null; then
echo "[Starting crond...]" && crond && echo "[OK]"
else
echo "[crond is running]"
fi
```

这样每次重启termux就可以自启动`crond`定时任务服务了。

输入`pgrep crond`就可以检查crond是否启动，如果正在运行就会出现一行数字，这是crond进程的ID。

## 编辑配置文件

```bash
cd zzu-helper
vim config_custom.yml
```

最小配置

```yaml
zzu:
    username: xxxxxxx
    password: xxxxxxx
```

具体见[配置文件详解](./config.md)

## 开启邮件服务(可选)

[邮件服务配置](./mail-settings.md)

## 防止Termux被清理

根据自己的手机选择合适策略，防止Termux进程被杀掉

我的手机是: 设置->应用启动管理->Termux->允许后台活动，并关闭省电模式
