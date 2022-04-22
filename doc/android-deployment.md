# 安卓手机部署

优势:

- 自动定时运行
- 没有开销

缺点:

- 需要占用手机后台，耗电
- 需要学习一点点东西

## 安装Termux

可以在`F-droid`上下载，或Github仓库[termux-app](https://github.com/termux/termux-app/releases/)

其他来源请自行辨别

## 安装Python

```bash
pkg install python
```

## 安装Git

```bash
pkg install git
```

## 克隆仓库

```bash
git clone https://github.com/yaaprogrammer/zzu-helper.git
```

## 安装依赖

```bash
cd zzu-helper
pip install -r requirements.txt
```

## 配置定时任务

1. 查找Python命令的绝对位置

    ```bash
    whereis python
    ```

    ```bash
    python: /data/data/com.termux/files/usr/bin/python /data/data/com.termux/files/usr/share/man/man1/python.1.gz
    ```

2. 安装cronie

    ```bash
    pkg install cronie
    ```

3. 编辑配置

    [学习crontab语法](https://www.runoob.com/linux/linux-comm-crontab.html)  
    [学习vi基本操作](http://c.biancheng.net/vi/)

    ```bash
    cronie -e
    ```

    ```cronie
    20 4 * * * /data/data/com.termux/files/usr/bin/python /data/data/com.termux/files/home/zzu-helper
    ```

## 防止Termux被清理

根据自己的手机选择合适策略，防止Termux进程被杀掉
