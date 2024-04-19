from netmiko import ConnectHandler, NetmikoTimeoutException, NetMikoAuthenticationException
from netmiko import Netmiko
from tkinter import *
from tkinter.ttk import *
from socket import *
from sys import *
from paramiko.ssh_exception import AuthenticationException

# Using readLines to gather device IPs from text file
file1 = open('iplist.txt', 'r')
IPs = file1.readlines()

# Define username and password to login to devices
count = len(IPs)
devices = []
username = input("Enter your username: ")
password = input("Enter your password: ")
config = ['boot-start-marker',
          'no boot system flash bootflash:/isr4400-universalk9.17.03.03.SPA.bin',
          'no boot system flash bootflash:/isr4400-universalk9.16.09.07.SPA.bin',
          'no boot system flash bootflash:/isr1738.bin',
          'boot system flash bootflash:/isr1767.bin',
          'boot system flash bootflash:/isr1738.bin',
          'boot system flash bootflash:/isr4400-universalk9.17.03.03.SPA.bin',
          'boot system flash bootflash:/isr4400-universalk9.16.09.07.SPA.bin',
          'boot-end-marker'
          ]

for x in IPs:
    cisco_4431 = {
        'device_type': 'cisco_ios',
        'host': IPs[count - 1],
        'username': username,
        'password': password,
        'port': 22,  # optional, defaults to 22
    }
    count = count - 1
    devices.append(cisco_4431)


def show_version():
    for host in devices:
        try:
            net_connect = ConnectHandler(**host)
            output = net_connect.send_command('show version')
            if '17.06.07' in output:
                print(host)
                print('Above has correct firmware')
            else:
                print(host)
                print('Above has WRONG firmware')
        except (NetmikoTimeoutException, NetMikoAuthenticationException, AuthenticationException):
            print('Failed to connect to below host')
            print(host)
            continue
    print("Finished")


def show_flash():
    for host in devices:
        try:
            net_connect = ConnectHandler(**host)
            output = net_connect.send_command('dir flash:')
            if 'isr1767.bin' in output:
                print(host)
                print('Above is ready to reboot')
        except (NetmikoTimeoutException, NetMikoAuthenticationException, AuthenticationException):
            print('Failed to connect to')
            print(host)
            continue
    print("Finished")


def copy_firmware():
    for host in devices:
        try:
            net_connect = ConnectHandler(**host)
            output = net_connect.send_command_timing('copy ftp://ciscofirm:nununuCund1!!@172.31.45.84/isr1767.bin '
                                                     'flash:')
            if 'Destination filename' in output:
                output += net_connect.send_command_timing("\n")
            print(output)
        except (NetmikoTimeoutException, NetMikoAuthenticationException, AuthenticationException):
            print('Failed to connect to')
            print(host)
            continue
    print("Finished")


def clean_switch():
    for host in devices:
        try:
            net_connect = ConnectHandler(**host)
            output = net_connect.send_command_timing('request platform software package clean switch all')
            if 'want' in output:
                output += net_connect.send_command_timing("y")
            print(output)
        except (NetmikoTimeoutException, NetMikoAuthenticationException, AuthenticationException):
            print('Failed to connect to')
            print(host)
            continue
    print("Finished")


def switch_install():
    for host in devices:
        try:
            net_connect = ConnectHandler(**host)
            output = net_connect.send_command_timing('request platform software package install switch all file '
                                                     'flash:filename.bin auto-copy verbose')
            net_connect.save_config()
            print(output)
        except (NetmikoTimeoutException, NetMikoAuthenticationException, AuthenticationException):
            print('Failed to connect to')
            print(host)
            continue
    print("Finished")


def change_config():
    for host in devices:
        try:
            net_connect = ConnectHandler(**host)
            output = net_connect.send_config_set(config) + net_connect.save_config()
            print(output)
        except (NetmikoTimeoutException, NetMikoAuthenticationException, AuthenticationException):
            print('Failed to connect to')
            print(host)
            continue
    print("Finished")


def reload_router():
    for host in devices:
        try:
            net_connect = ConnectHandler(**host)
            output = net_connect.send_command_timing(command_string="reload", cmd_verify=True)
            print(host)
            print(output)
            if 'Proceed' in output:
                output += net_connect.send_command("\n")
        except OSError:
            continue
        except (NetmikoTimeoutException, NetMikoAuthenticationException, AuthenticationException):
            print('Failed to connect to')
            print(host)
            continue
    print("Finished")


# Create Object
root = Tk()

# Initialize tkinter window with dimensions 100x100
root.geometry('500x500')
btn = Button(root, text='Show Version Devices !', command=lambda: show_version())
btn2 = Button(root, text='Copy Firmware Routers !', command=lambda: copy_firmware())
btn3 = Button(root, text='Change Config Routers !', command=lambda: change_config())
btn4 = Button(root, text='Reload Devices !', command=lambda: reload_router())
btn5 = Button(root, text='Flash Check Router !', command=lambda: show_flash())
btn6 = Button(root, text='Clean Switch !', command=lambda: clean_switch())
btn7 = Button(root, text='Install Switch Firmware !', command=lambda: switch_install())
btn.pack(side='top')
btn2.pack(side='top')
btn3.pack(side='top')
btn4.pack(side='bottom')
btn5.pack(side='top')
btn6.pack(side='top')
btn7.pack(side='top')
root.mainloop()
