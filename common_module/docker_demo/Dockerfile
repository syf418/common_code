# 基础镜像
FROM python:3.7

# 维护人
LABEL maintainer="myself"

# 注意：为了利用缓存快速重新打包，建议把一些不会更改或调整的执行动作放前面，比如包的安装
# 拷贝文件或目录到镜像中，也可用COPY指令，但不支持自动下载和解压
COPY ./python_whl/ python_whl

# 构建镜像时运行的shell命令
RUN pip3 install /python_whl/Flask-1.0.2-py2.py3-none-any.whl
# requirements里面包含要安装的包名和版本,比如：numpy==1.18.1
RUN pip3 install -r /python_whl/requirements.txt

# 拷贝文件或目录到镜像中，也可用COPY指令，但不支持自动下载和解压
COPY ./code/ code

# 声明容器运行的服务端口 
EXPOSE 8002

# 设置环境内环境变量
# ENV JAVA_HOME /usr/local/jdk1.8.0_45

# 工作目录
WORKDIR code

# 启动容器时执行的Shell命令
# CMD ["/roadLocal/start.sh"]
CMD ["python", "/code/restful_main.py"]