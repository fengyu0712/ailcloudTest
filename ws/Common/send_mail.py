import re
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from Common.log import Logger


# conf_path= Project_path.Conf_path + "mail.conf"
class Mail:
    def __init__(self):
        # conf=Read_conf(conf_path)
        self.senter = 'lijq36@midea.com'
        self.passwords = 'li777777.'
        self.mail_host = 'mail.midea.com'
        self.mail_post = 994
        self.receiver = ['lijq36@midea.com']
        self.senter_name = "李建强"
        self.receiver_name = str(self.receiver).replace('[', '').replace(']', '')
        self.msg = MIMEMultipart()

    def creat_mail(self, subject, text=None):
        if text is None:
            text = ""
        self.msg['From'] = Header(self.senter_name, 'utf-8')
        self.msg['To'] = Header(self.receiver_name, 'utf-8')
        self.msg['Subject'] = Header(subject, 'utf-8')  # 添加主题
        self.msg.attach(MIMEText(text, 'plain', 'utf-8'))

    def add_attach(self, path, ismsg=None):
        file_name = re.split("/", path)[-1]
        part = MIMEBase('application', "octet-stream")
        content = part.set_payload(open(path, "rb").read())
        encoders.encode_base64(part)
        print(file_name)
        part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file_name))
        if ismsg:
            self.msg.attach(MIMEText(str(content), 'html', 'utf-8'))  # 添加邮件正文
        self.msg.attach(part)

    def add_attach1(self, path):
        file_name = re.split("/", path)[-1]
        content = MIMEApplication(open(path, 'rb').read())
        content.add_header('Content-Disposition', 'attachment',
                           filename=('gbk', '', file_name))  # 注意：此处basename要转换为gbk编码，否则中文会有乱码。
        try:
            self.msg.attach(content)
        except Exception as e:
            Logger().error("附件添加失败:%s" % e)

    def sent_mail(self):
        smtp = smtplib.SMTP_SSL(self.mail_host, self.mail_post)  # 构建smtp实例化
        # smtp.connect()  # 链接邮箱服务器
        smtp.login(self.senter, self.passwords)  # 登录邮箱
        smtp.sendmail(self.senter, self.receiver, self.msg.as_string())  # 发送邮件
        Logger().info("邮件发送成功!")


excel_path = "E:/ws/test_result/result.xlsx"
report_path = "E:/ws/Test Results - pytest_in_testASR001_py.html"
if __name__ == '__main__':
    # subject0 = '这是邮件主题'
    # report_fail = "E:/ws//test_result//result.xlsx"
    a = "E:\\ws\\log\\2020-06-24.log"
    m = Mail()
    m.creat_mail("test")
    m.add_attach(a)
    m.sent_mail()
