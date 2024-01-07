import docker
import docker
client = docker.DockerClient('tcp://127.0.0.1:2375')

def docker_test():
# 创建一个grafana
    try:
        # 从指定镜像中创建并启动新容器
        container = client.containers.create(
        image='cyberw/locust-grafana:3',
        ports={'3000/tcp': 30001},
        name='colo_grafana_300001',
    )
        container.start()
        print("成功创建容器！")
    except Exception as e:
        print("创建容器时发生错误：", str(e))
    finally:
        # 关闭与 Docker 守护进程的连接
        client.close()