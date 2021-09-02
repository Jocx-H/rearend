from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from dao import crud
import smtplib
import json

# 读取本地邮箱设置
with open("config.json") as f:
    email_configs = json.load(f)['email']

def send_email_to_everyone(message: str):
    r"""
    给每个人都发一封邮件
    """
    infos = crud.select_items('user_inf', ['username', 'name', 'email'], where=None)
    for info in infos:
        if info['email'] is not None and len(info['email']) > 0:
            send_email(info['username']+" "+info['name'], message, to_addr = info['email'])

def send_email_by_username(username, message):
    infos = crud.select_items(
        'user_inf', ['username', 'name', 'email'], where={'username':username})
    if infos is not None and len(infos) > 0:
        info = infos[0]
        send_email(info['username']+" "+info['name'],
                   message, to_addr=info['email'])

def send_email(receiver: str, message: str, to_addr: str):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = _format_addr('员工之家 <%s>' % email_configs['from_addr'])
    msg['To'] = _format_addr(f'{receiver} <{to_addr}>')
    msg['Subject'] = Header('来自员工之家的提醒……', 'utf-8').encode()

    server = smtplib.SMTP(email_configs['smtp_server'], 25)
    server.set_debuglevel(1)
    server.login(email_configs['from_addr'], email_configs['pwd'])
    server.sendmail(email_configs['from_addr'], [to_addr], msg.as_string())
    server.quit()
