import os
from adb_shell.adb_device import AdbDeviceUsb
from adb_shell.exceptions import *
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

pubkey = 'QAAAAM9PsXbRqMIeGMid/sA/lmTebZZOgsjgytuOJyRdi2PsK9TqlubepeTKoehzhwQto4n9imOxbeULk/RXTNP6Dr0JY699RY9186HyBpvp8IjyINQy2nljSUxrpY1/YcgZLnbNu1zUlzwnocmQlCRKELZCQyDQ+zDKobJF+ocMyKt/zFl8a1E7VDz3I1U6hSAiGT9a3vYYUcbxD5hDc+DDNvpOfnbelxETAuu0K57Mi4m/iPNBcCmGlftXT5F0q15eaLCJGFqX7nWFeOaQfXhuRt1iXxCp1GRcuS3YvYQTtdRrf4amcSNOVUUsufHkNSWmZinZ0Iai9+5BzIHN42uisXHFSGPbvSgPoqwo5l6GXuMr+nGy1OxpkDzneGUS0JbjG2xeIcmQvRZWQrxpYzIPmV86Vlj8OQ+OPz8l1jsAyVLY4pVVoeGlAoIDbgSORYd2Hw45bg6OQtIZNPcjccRYTPUlrJ/zlaQXBDxS8/EKC0sF3+S6Q7J+LhJbN8tUce52xl1WvvXhr2uiTQMTzrIUFRA6f2f+mEqbJk9rfBirmM51EznKaEwewxT/G4a5LfVWAzqPrv+FS6Tuu2Hxf8mWtiZkcFpaLx8u6uNmFkUmMADHg3Vt8Mt9CktohSH5Y4WmdiJyu+B8sQ4L7x0G/92xnBd7/+0d9BvbZGUoLvUEKAQc0U+ytgEAAQA= wangzm5773@WANGZM'
privkey = '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDbY0jFcbGia+PN\ngcxB7veihtDZKWamJTXk8bksRVVOI3Gmhn9r1LUThL3YLblcZNSpEF9i3UZueH2Q\n5niFde6XWhiJsGheXqt0kU9X+5WGKXBB84i/iYvMniu06wITEZfedn5O+jbD4HND\nmA/xxlEY9t5aPxkiIIU6VSP3PFQ7UWt8Wcx/q8gMh/pFsqHKMPvQIENCthBKJJSQ\nyaEnPJfUXLvNdi4ZyGF/jaVrTEljedoy1CDyiPDpmwbyofN1j0V9r2MJvQ7600xX\n9JML5W2xY4r9iaMtBIdz6KHK5KXe5pbq1CvsY4tdJCeO28rgyIJOlm3eZJY/wP6d\nyBgewqjRAgMBAAECggEABa1HhEhsCB+86M6bhPc/NCxDOjipMye9AcbEJmJIPKSL\n0SXOJUb/RS6G+mbl0tS5xgLU8l93GO5dksLL9T7MejZ2x7/8q2MivPpHmydjl/Gk\nOdNTQ2A2nF2uvtiNQ1tjWnp8IToLRxKcmPAAivPj7v6bBAB5pi7rk6CsChPnEBPV\nLUnMXTlzPilHBpZOzN/4oCixnkNqa+r2fl88jcC8Z6EQJzo4mMrR52vIiqbguJ1T\nhO0Q01rrh5t+38C7tYxyxZ58JUdTyN7eBQw4PMYLVifvlQCXYZe5xwFIOGXEvOkH\nXPvg7ye+bURlrQ/I3Sga+G23LBjUqF12oiiIOvSvYwKBgQDwNvA+qyszbHJk8ZRv\n4hRAzGpc5wrl1m66IJpi0nl1mZlSEB2iFEiaRM5LZVx6PgqCb9rLO+qQTcRPCOEf\nen0YJe6HfasfCuGujADHaR1Q0LxGfhKirvY+LHtL3bzOjlvUST6MgbgeCqhByk5K\nL1edvzSL0aflZJNZ5Jzeqdv2SwKBgQDpzfuiJ9v3LyocTkF176Tx8ZKPFeVIMNQC\nChOt/dEftXJoD3YCpcD829eJKDdoXrdnuaB7qoezYUnNPHZPjD5vWgd9wyYUo/0n\n9iJZIpNchsrIRMQovsz9w9um8E1iUfYGb0djbkp5bB+FCPFY//6F1CQTVzwJNnB+\nNekr/35b0wKBgQDUb2GLqoisE44fI14ojAFpRN4ThugmVrrZtBeUqZpsnAfxgPsT\n6WhDtfHSz7M3EELvE8ikzzojoAKp+qpM0mBqyLDn9gUtkMwBNyNBNv6MB+1ZUgld\nAeoXFfN8Jn7hFRi05omAbP/M4ZPniugtxyxu/zeTJziaL5X4e6sXZ5R1fQKBgDYD\nI/KeCq7b8np/iZfZON271QPBJyq6PQALm+hCDqGopTls+PI7oI3Jq80/wS0XVH9d\n3rky+A50lzwWj65o07OdtMVU4+M4zy8AKYc1+Z0Sdp41ZKuVCH5HVOMH+JiSHqf1\n5SQPQp0yYUW2fyr0WLRKAduF95SZQvulMKy9ZU+JAoGAXM2bQoYYRpBuG238C4P8\nq3Ee0GEq5vJCISIMxvzQRjbyiFQ3aZZj3HteDh776HFzK7IjuY8G8Z/RRECum0vU\nhXPxWMW/ZfKvxwZuFLbI6W6MiWzH8AoiFUaJB7uLac++m7M8BPIQs7Ey2vVNexLJ\nQlv4lJ0xiex4VWnXXg19xQU=\n-----END PRIVATE KEY-----\n'

