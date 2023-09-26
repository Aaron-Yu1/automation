from modeles import DownloadFile,Args,Web_Access,TotalAccess,SendEmail
import datetime, sys


now_time = datetime.datetime.now()
name_date = int(now_time.strftime('%Y%m%d')) - 1
file_name = "www.access-" + str(name_date) + ".log"
remote_path = "/var/log/nginx/" + file_name

user_info = Args(sys.argv[1:])

DownloadFile(user_info['host'], user_info['port'], user_info['user'], user_info['password'], remote_path, file_name)

access = Web_Access(file_name)
print(access)

total = TotalAccess(file_name)
print(total)

html = """\
<html>
<body>
    <p>Hi Aaron,</p>
    <p>The access number of site is {total}.</p>
</body>
</html>
""".format(total=total)


SendEmail(user_info['email'], user_info['sender_password'], user_info['to'], html)