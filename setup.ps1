# ================================
# 設定參數（請修改）
# ================================
$repoOwner = "yu-working"
$repoName  = "CSW"
$branch    = "master"     # 若為 master 請改 master
$projectDir = "customer_service_wingman"  # 專案資料夾名稱

# ================================
# 1️⃣ 使用當前目錄（不建立新資料夾）
# ================================
Write-Host "Using current directory..."

# ================================
# 2️⃣ 下載 GitHub Repo（ZIP）
# ================================
Write-Host "Downloading repository..."
$zipUrl = "https://github.com/$repoOwner/$repoName/archive/refs/heads/$branch.zip"
$zipFile = "repo.zip"

Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile

# ================================
# 3️⃣ 解壓縮並清理 ZIP
# ================================
Write-Host "Extracting repository..."
Expand-Archive $zipFile -DestinationPath . -Force

# 解壓縮完畢後把 repo.zip 移除
Write-Host "Cleaning up zip..."
Remove-Item $zipFile -Force

# 取得解壓後資料夾名稱並改名為 customer_service_wingman，然後進入該資料夾
$extractedFolder = "$repoName-$branch"
Write-Host "Renaming extracted folder to $projectDir..."
if (Test-Path $projectDir) {
    Write-Host "Target folder '$projectDir' already exists. Skipping rename."
} else {
    Rename-Item -Path $extractedFolder -NewName $projectDir -Force
}
Set-Location $projectDir

# ================================
# 4️⃣ 安裝 uv
# ================================
Write-Host "Installing uv..."
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 重新載入 PATH（合併 User 與 Machine，避免抓不到指令）
$machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
$userPath    = [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path    = "$userPath;$machinePath"

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
