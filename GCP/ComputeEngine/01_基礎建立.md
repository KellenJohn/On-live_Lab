### GCP Compute Engine 操作說明
![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/41bc133c-6a7f-4a8b-943a-ba855b9a3dab)

 - 啟用所需的 API：在開始之前，確保你的 GCP 專案中啟用了所有需要使用的 API。根據你的需求，可能需要啟用 Compute Engine API、DNS API 等等。你可以在 Google Cloud Console 的 "API 和服務" 頁面進行啟用。
 - 虛擬機類型選擇：在建立虛擬機時，請根據你的應用需求選擇合適的虛擬機類型。不同的虛擬機類型提供不同的 CPU、RAM 和 GPU 資源，價格也會有所不同。
 - 防火牆規則設定：確保防火牆規則允許你需要的流量進入虛擬機。你可以設定防火牆規則來允許特定的 IP 地址或 IP 範圍，也可以允許特定的通訊埠（例如 HTTP 的 80 通訊埠）。
 - 網路標記與防火牆：GCP 提供網路標記功能，讓你可以將相同標記的虛擬機套用相同的防火牆規則。這樣可以方便地對多個虛擬機進行管理和設定。
 - 主機維護期間處理：為了確保高可用性，建議在主機維護期間進行虛擬機遷移。這樣可以避免主機維護期間的服務中斷。
 - 防刪除功能啟用：一般移除掉 Compute Engine 會瞬間刪除，可以防手滑，刪除時就必需要進到裡面把鉤鉤取消
 - 自動重新啟動功能：啟用自動重新啟動功能可以讓 Google 自動重新啟動虛擬機，以解決可能出現的問題。這有助於釋放記憶體和清理系統的垃圾，確保虛擬機持續運行。
 - 固定 IP 設定：如果需要固定 IP 地址，可以建立 IP 位址並將其綁定到虛擬機上。這樣即使虛擬機重啟，IP 地址也不會變更。
   - 臨時 IP，重開機會換另一個 IP，若要固定下來，請建立 IP 位址。
     - IP 綁定在運行的主機上 => 0.004 美元/小時
     - 主機關機，或 IP 放著不用 =>  0.010 美元/小時
 - 虛擬機磁碟管理：確保你對虛擬機的磁碟管理足夠。如果需要更多磁碟空間，可以掛載額外的磁碟到虛擬機上。
 - 可用性政策：了解 SPOT 實例可能會隨時被收回的特性，根據你的需求選擇適合的實例類型。

### 操作步驟
1. 建立 VM
2. 安裝 Apache
3. 寫網頁
4. 設定 DNS

 - DNS 設定：建立完虛擬機後，請設定 DNS 來將你的網站綁定到自定義的域名上，這樣用戶就能透過域名訪問你的網站。


點選 SSH 連線進入至機台
```shell
# 安裝 Apache 伺服器：根據你的需求，安裝 Apache 或其他網頁伺服器軟體，並配置伺服器以提供你的網頁內容。
sudo apt-get update
sudo apt-get install apache2 -y
```
點選外部 IP 打開查看 Apache 首頁
<img src="https://github.com/KellenJohn/On-live_Lab/assets/29540152/3952c6a9-6c1a-498c-9d38-428dbf1fc729" width="400" height="300" alt="Image">


```shell
# 撰寫你的網頁內容，確保網頁呈現正確且符合你的需求。
echo '<!doctype html><html><body>'
echo '<!DOCTYPE html>
<html>
<head>
    <title>Hello, World!</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a simple "Hello, World!" page served by Apache.</p>
</body>
</html>' | sudo tee /var/www/html/index.html
```
點選外部 IP 打開查看 Apache 首頁
![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/e46dcfdf-88e4-4751-9f9c-4194ef0cea56)
