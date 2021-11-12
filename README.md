# layout新版开发说明

仓储设计自动化第二版web服务端python代码仓库

## 项目结构
项目按如下结构排布

**单机**

```
../
 └──web
 └──web-server
 └──core
 └──tools
 └──cad
 └──dwg2dxf
 └──core
 └──3d 
```

**接入云服务**

```
../
 └──web
 └──web-server
 └──core
 └──tools
 └──cad
 └──dwg2dxf
 └──core
 └──3d 
 └──wda-cloud
 └──wda-auth-decorators
```

**参数配置**

```
端口： 8008
dwg 转 dxf server 端口： 8001
docker 网关： 172.17.0.1
nginx port: 38088
nginx username: shucheng
nginx port: Shucheng@2021Shanghai
```

## 数据库
默认使用sqlite作为数据库， 无需安装数据库

## 项目依赖

### 所需docker镜像

`cyborg` 为项目代号， 类似 `beaver`

- cyborg/webserver
- cyborg/core
- cyborg/cad
- cyborg/node14

**安装前需做**

#### 手动添加 ezdxf 依赖文件

直接pip install ezdxf会不兼容，需要手动下载安装指定版本

build docker 时需要手动将 ezdxf.tar.bz2 放入 /web-server/docker 目录下

安装文件及说明参考此  [issue](http://gitlab.shucheng-ai.com/layout/web-server/issues/11) 

**安装方式**

1. 直接通过 [main](http://gitlab.shucheng-ai.com/layout/main) 项目进行安装， 参考main项目[readme](http://gitlab.shucheng-ai.com/layout/main/blob/master/README.md)。
2. 单独构建，分别在 `web`, `web-server`, `core`, `cad` 项目下构建 docker， `bash build.sh`
3. 在国外时添加 `en` 参数安装无换源版docker

- `bash build.sh en`
- `git submodule foreach bash build.sh en`

3d项目所需docker和web项目为同一个，无需单独构建

### 编译core、cad、web、3d

1. 直接在main下进行编译 `git submodule foreach bash update.sh`
2. 独立编译各个项目

#### 2.1 编译core、cad

```
cd core # cad
bash update.sh
```

#### 2.2 编译web

```
cd web
bash npm_install.sh
bash update.sh
```

#### 2.3 编译3d

```
cd 3d
cd beaver-3d
bash npm_install.sh
bash npm_build.sh
```

### run docker

**开发说明**

``` 
三种模式

默认模式：
使用wsgi后台运行
bash run.sh 

开发者模式：
使用flask runserver，会打印消息，但print会有滞后
bash run.sh dev
```


### shell 模式

`web-server` 和 `web` 提供了shell模式，可以直接将docker当作虚拟机使用

**web-server**

在shell模式下，直接进入 `/www` 路径， 就能直接对 web-server, core, cad, tools 项目进行操作

```
bash run.sh shell
cd www
```

**web**

在shell模式下，直接进入 `/web/app` 路径， 就能直接对 web 项目进行 npm 脚本操作

```
bash start_docker.sh shell
```

#### update docker

```
bash update_docker.sh
```
