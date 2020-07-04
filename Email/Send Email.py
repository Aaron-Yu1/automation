import smtplib
from email.mime.text import MIMEText
from email.header import Header


mail_host = "smtp.qq.com"
mail_user = "XXXXXXXXXX@qq.com"
mail_pass = "XXXXXXXXX"

subject = "Python E-Mail Test"
sender = "<the email address of the sender>"
to_receiver = ["<the email address of the receiver>"]
cc_receiver = ["<the email address of the CC receiver>"]
receivers = to_receiver + cc_receiver

message = MIMEText("Hi,\n\nThis is Python Challenge test email, please ignore it. \n\nRegards,\nAaron" , "plain", "UTF-8")
message["Subject"] = Header(subject, "UTF-8")
message["From"] = sender
message['To'] = ";".join(to_receiver)
message["Cc"] = ";".join(cc_receiver)

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()
    print("Email sent successfully")
except smtplib.SMTPException:
    print("Error")