


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



我們先準備好一組自動擴展的機器，也就是執行個體群組 (Instance Group)，當使用者流量從最前端的負載平衡進來，接著把前端流量導到不同的機器，如果流量突然變大，後端機器無法負荷的時候，Instance Group 就會自動加開機器，由負載平衡自動把流量導流到新機器上，這樣原有的機器就不會因為負載過重而崩潰。
### Load Balancer 和 Instance Group：
當在 Google Cloud Platform（GCP）上建立執行個體群組（Instance Group）時，您可以根據需要使用不同的方法來創建虛擬機器實例。這些方法包括從腳本範本（Script Template）和映像（Image）建立。接下來，我們將解釋這兩種方法的相關流程。

#### 從腳本範本（Script Template）建立虛擬機器實例：
1. 腳本範本是一個包含設定和指令的檔案，可用於自動化虛擬機器的配置和部署。您可以在 GCP 上建立腳本範本，其中包含有關虛擬機器設定的信息，例如操作系統、軟體、環境變數等。
當有新的虛擬機器需要添加到群組時，執行個體群組會自動運行腳本範本以創建新的虛擬機器。
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
2. 從虛擬機器實例建立映像（Image）
 - 映像是一個包含完整操作系統和應用程式的檔案，可以用來部署虛擬機器。您可以在 GCP 上創建映像，並在其中安裝和設定所需的軟體。與 Dockerfile 不同的是，這邊可以先行準備好一個實際的 VM 後，在進去設定完成後，關閉此台 VM 後，即可建立映像（Image） 
 - 在建立執行個體群組時，您可以指定使用特定的映像來創建虛擬機器實例。執行個體群組將基於這個映像複製多個實例。
 - 當有新的虛擬機器需要添加到群組時，執行個體群組會從映像複製一個新的虛擬機器。

3.其他設定要留意
 - 等待期：主機建立好 scripts 中所需要的 Apache, software, web page 等，需要等待這些都執行完才能對外服務。
 - 自動修復：當群組判斷某台主機「不健康」，群組會直接「刪除」它，然後重新建立機器，並沒有真的修復！
 - Instance Group 建立好後，群組主機名稱會以群組名稱為前綴 + 4 碼隨機字母數字，e.g., lab-e87q，大概會是這樣的概念，Instance Group Template -> Instance Group -> VM(名稱為 Instance Group + "4-digit alphanumeric code")


### 設定 Load Balancer（負載平衡器）：
1. 在建立執行個體群組後，如果您希望實現負載平衡，則可以在 GCP 上設定負載平衡器。負載平衡器可以將流量均勻地分配給執行個體群組中的虛擬機器，從而實現流量的負載均衡和高可用性。
2. 設定負載平衡器涉及到指定前端 IP 和後端服務。前端 IP 是外部用戶訪問負載平衡器的入口，而後端服務則是將流量轉發到執行個體群組中的虛擬機器。
3. 一旦設定完成，負載平衡器將根據流量量和虛擬機器的運行狀態，自動將請求分配給執行個體群組中的可用虛擬機器，從而實現資源的均勻分配和高效的流量處理。

> 總結來說，在 GCP 上建立執行個體群組涉及使用腳本範本或映像來創建虛擬機器實例，並在需要時進行自動擴展。然後，您可以設定負載平衡器，以實現流量的均勻分配和高可用性，並確保執行個體群組中的虛擬機器能夠有效處理大量的網絡請求。這樣可以確保您的應用程式在高流量時保持高效運行，同時提高整個系統的穩定性和可用性。


### 壓測與監控
```sh
sudo apt-get install siege
siege -c 250 http://34.117.52.25
```

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






