# ------------------------------------------------------------------------------
# Script Name: XTCinstaller.ps1
# Author: GuGuan123
# Version: 1.1
# Created: 2025-04-03
# Updated: 2025-04-04
# Description: Install APK to XTC smartwatch via ADB
# ------------------------------------------------------------------------------

param (
	[string]$apkAddress = ""  # External parameter for APK address (link or local path)
)

# Assuming adb.exe is added to the system PATH or a full path is provided
$adbPath = "adb"  # If adb is not in PATH, change to "C:\path\to\adb.exe"

# Generate install command and write to a temporary file
function Add-InstallCommand {
	param (
		[string]$cmdPart1,
		[string]$cmdPart2
	)
	return "echo -n `"${cmdPart1} instal`">>/sdcard/apk.txt; echo `"l$cmdPart2`">>/sdcard/apk.txt;"
}

try {
# Check if ADB is installed
if (Get-Command $adbPath -ErrorAction SilentlyContinue) {	# Check if adb is in PATH
	& $adbPath version
} else {
	throw "ADB not found, please ensure ADB is installed and in the PATH"
}

# Check device connection
Write-Host "Connecting to the smartwatch..."
$deviceList = & $adbPath devices | Select-String -Pattern "device$"
if ($deviceList.Count -eq 0) {
	throw "No device detected"
}
Write-Host "Connection successful."

# Determine APK address: use external parameter if provided, otherwise prompt user
if ([string]::IsNullOrWhiteSpace($apkAddress)) {
	Write-Host "The software location can be either an APK download link or a local file path."
	Write-Host "If using a local path, ADB push needs to be unlocked."
	Write-Host "If using a download link, no additional steps are needed."
	$inputMsg = Read-Host "Please enter the software location"
} else {
	$inputMsg = $apkAddress
}

# Clean up user input
$inputMsg = $inputMsg.Trim()
if ($inputMsg.StartsWith('&')) {
	$inputMsg = $inputMsg.Substring(1).Trim()
}
$inputMsg = $inputMsg.Trim('"', "'")

# Clean up old files
& $adbPath shell "if test -e /sdcard/apk.txt; then rm /sdcard/apk.txt; fi"
& $adbPath shell "if test -e /sdcard/apk.apk; then rm /sdcard/apk.apk; fi"

# Handle APK file based on input
if ($inputMsg.Trim() -eq "") {
	throw "You did not enter an APK link or path"
} elseif ($inputMsg -match "^(http://|https://|ftp://)") {
	Write-Host "Downloading the APK..."
	# Use curl to download the file to the device
	& $adbPath shell "curl --output /sdcard/apk.apk ${inputMsg}"
} else {
	# Check if local file exists
	if (-not (Test-Path $inputMsg)) {
		throw "File not found: ${inputMsg}"
	}
	# Push local file to the device
	& $adbPath push $inputMsg "/sdcard/apk.apk"
}

Write-Host "Creating installation session..."
# Create installation session
$createCmd = Add-InstallCommand -cmdPart1 "pm" -cmdPart2 "-create"
$response = & $adbPath shell "${createCmd} sh /sdcard/apk.txt"
if (-not ($response -match "Success")) {
	throw "Failed to create installation session: ${response}"
}
$sessionID = [int]($response -split '\[')[1].Split(']')[0]
Write-Host "Session ID: ${sessionID}"

Write-Host "Installing the software, this may take some time..."
# Write and commit installation session
& $adbPath shell "rm /sdcard/apk.txt"
$writeCmd = Add-InstallCommand -cmdPart1 "pm" -cmdPart2 "-write ${sessionID} force /sdcard/apk.apk"
$commitCmd = Add-InstallCommand -cmdPart1 "pm" -cmdPart2 "-commit ${sessionID}"
& $adbPath shell "${writeCmd} ${commitCmd} sh /sdcard/apk.txt"

# Clean up temporary files
& $adbPath shell "rm /sdcard/apk.txt"
& $adbPath shell "rm /sdcard/apk.apk"

# & $adbPath kill-server
} catch {
	$exceptionName = $_.Exception.GetType().Name
	$exceptionInfo = $_.Exception.Message
	Write-Host "[Error] ${exceptionName}: ${exceptionInfo}"
	Exit 1
} finally {
	if ($Host.UI.RawUI) {
		Write-Host "Press Enter to exit."
		$null = Read-Host
	}
}
