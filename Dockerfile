FROM jfloff/alpine-python:3.6-onbuild
LABEL version="1.0"
LABEL author="yaaprogrammer"
LABEL description="zzu check-in script"

# 复制项目
COPY . /zzu-helper

# 复制crontab任务至/etc/cron.d
COPY ./zzu_job /etc/cron.d/zzu_job

# 修改时区并添加zzu_job内容至root任务
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && cat /etc/cron.d/zzu_job >> /var/spool/cron/crontabs/root

CMD crond -f
