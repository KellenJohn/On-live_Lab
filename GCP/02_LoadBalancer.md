

1. 買個人專用網域 (Domain Name)
 - 首先，你需要選擇一個個人網域來代表你的網站，這將是你網站的網址。你可以在網路上購買網域，例如在 Godaddy 或 Google Domain 購買一個網域；當然也有免費的可以供測試使用，但是會有到期的風險。
 - Google Domain 和 GCP 是兩個不同的 Google 產品，一個用於網域註冊和管理，另一個用於雲計算和應用程序運行。它們之間的關聯在於可以通過 Google Domain 將網域指向 GCP 上的應用程序。  

2. 在 Google Cloud Platform (GCP) 建立 Compute Engine 並選擇固定 IP
 - 在 GCP 上建立一個 Compute Engine 虛擬機器(VM) 來運行你的網站，我們會將此 VM 作為負載平衡的後端伺服器。
 - 請確保在建立 VM 時選擇「固定外部 IP 地址」，這將確保你的 VM 擁有一個固定的 Public IP 地址。

3. 建立執行個體群組
 - Load Balancer 通常會與 Instance Group 一起使用，Load Balancer 需要知道要將請求轉發到哪些虛擬機器實例，這些虛擬機實例通常會被組織成 Instance Group。
 - 這樣的架構可以有以下幾個好處：
   - 可擴展性：可以在 Instance Group 中添加或移除虛擬機器實例，Load Balancer 會自動調整並將流量平均分配給這些實例。
   - 高可用性：如果某個虛擬機器實例出現故障或不可用，Load Balancer會自動將流量重新導向到其他可用的虛擬機器實例。
   - 簡化管理：通過 Instance Group，集中管理一組虛擬機器實例，方便擴展和維護。
 - 選擇 New unmanaged instance group

4. 到 Cloud DNS 或域名商後台設定 A record 或 CNAME：
 - 選擇「網路」→ 「Cloud DNS」→ 建立「可用區」：將你在域名商處得到的DNS名稱 (例如：example.com) 貼到 DNS 名稱欄位中
 - 完成後，你的 Cloud DNS 設定應該會顯示 NS (Name Server) 和SOA (Start of Authority) 類型的記錄；接著在設定 A record 及 CName(選項)
 - A 記錄：如果你想直接將你的個人網域指向 VM 的固定IP，新增一個 A 記錄，將網域名稱 (例如：example.com) 指向VM的固定IP地址 (例如：123.45.67.89)。
 - CNAME 記錄(Canonical Name)：將一個域名（或子域名）映射到另一個域名，如果你想將你的網域指向另一個名稱而不是直接指向 IP，新增一個 CNAME 記錄，將網域名稱 (例如：apache.example.com) 指向另一個目標網域名稱 (例如：apache.foobar.com)。這樣當有人輸入 apache.example.com 時，DNS 解析會自動將它轉發到 apache.foobar.com。

5. 在Google Cloud Platform (GCP) 建立 Load Balancer
 - 預計是 User --> Load Balancer 前端對外 443 port --> Load Balancer 後端導向主機的 80 port
 - 前端設定：：在 Load Balancer 中，建立前端配置來定義 Load Balancer 入口，可以選擇 HTTP 或 HTTPS 前端，並指定要監聽的端口
   - 這邊我們選 HTTPS 順便試一下憑證，然後也驗證一下後端是 HTTP 80 端口！建立憑證 > 網域 > 這邊我們選擇在 Cloud DNS 上建立好的 apache.example.com，稍後回去我們在拿到底下的 Stati IP 替換成在 Cloud DNS A recored 的 apache.example.com 的 IP 位置，注意 Cloud DNS 一定要解析到 Load Balancer 的 IP，憑證才會生效
   - IP Address：我們選擇建立靜態 IP(Static IP)來取代掉臨時 IP(Empheral IP)。題外話，靜態 IP 翻的不是很懂，比較偏像是保留性質的 IP，在GCP上使用 "Static IP" 時，它並不是真正的固定不變的 IP 地址，仍然可以將這個IP地址釋放或重新分配給其他虛擬機器。
 - 後端設定：在 Load Balancer 中，建立後端服務，將虛擬機器實例加入該後端服務。這些 VM 實例將會接收來自 Load Balancer 的請求。
   - 健康檢查(Health Check)：建立健康檢查，通訊協定 TCP + 通訊埠 80

   主機與路徑規則




