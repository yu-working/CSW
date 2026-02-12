# ================================
# 設定參數（請修改）
# ================================
$repoOwner = "yu-working"
$repoName  = "CSW"
$branch    = "master"     # 若為 master 請改 master
$projectDir = "customer_service_wingman"  # 專案資料夾名稱

# ================================
# 1️⃣ 建立專案資料夾
# ================================
Write-Host "Creating project directory..."
New-Item -ItemType Directory -Force -Path $projectDir | Out-Null
Set-Location $projectDir

# ================================
# 2️⃣ 下載 GitHub Repo（ZIP）
# ================================
Write-Host "Downloading repository..."
$zipUrl = "https://github.com/$repoOwner/$repoName/archive/refs/heads/$branch.zip"
$zipFile = "repo.zip"

Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile

# ================================
# 3️⃣ 解壓縮
# ================================
Write-Host "Extracting repository..."
Expand-Archive $zipFile -DestinationPath . -Force

# 進入解壓後資料夾
$extractedFolder = "$repoName-$branch"
Set-Location $extractedFolder

# ================================
# 4️⃣ 安裝 uv
# ================================
Write-Host "Installing uv..."
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 重新載入環境變數
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")

uv --version

# ================================
# 5️⃣ 建立 Python 3.10 虛擬環境
# ================================
Write-Host "Creating Python 3.10 virtual environment..."
uv venv --python 3.10

# 啟用虛擬環境
Write-Host "Activating virtual environment..."
.venv\Scripts\Activate.ps1

# ================================
# 6️⃣ 安裝 requirements.txt
# ================================
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies..."
    uv pip install -r requirements.txt
} else {
    Write-Host "No requirements.txt found."
}

Write-Host "Setup complete."
