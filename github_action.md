##### Github Actions 的基本元素
要了解 Github Actions 的基本概念，有幾個元素（或是術語）是必須要知道的，範圍由大至小分別為： `Workflow -> Job -> Step -> Action`

* Workflow : CI/CD 一次要運行的整個過程，就稱作 Workflow，一個 Workflow 裡會涵蓋多個 Job、Step、 Action。
* Job : 意義跟翻成中文差不多，代表「任務」。一個 Workflow 由多個 Job 組成，這也意謂著一個 Workflow 可以完成多個任務。
* Step : 代表一個個「步驟」，一個 Job 由多個 Step 組成，意謂著一個 Job 是一個步驟一個步驟來完成的。
* Action : 「命令」或「動作」，每個 Step 可以依序執行多個命令（動作）。

##### Github Actions Workflow Config
要啟用 Github Actions，不需要什麼複雜的設定，只需要在專案的根目錄新增 .github/workflow 的路徑，
將專案推到 Github 上後 Github 就會自動執行放在該路徑裡的 .yml config 檔 (Workflow document 採用 YAML 格式)。
.yml 檔的檔名可以隨意取，也可以創建多個 .yml 檔，Github 會執行 .github/workflow 路徑下的所有 YAML 文件。

這邊直接以 medium-stat-box 這個專案的 config 檔來當作例子：

範本
```yaml
# workflow 名稱
name: CI

# 什麼情況下觸發 workflow
on:
  # 對於 main branch 建立 Branch 與 Pull Request 時觸發 workflow 
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

  # 允許你從 Action 頁簽上手動執行 workflow
  workflow_dispatch:

# Job 可以循序或平行執行
jobs:
  # 這個 workflow 只有一個 job，名稱為 "build"
  build:
    # 這個 job 會執行在作業系統為 ubuntu 的 runner
    runs-on: ubuntu-latest

    # 作為 Job 的一部分，Steps 會循序執行一連串的動作
    steps:
      # 在 $GITHUB_WORKSPACE 下簽出您的存儲庫，以便您的工作可以訪問它
      - uses: actions/checkout@v2

      # 在 Runner 上使用 shell 顯示出 Hello world
      - name: Run a one-line script
        run: echo Hello, world!

      # 執行一組的指令
      - name: Run a multi-line script
        run: |
          echo Add other actions to build,
          echo test, and deploy your project.
```


範本
```yaml
# .github/workflows/continuous-integration-workflow.yml
# workflow 名稱
name: Greet Everyone
# This workflow is triggered on pushes to the repository.
on: [push]

jobs:
  build:
    # Job name is Greeting
    name: Greeting
    # This job runs on Linux
    runs-on: ubuntu-latest
    steps:
      # This step uses GitHub's hello-world-javascript-action: https://github.com/actions/hello-world-javascript-action
      - name: Hello world
        uses: actions/hello-world-javascript-action@v1
        with:
          who-to-greet: 'Mona the Octocat'
        id: hello
      # This step prints an output (time) from the previous step's action.
      - name: Echo the greeting's time
        run: echo 'The time was ${{ steps.hello.outputs.time }}.'
```

Trivy 範本
```yaml
  push:
    branches:
      - master
  pull_request:
jobs:
  build:
    name: Build
    runs-on: ubuntu-20.04
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Build an image from Dockerfile
        run: |
          docker build -t docker.io/my-organization/my-app:${{ github.sha }} .
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'docker.io/my-organization/my-app:${{ github.sha }}'
          format: 'table'
          exit-code: '1'
          ignore-unfixed: true
          vuln-type: 'os,library'
          severity: 'CRITICAL,HIGH'

```
Docker
```yaml
name: ci

on:
  push:
    branches:
      - 'main'

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      -
        name: Set up QEMU
        uses: docker/setup-qemu-action@v2
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      -
        name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      -
        name: Build and push
        uses: docker/build-push-action@v3
        with:
          push: true
          tags: user/app:latest
```
### Referenece
* [實作開源小工具](https://medium.com/starbugs/%E5%AF%A6%E4%BD%9C%E9%96%8B%E6%BA%90%E5%B0%8F%E5%B7%A5%E5%85%B7-%E8%88%87-github-actions-%E7%9A%84%E7%AC%AC%E4%B8%80%E6%AC%A1%E7%9B%B8%E9%81%87-3dd2d70eeb)
* [ITHelp](https://ithelp.ithome.com.tw/articles/10262377)
* [Nice](https://ithelp.ithome.com.tw/users/20091494/ironman/4464?page=2)
★ https://blog.isayme.org/posts/issues-55/
★ https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html
https://docs.github.com/cn/actions/creating-actions/creating-a-docker-container-action
https://anzhiy.cn/posts/asdx.html

作業/11
https://docs.github.com/cn/actions/creating-actions/creating-a-docker-container-action
https://docs.github.com/cn/actions/publishing-packages/publishing-docker-images
https://github.com/docker/build-push-action/issues/603
[★](https://github.com/docker/build-push-action/issues/223)
