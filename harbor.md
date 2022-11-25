[Linux Alpine](https://www.cnblogs.com/jackadam/p/9290366.html)
[Linux Alpine](https://juejin.cn/post/7024096619318476814)

[ref](https://ithelp.ithome.com.tw/articles/10249640)
[ref](https://medium.com/starbugs/%E7%94%A8-harbor-%E6%9E%B6%E8%A8%AD%E7%A7%81%E6%9C%89-docker-%E5%80%89%E5%BA%AB-9e7eb2bbf769)



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


$ sudo ./install.sh

# 新增以下檔案內容 /etc/docker/daemon.json

{
    "insecure-registries": ["<Your Harbor Domain> or <IP>"]
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
# 準備一個 harbor.yml 的設定檔案
# 執行 prepare 這個腳本，此腳本會讀取 harbor.yml 的設定檔案，並根據此產生一個合適的 docker-compose 檔案
# 最後根據運行產生出來的 docker-compose 檔案即可

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


