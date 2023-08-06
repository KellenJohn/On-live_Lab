### 透過 Load Balancer 導流至 Instance Group(管理 App Server) 並搭配 Cloud DNS 來對外提供服務

在 Google Cloud Platform（GCP）上建立個人網站，您需要先建立一個虛擬機器（Compute Engine VM）來運行您的網站應用程式。在建立 VM 時，請務必選擇 "固定外部IP地址"，這將確保您的VM擁有一個穩定的公有 IP 地址，方便用戶訪問您的網站。接著，建立一個 Instance Group 來管理一組虛擬機器實例。Instance Group 可用於實現負載均衡和自動擴展，這在面對高流量時非常有用。如果您只打算使用單一虛擬機器，也可以直接將該虛擬機器連接到 Load Balancer。接下來，可以在 GCP 上建立 Load Balancer，它將負責將流量平均分發到 Instance Group 中的虛擬機器實例，從而實現載荷均衡和高可用性。您可以選擇 HTTPS 前端，並在 Google Domain 上建立憑證，確保網站的安全性。

最後，您需要建立後端服務，將虛擬機器實例加入該後端服務，以接收來自 Load Balancer 的請求。您還可以建立健康檢查來監測虛擬機器實例的狀態，並確保只有健康的實例會接收流量。

為了讓您的網域名稱指向您的網站，您需要進行 DNS 設定。在 Google Cloud Platform 的 Cloud DNS 中，您可以將您在域名供應商處得到的 DNS 名稱（例如：example.com）與您的 VM 的固定 IP 地址進行關聯，這樣當有人輸入您的網域名稱時，DNS解析會將其轉發到您的 VM，用戶就能訪問您的網站。

![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/b85d4ac0-19b5-4524-97da-b352dffa6829)


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
 - A 記錄：它用於將域名（例如example.com）映射到對應的IPv4（Internet Protocol version 4）地址，如果你想直接將你的個人網域指向 VM 的固定IP，新增一個 A 記錄，並將網域名稱 (例如：example.com) 指向 VM 的固定 IP 地址 (例如：123.45.67.89)。這就像告訴 GPS 導航系統要去台北車站，實際上就會帶你到台北車站的具體的位置(地址)
 - CNAME 記錄(Canonical Name)：將一個域名（或子域名）映射到另一個域名，如果你想將你的網域指向另一個名稱而不是直接指向 IP，新增一個 CNAME 記錄，將網域名稱 (例如：apache.example.com) 指向另一個目標網域名稱 (例如：apache.fubar.com)。這樣當有人輸入 apache.example.com 時，DNS 解析會自動將它轉發到 apache.fubar.com。

5. 在Google Cloud Platform (GCP) 建立 Load Balancer
 - 預計是 User --> Load Balancer 前端對外 443 port --> Load Balancer 後端導向主機的 80 port
 - 前端設定：：在 Load Balancer 中，建立前端配置來定義 Load Balancer 入口，可以選擇 HTTP 或 HTTPS 前端，並指定要監聽的端口
   - 這邊我們選 HTTPS 順便試一下憑證，然後也驗證一下後端是 HTTP 80 端口！建立憑證 > 網域 > 這邊我們選擇在 Cloud DNS 上建立好的 apache.example.com，稍後回去我們在拿到底下的 Stati IP 替換成在 Cloud DNS A recored 的 apache.example.com 的 IP 位置，注意 Cloud DNS 一定要解析到 Load Balancer 的 IP，憑證才會生效
   - IP Address：我們選擇建立靜態 IP(Static IP)來取代掉臨時 IP(Empheral IP)。題外話，靜態 IP 翻的不是很懂，比較偏像是保留性質的 IP，在GCP上使用 "Static IP" 時，它並不是真正的固定不變的 IP 地址，仍然可以將這個IP地址釋放或重新分配給其他虛擬機器。
 - 後端設定：在 Load Balancer 中，建立後端服務，將虛擬機器實例加入該後端服務。這些 VM 實例將會接收來自 Load Balancer 的請求。
   - 健康檢查(Health Check)：建立健康檢查，通訊協定 TCP + 通訊埠 80

   主機與路徑規則


---

### 補充：
#### DNS 如何將流量路由到 Web 應用程式？

![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/2c8329b2-e267-4edc-9401-0157fee1b867)

