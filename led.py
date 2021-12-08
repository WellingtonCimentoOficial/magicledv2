import socket
import os
import platform
import time
from colorama import init, Fore, Style, Back
import db

init() #init of colorama

ip = "47.88.59.195"
port1 = 80
port2 = 8080

on = "71230fa3"
off = "71240fa4"

sys_op = platform.system()

msg_success = Fore.GREEN + '[+] Success' + Style.RESET_ALL
msg_error = Fore.RED + '[-] Error' + Style.RESET_ALL
msg_connection_error = Fore.RED + '[-] Error establishing connection' + Style.RESET_ALL
msg_error_recv_data = Fore.RED + '[-] Error receving command' + Style.RESET_ALL
msg_error_send_data = Fore.RED + '[-] Error sending command' + Style.RESET_ALL
msg_timeout_error = Fore.YELLOW + '[-] TimeOut' + Style.RESET_ALL
msg_request_incorret = Fore.YELLOW + '[-] Request Incorrect' + Style.RESET_ALL
msg_invalid_command = Fore.RED + '[-] Invalid Command' + Style.RESET_ALL
msg_token_invalid = Fore.YELLOW + '[-] Token Invalid' + Style.RESET_ALL
msg_no_device_response = Fore.YELLOW + '[-] No device response' + Style.RESET_ALL
msg_start_connection = Fore.YELLOW + '[*] Start connection' + Style.RESET_ALL
msg_already_disconnected = Fore.YELLOW + '[*] Already disconnected' + Style.RESET_ALL
msg_already_connected = Fore.YELLOW + '[*] Already connected' + Style.RESET_ALL
msg_device_added = Fore.GREEN + '[+] Device successfully added' + Style.RESET_ALL
msg_device_not_added = Fore.RED + '[-] Device not added' + Style.RESET_ALL
msg_add_device_name = Fore.YELLOW + '[*] Add device name' + Style.RESET_ALL
msg_rem_success = Fore.GREEN + '[+] Device successfully removed' + Style.RESET_ALL
msg_rem_not_removed = Fore.RED + '[-] Device not removed' + Style.RESET_ALL
msg_no_devices = Fore.YELLOW + '[*] No devices' + Style.RESET_ALL
msg = ['EMPTY']

status = Back.RED + 'Disconnected' + Style.RESET_ALL
status_checker = False

commands_send_action = ['turn on', 'turn off']

def modify_headers(header, token):
	if header == 'checker':
		header_checker = [
			"POST /app/sendRequestCommand/ZG001 HTTP/1.1",
			"User-Agent: Magic Home/1.8.1(ANDROID,10,pt-BR)",
			"Accept-Language: pt-BR",
			"AppBuildVer: 175",
			"Accept: application/json",
			"token: " + token,
			"Content-Type: application/json; charset=utf-8",
			"Content-Length: 69",
			"Host: wifij01us.magichue.net",
			"Connection: Keep-Alive",
			"Accept-Encoding: gzip",
			"",
			'{"macAddress":"20521CCDA8FB","hexData":"818a8b96","responseCount":14}'
		]
		return header_checker
	elif header == 'on':
		header_on = [
			"POST /app/sendCommandBatch/ZG001 HTTP/1.1",
			"User-Agent: Magic Home/1.8.1(ANDROID,10,pt-BR)",
			"Accept-Language: pt-BR",
			"AppBuildVer: 175",
			"Accept: application/json",
			"token: " + token,
			"Content-Type: application/json; charset=utf-8",
			"Content-Length: 73",
			"Host: wifij01us.magichue.net",
			"Connection: Keep-Alive",
			"Accept-Encoding: gzip",
			"",
			'{"dataCommandItems":[{"hexData":"' + on + '","macAddress":"10521CCDA8FB"}]}'
		]
		return header_on
	elif header == 'off':
		header_off = [
			"POST /app/sendCommandBatch/ZG001 HTTP/1.1",
			"User-Agent: Magic Home/1.8.1(ANDROID,10,pt-BR)",
			"Accept-Language: pt-BR",
			"AppBuildVer: 175",
			"Accept: application/json",
			"token: " + token,
			"Content-Type: application/json; charset=utf-8",
			"Content-Length: 73",
			"Host: wifij01us.magichue.net",
			"Connection: Keep-Alive",
			"Accept-Encoding: gzip",
			"",
			'{"dataCommandItems":[{"hexData":"' + off + '","macAddress":"10521CCDA8FB"}]}'
		]
		return header_off
	else:
		print('this header not exist')

def banner():
	banner_content = [	'███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗    ██╗     ███████╗██████╗',
						'████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝    ██║     ██╔════╝██╔══██╗',
						'██╔████╔██║███████║██║  ███╗██║██║         ██║     █████╗  ██║  ██║',
						'██║╚██╔╝██║██╔══██║██║   ██║██║██║         ██║     ██╔══╝  ██║  ██║',
						'██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗    ███████╗███████╗██████╔╝',
						'╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝    ╚══════╝╚══════╝╚═════╝ v2.0',
	Style.BRIGHT + 		'                                         Created by: Wellington Cimento\n'
	]
	for linha in banner_content:
		print(linha)