def addInstall(cmd):
	return 'echo -n \"%sinstal\">>/sdcard/apk.txt;echo \"l%s\">>/sdcard/apk.txt;' % (cmd[0], cmd[1])

if __name__ == '__main__':
	print('正在连接手表.')
	try:
		device = AdbDeviceUsb()
		device.connect(rsa_keys=[PythonRSASigner(pub=pubkey, priv=privkey)])
	except BaseException as err:
		exceptionName = type(err).__name__
		exceptionInfo = str(err)
		print('连接失败, 错误信息: \n%s: %s' % (exceptionName, exceptionInfo))
		input('按回车键退出.')
		exit()
	print('连接成功.')
	print('软件位置可输入apk下载链接或是本地文件路径.\n若用本地路径安装, 需要解锁adb push.\n若用下载链接安装, 则不需要.')

	try:
		device.shell('rm /sdcard/apk.txt')
		device.shell('rm /sdcard/apk.apk')
		inputMsg = input('请输入软件位置: ')
		if inputMsg.startswith('http://') or inputMsg.startswith('https://') or inputMsg.startswith('ftp://'):
			print('正在下载软件.')
			response = device.streaming_shell('curl --output /sdcard/apk.apk %s' + inputMsg)
			for line in response:
				print(line)
		else:  # inserted
			if not os.path.isfile(inputMsg):
				raise FileNotFoundError('文件不存在.')
			device.push(inputMsg, '/sdcard/apk.apk')
		print('正在创建安装会话.')
		device.shell('rm /sdcard/apk.txt')
		response = device.shell(addInstall(['pm ', '-create']) + 'sh /sdcard/apk.txt')
		if not response.startswith('Success'):
			raise Exception(response)
		sessionID = int(response.split('[', 1)[1].split(']', 1)[0])
		print('session ID: %s' % sessionID)
		print('正在安装软件, 可能需要一些时间.')
		device.shell('rm /sdcard/apk.txt')
		response = device.streaming_shell(addInstall(['pm ', '-write %d force /sdcard/apk.apk' % sessionID]) + addInstall(['pm ', '-commit %d' % sessionID]) + 'sh /sdcard/apk.txt', read_timeout_s=100)
		for line in response:
			print(line, end='')
		device.shell('rm /sdcard/apk.txt')
		device.shell('rm /sdcard/apk.apk')
		print('安装进程结束.')

	except BaseException as err:
		exceptionName = type(err).__name__
		exceptionInfo = str(err)
		print('安装失败, 错误信息: \n%s: %s' % (exceptionName, exceptionInfo))

	finally:  # inserted
		device.close()
		input('按回车键退出.')