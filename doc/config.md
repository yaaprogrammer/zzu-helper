# 配置文件详解

## 推荐配置方法

在项目根目录新建一个`config_custom.yml`配置文件，在该文件中同级同名配置会覆盖`config.yml`中的默认配置。这种配置方法可以让你的自定义配置不会在`git pull`后被覆盖。

示例:

```bash
vim config_custom.yml
```

```yaml
zzu:
    username: xxxxxxx
    password: xxxxxxx
```

## 邮件服务相关配置

详细配置方法在 [邮件服务配置](./mail-settings.md)

```yaml
smtp:
  host: smtp.qq.com # smtp服务器主机域名
  user: xxxxx@qq.com # 用户名
  password: xxxxx # 密码/授权码
  port: 465 # smtp端口
  ssl: true # 是否使用SSL加密
  message:
    from: ZZU自动填报小助手 # 发件人昵称
    to: xxx # 收件人昵称
    receivers: # 收件人，可以添加多个
    - xxxxxx@qq.com 
    # - xxxxxx@qq.com
```

## 网络相关配置

```yaml
crawler:
  headers:
      ua: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36 # 伪装为浏览器的请求
  timeout: 21 # 超时时间秒数
  verify: false # ZZU填报网站SSL有些问题，需要关闭SSL验证，否则无法正常请求.
  retry:
    times: 3 # 网络错误重试次数，均失败后抛出错误
  delay:
    min: 0 # 每次请求前随机等待最小秒数
    max: 0 # 每次请求前随机等待最大秒数
```

## 主程序重试次数配置

```yaml
retry:
  times: 3  # 主程序重试次数
```

## 账号相关配置

```yaml
zzu:
  username: xxxxxxx  # 你的学号
  password: xxxxxxx  # 你的密码
```

## 响应文本中相应行为的标志

即在页面中可以看到的，证明该行为发生的文本

```yaml
flag:
  profile: 今日您已经填报过了 # 在个人资料界面表示已填报的标志
  submit: 感谢您今日上报 # 填报成功的标志
  resubmit: 你今日的健康状态上报信息已通过审核 # 重复提交的标志
  fail: 提交失败 #填报失败的标志
```

## 正则表达式相关配置

从Html中提取信息时使用的正则表达式，便于网页结构简单变动时的修改

```yaml
pattern:
  login_iframe: (?<=iframe name="my_toprr" src=").*?(?=")
  login_url: (?<="POST" action=").*?(?=")
  unknown_key: (?<=input type="hidden" name=").*?(?=")
  unknown_value: (?<=input type="hidden" name=".*?" value=").*?(?=")
  redirect_url: (?<=location=").*?(?=")
  user_profile_url: (?<=id="zzj_top_6s" src=").*?(?=")
  sid: (?<=input type="hidden" name="sid" value=").*?(?=")
  ptopid: (?<=ptopid=).*?(?=&)
  fun18: (?<=input type="hidden" name="fun18" value=").*?(?=")
```

## Url相关配置

Url如果变动可以直接修改此处

```yaml
url:
  base: http://jksb.zzu.edu.cn/
  post: https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb
```
