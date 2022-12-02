* [舙](http://rhel.9mdqf2fo6vsi.instruqt.io:8080/)

[Linux Alpine](https://www.cnblogs.com/jackadam/p/9290366.html)
[Linux Alpine](https://juejin.cn/post/7024096619318476814)

[ref](https://ithelp.ithome.com.tw/articles/10249640)
[ref](https://medium.com/starbugs/%E7%94%A8-harbor-%E6%9E%B6%E8%A8%AD%E7%A7%81%E6%9C%89-docker-%E5%80%89%E5%BA%AB-9e7eb2bbf769)

1.簡介
alpine沒有使用fedora的systemctl來進行服務管理，使用的是RC系列命令
OpenRC init系統
在類Unix系統上，OpenRC是一個基於依賴的init。由於0.25 OpenRC包含openrc-init，它可以替換/ sbin/init，但init程序的默認提供程序是SysVinit for OpenRC。與Linux一樣，OpenRC也可用於多個BSD系統。
OpenRC是TrueOS，Gentoo，Alpine Linux，Parabola GNU / Linux-libre，Artix Linux和其他類似unix 系統的默認初始化系統，而其他一些像Devuan則提供它作爲選項

2.rc-update
rc-update主要用於不同執行級增加或者刪除服務。
3.rc-status
rc-status 主要用於執行級的狀態管理。
4.rc-service
rc-service主用於管理服務的狀態
5.openrc
openrc主要用於管理不同的執行級。
6.我常用的RC系列命令
a.增加服務到系統啟動時執行，下例為docker
rc-update add docker boot
b.重啟網路服務
rc-service networking restart
c.列出所有服務
rc-status -a

五：關機重啟
$ reboot #重啟系統
$ poweroff #關機

```sh
3.1 openrc的安裝
apk add --no-cache openrc
3.2 rc-update - 不同運行級增加或者刪除服務
rc-update add nginx 增加一個服務
rc-update del nginx 刪除一個服務
3.3 rc-status - 運行級的狀態管理
rc-status  查看默認運行級別的狀態
rc-status -a 查看所有運行級別的狀態
3.4 rc-service - 管理服務的狀態
rc-service nginx start 啓動一個服務
rc-service nginx stop  停止一個服務
rc-service nginx restart  重啓一個服務
3.5 openrc - 管理不同的運行級
Alpine Linux可用的運行級

default
sysinit
boot
single
reboot
shutdown

3.5 關機重啓指令 - 在容器中試了好像沒反應
reboot 重啓系統，類似於shutdown -r now。
halt 關機，類似於shutdown -h now。
poweroff 關機
0x04 安裝nginx
4.1 安裝nginx軟件並更新
apk –update add –no-cache nginx
4.2 啓動nginx(二選一執行)
/etc/init.d/nginx start
rc-service nginx start
4.3 將nginx添加到啓動服務中，下次開機自動運行
rc-update add nginx

docker system info 
>>> hen check that 192.168.99.1:5000 exists in "insecure-registries" section
```


```sh
# apk add --no-cache docker openrc
# 1.安裝 docker docker-compose
apk update
apk add docker docker-compose
# 2.設定開機啟動與啟動 docker 服務
rc-service docker start
rc-update add docker
# 
service docker start
rc-service docker restart
# 设置服务开机自启动
rc-update add docker boot
reboot
```
~ 


https://linuxconfig.org/how-to-install-docker-in-rhel-8#
https://docs.docker.com/engine/install/rhel/
https://github.com/goharbor/harbor/issues/13553

redhat lab
```sh
sudo yum remove docker \
                docker-client \
                docker-client-latest \
                docker-common \
                docker-latest \
                docker-latest-logrotate \
                docker-logrotate \
                docker-engine \
                podman \
                runc
sudo yum install -y yum-utils
sudo yum-config-manager \
             --add-repo \
             https://download.docker.com/linux/rhel/docker-ce.repo       
             
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
yum list docker-ce --showduplicates | sort -r

# >>>>>>>>>>>>>>>>>>>

sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf repolist -v
dnf list docker-ce --showduplicates | sort -r
sudo dnf install docker-ce-3:20.10.21-3.el9
sudo dnf install --nobest docker-ce
sudo dnf install https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.2.6-3.3.el7.x86_64.rpm
sudo dnf install docker-ce
sudo systemctl disable firewalld
sudo systemctl enable --now docker

$ systemctl is-active docker
active
$ systemctl is-enabled docker


curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o docker-compose
sudo mv docker-compose /usr/local/bin && sudo chmod +x /usr/local/bin/docker-compose

$ sudo dnf install python3-pip
$ pip3 install docker-compose --user
```


Harbor script

```sh
$ wget https://github.com/goharbor/harbor/releases/download/v2.0.2/harbor-offline-installer-v2.0.2.tgz
$ tar -xvf harbor-offline-installer-v2.0.2.tgz
$ cd harbor
$ tree .
.
├── common.sh
├── harbor.v2.0.2.tar.gz
├── harbor.yml.tmpl
├── install.sh
├── LICENSE
└── prepare

cp harbor.yml.tmpl harbor.yml
$ sudo ./install.sh
輸入「ifconfig -a」指令來檢視所有網路介面卡資訊

# 新增以下檔案內容 /etc/docker/daemon.json


ifconfigvi
{
    "insecure-registries": ["10.5.2.73"]
}

{
    "experimental": true,
    "debug": true,
    "log-level": "info",
    "insecure-registries": ["192.168.0.7"],
    "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"],
    "tls": false,
    "tlscacert": "",
    "tlscert": "",
    "tlskey": ""
}    

重新啟動 docker & systemctl
$ sudo systemctl daemon-reload && sudo systemctl restart docker



```
* 準備一個 harbor.yml 的設定檔案
* 執行 prepare 這個腳本，此腳本會讀取 harbor.yml 的設定檔案，並根據此產生一個合適的 docker-compose 檔案
* 最後根據運行產生出來的 docker-compose 檔案即可

docker login <Your Harbor Domain> or <IP>
docker login --username admin --password 1313  https://192.168.0.7

https://github.com/gliderlabs/docker-alpine/issues/183
https://blog.51cto.com/u_15266039/4967617

```sh
~ # apk add openrc --no-cache
fetch http://dl-cdn.alpinelinux.org/alpine/v3.8/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.8/community/x86_64/APKINDEX.tar.gz
(1/2) Installing openrc (0.35.5-r4)
Executing openrc-0.35.5-r4.post-install
(2/2) Installing docker-openrc (18.06.1-r0)
Executing busybox-1.28.4-r0.trigger
OK: 187 MiB in 26 packages
~ # which service
/sbin/service
~ # service docker start
 * WARNING: docker is already starting
~ # service docker status
 * You are attempting to run an openrc service on a
 * system which openrc did not boot.
 * You may be inside a chroot or you may have used
 * another initialization system to boot this system.
 * In this situation, you will get unpredictable results!
 * If you really want to do this, issue the following command:
 * touch /run/openrc/softlevel
~ # touch /run/openrc/softlevel
touch: /run/openrc/softlevel: No such file or directory
~ # mkdir -p /run/openrc
~ # touch /run/openrc/softlevel
~ # service docker status
 * status: stopped
~ # service docker start
 * WARNING: docker is already starting
~ # service docker restart
 * WARNING: docker is already starting
~ # service docker stop
 * ERROR: docker stopped by something else
~ # service docker start
 * WARNING: docker is already starting
```


3.创建并修改完daemon.json文件后，需要让这个文件生效
a.修改完成后reload配置文件
sudo systemctl daemon-reload >>>> 怎麼處理
b.重启docker服务
sudo systemctl restartdocker.service
c.查看状态

sudo systemctl status docker -l

d.查看服务

sudo docker info
————————————————
版权声明：本文为CSDN博主「jwensh」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u013948858/article/details/79974796

