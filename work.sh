# Contain lab os: Linux-Alpine
# basic apk update
apk update
apk add curl
apk add lynx
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
 

 
# k3s / 最不吃資源
# Curl 下載方式一
curl -s https://raw.githubusercontent.com/rancher/k3d/master/install.sh | bash
# Wget 下載方式二
wget -q -O - https://raw.githubusercontent.com/rancher/k3d/master/install.sh | bash
k3d cluster create demo --servers 1 --agents 3
curl -sfL http://rancher-mirror.cnrancher.com/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -
 
# kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.9.0/kind-linux-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/kind
kind create cluster --name demo

# minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube version
minikube start --force --driver=docker