寫 Domain 供應商大家比較了解，但實際上還要了解 Root Server / TLD Server / Authoritative Server 運作的關係，科普可以參考 [AWS DNS](https://aws.amazon.com/tw/route53/what-is-dns/#DNS_%E5%A6%82%E4%BD%95%E5%B0%87%E6%B5%81%E9%87%8F%E8%B7%AF%E7%94%B1%E5%88%B0_Web_%E6%87%89%E7%94%A8%E7%A8%8B%E5%BC%8F%EF%BC%9F)，算是有圖有文件及流的概念說明！

1. 使用者開啟 Web 瀏覽器，在網址列輸入 www.example.com，然後按 Enter。
2. www.example.com 的請求路由到 DNS 解析程式，這通常由使用者的網際網路服務供應商 (ISP) 管理，例如有線電視網際網路供應商、DSL 寬頻供應商或公司網路。
3. ISP 的 DNS 解析程式將 www.example.com 的請求轉送到 DNS 根名稱伺服器。
4. ISP 的 DNS 解析程式再次轉送 www.example.com 的請求，這次轉送到 .com 網域的其中一個 TLD 名稱伺服器。.com 網域的名稱伺服器會以與 example.com 網域關聯的四部 Amazon Route 53 名稱伺服器名稱回應請求。
5. ISP 的 DNS 解析程式選擇一部 Amazon Route 53 名稱伺服器，並將 www.example.com 的請求轉送到該名稱伺服器。
6. Amazon Route 53 名稱伺服器會在 example.com 託管區域中尋找 www.example.com 記錄，取得關聯的值，例如 Web 伺服器的 IP 地址 192.0.2.44，然後將 IP 地址傳回 DNS 解析程式。
7. ISP 的 DNS 解析程式最終取得使用者需要的 IP 地址。解析程式將該值傳回 Web 瀏覽器。DNS 解析程式也會將 example.com 的 IP 地址快取 (存放) 您所指定的一段時間，下次有人瀏覽到 example.com 時即可更快速的做出回應。如需詳細資訊，請參閱存留時間 (TTL)。
8. Web 瀏覽器將 www.example.com 的請求傳送到從 DNS 解析程式取得的 IP 地址。這就是您的內容所在之處，例如，在 Amazon EC2 執行個體上執行的 Web 伺服器或是設定為網站端點的 Amazon S3 儲存貯體。
9. 位於 192.0.2.44 的 Web 伺服器或其他資源將 www.example.com 的網頁傳回 Web 瀏覽器，然後 Web 瀏覽器就會顯示該頁面
![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/2067565a-09cf-4cfa-be96-a679e212633d)


#### Root Server、TLD Server 和 Authoritative Server

> 是 Domain Name System（DNS）中不同層次的伺服器，它們在解析網域名稱時扮演不同的角色。

以下是它們的差異和舉例：
1. Root Server（根域名伺服器）：
 - Root Server 是 DNS 層次結構的最上層，它們是整個DNS系統的起始點。
 - Root Server 主要負責回答根域名（例如.com、.org、.net等）的查詢，並指向下一級的 TLD Server。
 - 全球共有13組Root Server，位於不同地理位置，每組Root Server都由不同的組織管理。
   - 舉例：當用戶輸入 "www.example.com"，瀏覽器會向 Root Server 查詢 .com 域名的 IP 地址。

2. TLD Server（頂級域名伺服器）：
 - TLD Server 是 DNS 的下一級，處於根域名伺服器之後。
 - TLD Server 負責回答頂級域名（例如.com、.org、.net等）的查詢，並指向該頂級域名下一級的Authoritative Server。
 - 每個頂級域名（例如.com）都有自己的TLD Server。
   - 舉例：當用戶輸入 "www.example.com"，瀏覽器會向 .com 域名的 TLD Server 查詢 example.com 的 IP 地址。

3. Authoritative Server（授權伺服器）：
  - Authoritative Server 是 DNS 層次結構中的最低級，它處於TLD Server之後。
  - Authoritative Server 是管理特定網域名稱解析的伺服器，負責回答特定網域名稱的查詢；就像是 Cloud DNS（GCP）和 Route 53（AWS）這樣的產品，它們都是提供域名解析服務的授權伺服器
  - 當用戶在瀏覽器中輸入網站的域名(網站)時，最終的解析工作由 Authoritative Server 完成，它會提供該網站的IP地址或其他相關記錄，例如該網站的 IP 地址或其他 DNS 記錄，這樣瀏覽器就能根據得到的 IP 地址連接到相應的網站伺服器，從而顯示網站內容。
    - 舉例：假設"www.example.com"的Authoritative Server是由example.com網站擁有者所管理的伺服器，當用戶輸入該網址時，瀏覽器會向該Authoritative Server查詢相關的IP地址或其他資訊。
 
> 總結來說，Root Server 是 DNS 的最高層，負責回答根域名的查詢；TLD Server 處於 Root Server 之後，負責回答頂級域名的查詢；Authoritative Server 處於 TLD Server 之後，是最低層的伺服器，負責回答特定網域名稱的查詢。這些伺服器協同工作，使得用戶能夠通過網域名稱訪問互聯網上的網站和服務。

### Reference
* [TECH IN THE CLOUD](https://robertleggett.blog/2019/11/25/deep-dive-dns/)
* [Cloud DNS Best Practice](https://cloud.google.com/dns/docs/best-practices?hl=zh-cn#reference_architectures_for_hybrid_dns)
