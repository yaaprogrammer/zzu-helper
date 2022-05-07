# Docker 部署

1. `zzu_job` 为cron定时任务，修改为你想要的时间
2. `vim config_custom` 修改默认配置

    ```yaml
    smtp:
        enable: false # 关闭邮件服务
    zzu:
        username: xxxxxxx # 你的学号
        password: xxxxxxx # 你的密码
    ```

3. `docker build -t zzu-helper:v1.0 .`  构建镜像
4. `docker run -d zzu-helper:v1.2` 运行容器
