'''
这个文件用于存放函数，所有功能都应该以函数的形式实现，方便以后更改。
'''
import os
import sys
import json
import getopt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import paramiko

# 用于实现远程连接，在远程主机上运行 shell 命令
def RemoteConnect(host, port, user, password, command):
    # Create object of SSHClient and
    # connecting to SSH
    ssh = paramiko.SSHClient()

    # Adding new host key to the local
    # HostKeys object(in case of missing)
    # AutoAddPolicy for missing host key to be set before connection setup.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(host, port=port, username=user,
                password=password, timeout=3)

    # Execute command on SSH terminal
    # using exec_command
    stdin, stdout, stderr = ssh.exec_command(command)

    print(stdout.read())
    print(stderr.read())

# 从远程主机下载文件，如，日志文件
def DownloadFile(host, port, user, password, remote_path, filename):
    # 获取Transport实例
    tran = paramiko.Transport((host, port))

    # 连接SSH服务端，使用password
    tran.connect(username=user, password=password)
    # 或使用
    # 配置私人密钥文件位置
    # private = paramiko.RSAKey.from_private_key_file('/Users/root/.ssh/id_rsa')
    # 连接SSH服务端，使用pkey指定私钥
    # tran.connect(username="root", pkey=private)

    # 获取SFTP实例
    sftp = paramiko.SFTPClient.from_transport(tran)

    # 获取程序当前路径
    current_path = os.path.realpath(__file__)
    directory_path = os.path.dirname(current_path)

    # 设置上传的本地/远程文件路径
    localpath = directory_path + "/" + filename
    remotepath = remote_path

    # 执行上传动作
    # sftp.put(localpath, remotepath)
    # 执行下载动作
    sftp.get(remotepath, localpath)

    tran.close()

# 参数化，以实现铭感信息通过参数的方式传递给脚本
def Args(argv):
    user_info = {}
    try:
        '''
        参数说明
        H: 获取帮助
        u: ssh 用户名
        p: ssh 密码
        h: 远程主机
        P: 远程端口
        e: 发件人邮箱地址
        s: 发件人邮箱密码
        r: 收件人邮箱地址
        '''
        opts, args = getopt.getopt(argv, 'H:u:p:h:P:e:s:t:',['help=', 'user=', 'password=', 'host=', 'port=', 'email=', 'sender_password=', 'to='])
    except getopt.GetoptError:
        print ('This is a help.')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-H", "--help"):
            print ('This is a help.')
            sys.exit()
        elif opt in ('-u', '--user'):
            user_info['user'] = arg
        elif opt in ('-p', '--password'):
            user_info['password'] = arg
        elif opt in ('-h', '--host'):
            user_info['host'] = arg
        elif opt in ('-P', '--port'):
            user_info['port'] = int(arg)
        elif opt in ('-e', '--email'):
            user_info['email'] = arg
        elif opt in ('-s', '--sender_password'):
            user_info['sender_password'] = arg
        elif opt in ('-t', '--to'):
            user_info['to'] = arg
    return user_info

# 统计下载的日志文件中，IP 地址的信息。返回一个字典，key 为 IP 地址，value 为当日，此 IP 访问的次数。
def Web_Access(file_name):
    access = {}
    with open(file_name, 'r', encoding="utf-8") as f:
        for i in f:
            if '\\' in i:
                i = i.replace('\\', '\\\\')
            load_dict = json.loads(i)
            # print(load_dict)
            clint_ip = load_dict['clientip']
            if clint_ip not in access.keys():
                access[clint_ip] = 1
            if clint_ip in access.keys():
                key = access[clint_ip]
                access[clint_ip] = key + 1

    return access

# 统计日志文件中，整个 IP 地址的数量。
def TotalAccess(file_name):
    total = 0
    with open(file_name, 'r', encoding="utf-8") as f:
        for i in f:
            if '\\' in i:
                i = i.replace('\\', '\\\\')
            load_dict = json.loads(i)
            total = total + 1

    return total

# 以邮件的方式，通知到指定的人员。
def SendEmail(sender, sender_password, receiverreve, html):
    # 邮件信息
    part = MIMEText(html, "html")

    # 添加邮件信息
    msg = MIMEMultipart()
    msg.attach(part)

    # 发件信息
    msg['From'] = sender
    msg['To'] = receiverreve
    msg['Subject'] = "Web Site Access"

    try:
        # SMTP 配置
        s = smtplib.SMTP("smtp.office365.com",587)

        # Hostname to send for this command defaults to the fully qualified domain name of the local host.
        s.ehlo()

        # Puts connection to SMTP server in TLS mode
        s.starttls()
        s.ehlo()

        # 登录
        s.login(sender, sender_password)

        # 发送邮件
        s.sendmail(sender, receiverreve, msg.as_string())

        # 退出
        s.quit()

    except smtplib.SMTPException:
        print("Error")

