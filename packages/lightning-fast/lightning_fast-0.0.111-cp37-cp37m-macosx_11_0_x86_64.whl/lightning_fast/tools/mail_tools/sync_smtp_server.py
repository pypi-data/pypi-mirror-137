import smtplib
from email.header import Header
from email.mime.text import MIMEText

from lightning_fast.tools.mail_tools.smtp_base import SmtpBase


class SyncSmtpServer(SmtpBase):
    def __init__(self, host, email_from, password=None):
        self.host = host
        self.email_from = email_from
        self.password = password

    def _init_server(self):
        server = smtplib.SMTP(self.host)
        if self.email_from and self.password:
            server.login(self.email_from, self.password)
        return server

    def send_email_to_one(
        self, to: str, subject: str, title: str, content: str, to_name: str = None
    ) -> None:
        html_content = self.get_common_html_email_content(title, content, to, to_name)
        msg = MIMEText(html_content, _subtype="html")
        server = self._init_server()
        msg["From"] = self.email_from
        msg["To"] = to
        msg["Subject"] = Header(subject)
        server.sendmail(self.email_from, to, msg.as_string())
        server.close()
