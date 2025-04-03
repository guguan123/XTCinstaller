# ------------------------------------------------------------------------------
# Script Name: XTCinstaller.ps1
# Author: GuGuan123
# Version: 1.0
# Created: 2025-04-03
# Description: 通过 ADB 安装 APK 到小天才电话手表
# ------------------------------------------------------------------------------


# 假设 adb.exe 已添加到系统 PATH 中，或者需要指定完整路径
$adbPath = "adb"  # 如果 adb 不在 PATH 中，可以改为 "C:\path\to\adb.exe"

# 函数：生成安装命令并写入临时文件
function Add-InstallCommand {
	param (
		[string]$cmdPart1,
		[string]$cmdPart2
	)
	return "echo -n `"${cmdPart1} instal`">>/sdcard/apk.txt; echo `"l$cmdPart2`">>/sdcard/apk.txt;"
}

# 检查设备连接
Write-Host "正在连接手表..."
$deviceList = & $adbPath devices
if (-not ($deviceList -match "device")) {
	throw "未检测到设备连接"
}
Write-Host "连接成功."

# 获取用户输入的软件位置
Write-Host "软件位置可输入 APK 下载链接或是本地文件路径."
Write-Host "若用本地路径安装，需要解锁 adb push."
Write-Host "若用下载链接安装，则不需要."
$inputMsg = Read-Host "请输入软件位置"

# 清理旧文件
& $adbPath shell "if test -e /sdcard/apk.txt; then rm /sdcard/apk.txt; fi"
& $adbPath shell "if test -e /sdcard/apk.apk; then rm /sdcard/apk.apk; fi"

# 根据输入处理 APK 文件
if ($inputMsg.Trim() -eq "") {
	throw "您没有输入 APK 链接或路径"
} elseif ($inputMsg -match "^(http://|https://|ftp://)") {
	Write-Host "正在下载软件..."
	# 使用 curl 下载文件到设备
	& $adbPath shell "curl --output /sdcard/apk.apk ${inputMsg}"
} else {
	# 检查本地文件是否存在
	if (-not (Test-Path $inputMsg)) {
		throw "文件不存在: ${inputMsg}"
	}
	# 推送本地文件到设备
	& $adbPath push $inputMsg "/sdcard/apk.apk"
}

Write-Host "正在创建安装会话..."
# 创建安装会话
$createCmd = Add-InstallCommand -cmdPart1 "pm" -cmdPart2 "-create"
$response = & $adbPath shell "${createCmd} sh /sdcard/apk.txt"
if (-not ($response -match "Success")) {
	throw "创建安装会话失败: ${response}"
}
$sessionID = [int]($response -split '\[')[1].Split(']')[0]
Write-Host "session ID: ${sessionID}"

Write-Host "正在安装软件，可能需要一些时间..."
# 写入和提交安装会话
& $adbPath shell "rm /sdcard/apk.txt"
$writeCmd = Add-InstallCommand -cmdPart1 "pm" -cmdPart2 "-write ${sessionID} force /sdcard/apk.apk"
$commitCmd = Add-InstallCommand -cmdPart1 "pm" -cmdPart2 "-commit ${sessionID}"
& $adbPath shell "${writeCmd} ${commitCmd} sh /sdcard/apk.txt"

# 清理临时文件
& $adbPath shell "rm /sdcard/apk.txt"
& $adbPath shell "rm /sdcard/apk.apk"
Write-Host "安装进程结束."

# 确保连接关闭（PowerShell 中直接调用 adb kill-server 可选）
# & $adbPath kill-server