def menu():
	print(Style.BRIGHT + "IP: " + Fore.GREEN + ip + Style.RESET_ALL + Style.BRIGHT + "     Port1: " + Fore.GREEN + str(port1) + Style.RESET_ALL + Style.BRIGHT + "     Port2: " + Style.RESET_ALL + str(port2) + Style.BRIGHT + "     Status: " + status + Style.RESET_ALL)
	print(Style.BRIGHT + "\nCommands: " + Style.RESET_ALL + "turn on *device*, turn off *device*, list device *device*,\nlist devices, add device *name*, delete device *name*, list token\n")

def connection():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(0.5)
	try:
		s.connect((ip, port1))
	except:
		return False
	return s

def send_header(connection, header, msg):
	for linha in header:
		try:
			connection.send(linha.encode() + b'\r\n')
		except:
			print(msg_error_send_data)
	try:
		data = connection.recv(1024)
		return data
	except Exception as e:
		if "TimeoutError" in str(e):
			msg.append(msg_timeout_error)
		else:
			msg.append(msg_error_recv_data)
	try:
		connection.close()
	except:
		time.sleep(5)

def send(header, msg, connection):
	data = send_header(connection, header, msg)
	data_checker = verify_jason_response(data)
	if data_checker == 'ok':
		send_header(connection, header, msg)
		msg.append(msg_success)
	elif data_checker == 'tk':
		msg.append(msg_token_invalid)
	elif data_checker == 'nqr':
		msg.append(msg_no_device_response)
	elif data_checker == 'er':
		msg.append(msg_request_incorret)

def verify_menu_selection(op, connection):
	global status
	global status_checker
	if op == "connect":
		if status_checker == False:
			verify_connection(connection)
			status_checker = True
		else:
			msg.append(msg_already_connected)
	elif op == "disconnect":
		if status_checker == True:
			connection.close()
			status_checker = False
			status = Back.RED + 'Disconnected' + Style.RESET_ALL
		else:
			msg.append(msg_already_disconnected)
	elif op.split()[0] == 'turn' and op.split()[1] == 'on' and len(op.split()) == 3:
		if status_checker == True:
			try:
				device = op.split()[2]
				token = db.list_device(device)
				send(modify_headers('on', token), msg, connection)
			except:
				msg.append(msg_add_device_name)
		else:
			msg.append(msg_start_connection)
	elif op.split()[0] == 'turn' and op.split()[1] == 'off' and len(op.split()) == 3:
		if status_checker == True:
			try:
				device = op.split()[2]
				token = db.list_device(device)
				send(modify_headers('off', token), msg, connection)
			except:
				msg.append(msg_add_device_name)
		else:
			msg.append(msg_start_connection)
	elif op.split()[0] == 'add' and op.split()[1] == 'device' and len(op.split()) == 4:
		try:
			device = op.split()[2]
			token = op.split()[3]
			print(op)
			if db.add_token(device, token) == True:
				msg.append(msg_device_added)
			else:
				msg.append(msg_device_not_added)
		except:
			msg.append(msg_add_device_name)
	elif op.split()[0] == 'delete' and op.split()[1] == 'device' and len(op.split()) == 3:
		try:
			device = op.split()[2]
			if db.rem_token(device) == True:
				msg.append(msg_rem_success)
			else:
				msg.append(msg_rem_not_removed)
		except:
			msg.append(msg_add_device_name)
	elif op.split()[0] == 'list' and op.split()[1] == 'device' and len(op.split()) == 3:
		try:
			device = op.split()[2]
			msg.append(db.list_device(device))
		except:
			msg.append(msg_add_device_name)
	elif op.split()[0] == 'list' and op.split()[1] == 'token' and len(op.split()) == 3:
		try:
			device = op.split()[2]
			msg.append(db.list_device(device))
		except:
			msg.append(msg_add_device_name)
	elif op == 'list devices':
		devices = db.list_devices()
		if not len(devices) == 0:
			for item in devices:
				for device in item:
					msg.append('Device: ' + device)
		else:
			msg.append(msg_no_devices)
	elif op == 'exit':
		exit_exit()
	else:
		if op in commands_send_action:
			msg.append(msg_start_connection)
		else:
			msg.append(msg_invalid_command)

def verify_jason_response(html):
	if "HTTP/1.1 200" in str(html):
		return 'ok'
	elif "Token is invalid" in str(html):
		return 'tk'
	elif "No equipment response" in str(html):
		return 'nqr'
	else:
		return 'er'

def clear_screen():
	if sys_op == "Windows":
		os.system('cls')
	elif sys_op == "Linux":
		os.system('clear')
	else:
		print("unknown operating system")

def verify_message():
	if 'EMPTY' not in msg:
		if len(msg) > 1 and msg == msg[-1]:
			msg.remove(msg[-0])
			clear_screen()
			banner()
			menu()
			for message in msg:
				print(message)
		else:
			clear_screen()
			banner()
			menu()
			for message in msg:
				print(message)
	else:
		msg.remove(msg[-0])
		clear_screen()
		banner()
		menu()

def verify_connection(connection):
	if not connection == False:
		global status
		status = Back.GREEN + Style.BRIGHT + 'Connected' + Style.RESET_ALL
		return connection
	else:
		clear_screen()
		print(msg_connection_error)
		time.sleep(3)
		exit_exit()

def exit_exit():
	clear_screen()
	print('Exiting...')
	time.sleep(3)
	exit()

def run():
	db.create_database()
	while True:
		socket_connection = connection()
		verify_message()
		print('')
		op = input(Style.BRIGHT + ">: " + Style.RESET_ALL)
		verify_menu_selection(op, socket_connection)

if __name__ == "__main__":
	run()
