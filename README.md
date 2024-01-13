# 说明
这是一个基于Python+Locust+Grafana+Vue 追求简单化执行性能测试，平台化集成脚本生成、执行配置、任务管理、监控报警

* 简单
* 平台化
* 易扩展

# 架构

# 部署

## 服务端

### 安装依赖

```shell
pip install -r requirements.txt
```
## 部署postgres+grafana
推荐docker部署，项目下有docker-compose文件，直接部署[docker-compose.yml](docker-compose.yml)
## 部署前端服务
##
# 运行
## 平台操作
# 手动运行locust

```shell
 locust --timescale --headless --override-plan-name 0108
```



# 平台流程

# 注意点：

mysqlclient无法安装，在settings使用pymysql转换
locust-plugins依赖问题
locustfile脚本，需要增加pgsqldb的环境变量配置
docker化部署pgsql+grafana
locustfile要自动生成，还要分发到每个压力机上

| 分布式

部署环境遇到的问题

1、docker 远程访问，需要开启ssl
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
