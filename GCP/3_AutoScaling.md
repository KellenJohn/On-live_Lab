```sh
#! /bin/bash
apt-get update
apt-get install -y apache2
cat <<EOF > /var/www/html/index.html
<html><body><h1>Hello World(From Image)</h1>
<p>This page was created from a simple startup script!</p>
</body></html>
EOF
```
sudo apt-get install siege
siege -c 250 http://34.117.52.25

自動擴充概念說明
使用 Startup-Script 建立群組說明


使用 Image 建立群組說明
示範 使用 Startup-Script 建立群組
確認範本能正常建立機器


使用範本建立群組
調度模式說明
自動擴充指標說明
健康狀態檢查說明
建立健康狀態檢查
將健康狀態檢查設定到群組


等待期：主機建立好 scripts 中所需要的 Apache, software, web page 等，需要等待這些都執行完才能對外服務。
自動修復：當群組判斷某台主機「不健康」，群組會直接「刪除」它，然後重新建立機器，並沒有真的修復！
主機名稱會以群組名稱為前綴 + 4 碼隨機字母數字，e.g., lab-e87q
Load Balancer 的健康狀態檢查：
機器健康，LB 才會送流量給機器，不健康，LB 不送流量給機器，與前面的執行個體健康狀態檢查不一樣(會去修復)，兩個目的不一樣！
Monitaring
建立儀錶板 Dashboard，Save Chart > 命名 Chart Name > 指定 Dashbaord 名稱或新增 New Dashboard
建立網路流量指標 Metrics Explorer 
選取指標
VM instance > Instance > Received bytes
VM instance > 熱門指標 > CPU Utilization
Label = instance_group
Comparison = equal
value = [群組名稱]






