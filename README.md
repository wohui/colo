# 说明

这是一个基于Python+Locust+Grafana+Vue的性能测试平台，追求简单化执行性能测试，平台化集成脚本管理、场景配置、压力配置、任务管理、监控报警等
是使用Python+Locust搭建一个性能测试平台，也想通过Grafana做个监控大盘的，会是一个不错的选择。
（开发中）

* 简单
* 平台化
* 易扩展

# 项目架构

## 技术栈

前端：vue3+element-ui

后端：django+mysql

性能引擎：locust

监控系统：Grafana+postgressql（timescale）

## 架构图

![系统简要架构图](assets/system_framework.png)

# 部署

## 部署基础组件

1.部署Grafana+postgressql，推荐使用docker部署，项目下有docker-compose.yml文件，可参考部署
2.建好数据库/assets/timescale_schema.sql有脚本
3.部署Grafana，导入好监控指标

参考：locust_plugins [https://github.com/SvenskaSpel/locust-plugins/tree/master/locust_plugins/dashboards](https://)

## 部署前端

```bash
# 进入前端项目目录
cd ui-colo
# 安装前端依赖
npm install
# 运行前端服务
npm run dev
# 打包预发布环境
npm build:stage

# 打包正式环境
npm build:prod

```

## 部署后端

```bash
# 安装依赖
pip install -r requirements.txt
# 建colo需要的库表
##安装一个mysql库，具体用户名等信息在setting.py配置
# 运行一下2个命令，生成所需的表
python manage.py makemigrations api
python manage.py migrate
# 运行后端服务
python3 manage.py runserver 0.0.0.0:8000

```

# 功能展示

浏览器打开访问localhost:3333

### 脚本管理

![image.png](assets/image_script.png)
脚本暂时还没规划好是保存在数据库还是在git上，TODO

### 测试计划

![image.png](assets/image_plan.png)

### 测试记录

开始压测后，会在这里生成一个记录，可以停止和打开监控大盘

![image.png](assets/image_record.png)

### 监控大盘展示

生成唯一的testplan,交给grafana来聚合，展示

![image.png](assets/image_monitor1.png)

![image.png](assets/image_monitor2.png)

![image.png](assets/image_monitor3.png)

# 平台流程

# 手动运行locust

```shell
 locust --timescale --headless --override-plan-name 0108
 #运行locust 输出到postgressql
```

# 🙏 致谢/Acknowledgments

* [locust-plugins](https://github.com/SvenskaSpel/locust-plugins)
* [v3-admin](https://github.com/un-pany/v3-admin-vite/)

# TODO

* [ ]  脚本上传管理
* [ ]  分布式执行

# 注意点记录：

mysqlclient无法安装，在settings使用pymysql转换
locust-plugins依赖问题
locustfile脚本，需要增加pgsqldb的环境变量配置
docker化部署pgsql+grafana
locustfile要自动生成，还要分发到每个压力机上

# 部署过程环境遇到的问题

## docker 部署在另一台局域网的macmini上，远程访问，需要开启ssl

[Service]
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock

2、Docker进程监听2375端口，接受远程访问。但是在MacOS下，却无法使用。需要做如下两步配置：

brew install socat
socat TCP-LISTEN:2375,reuseaddr,fork UNIX-CONNECT:/var/run/docker.sock &

报错了，网上找到解决方案

使用socat镜像开启服务

docker run -d --name socat --restart always -p 2375:2375 -v /var/run/docker.sock:/var/run/docker.sock alpine/socat tcp-listen:2375,fork,reuseaddr unix-connect:/var/run/docker.sock\

配置

vi ~/.bash_profile

export DOCKER_HOST=tcp://localhost:2375

重启生效

source .bash_profile
