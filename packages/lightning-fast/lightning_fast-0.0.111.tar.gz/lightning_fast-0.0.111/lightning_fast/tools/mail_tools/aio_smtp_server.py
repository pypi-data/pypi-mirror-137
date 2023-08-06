from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict, Optional

import aiosmtplib

from lightning_fast.tools.mail_tools.smtp_base import SmtpBase


class AioSmtpServer(SmtpBase):
    """
    使用此类可以异步方式发送邮件
    """

    def __init__(self, host: str, email_from: str):
        self.host = host
        self.email_from = email_from

    async def send_email_to_one(
        self, to: str, subject: str, title: str, content: str, to_name: str = None
    ) -> None:
        """
        :param to: 邮件发送至地址
        :param subject: 邮件主题
        :param title: 邮件内容中标题
        :param content: 邮件内容
        :param to_name: 邮件发送至名字
        :return: 无返回
        """
        # await smtp.login(self.email_from, None)
        smtp = aiosmtplib.SMTP(hostname=self.host, port=25)
        async with smtp:
            message = MIMEMultipart("mixed")
            msg = MIMEText(
                self.get_common_html_email_content(title, content, to, to_name),
                "html",
                "utf-8",
            )
            message["From"] = self.email_from
            message["To"] = to
            message["Subject"] = subject
            message.attach(msg)
            await smtp.send_message(message)

    async def send_email_to_many(
        self,
        tos: List[str],
        subject: str,
        title: str,
        content: str,
        from_name: Optional[str] = None,
        bytes_mapping: Optional[Dict[str, bytes]] = None,
    ) -> None:
        """
        :param tos: 邮件发送至地址列表
        :param subject: 邮件主题
        :param title: 邮件内容中标题
        :param content: 邮件内容
        :param from_name: 邮件发送人名字
        :param bytes_mapping: 文件名与文件bytes对应的mapping
        :return: 无返回
        """
        # await smtp.login(self.email_from, None)
        if not bytes_mapping:
            bytes_mapping = {}
        smtp = aiosmtplib.SMTP(hostname=self.host, port=25)
        async with smtp:
            message = MIMEMultipart("mixed")
            msg = MIMEText(
                self.get_html_content_with_hello(title, content, "您好", from_name),
                "html",
                "utf-8",
            )
            message["From"] = self.email_from
            message["To"] = ",".join(tos)
            message["Subject"] = subject
            message.attach(msg)
            for name, bytes_like in bytes_mapping.items():
                part = MIMEApplication(bytes_like, Name=name)
                part["Content-Disposition"] = 'attachment; filename="%s"' % name
                message.attach(part)
            await smtp.send_message(message, recipients=tos)

    async def send_email_to_team_leader_with_cc(
        self,
        to: str,
        cc: list,
        subject: str,
        title: str,
        content: str,
        from_name: str = None,
    ) -> None:
        """
        :param to: 邮件发送至地址
        :param cc: 抄送地址
        :param subject: 邮件主题
        :param title: 邮件内容中标题
        :param content: 邮件内容
        :param from_name: 邮件发送人名字
        :return: 无返回
        """
        # await smtp.login(self.email_from, None)
        smtp = aiosmtplib.SMTP(hostname=self.host, port=25)
        async with smtp:
            message = MIMEMultipart("mixed")
            msg = MIMEText(
                self.get_html_content_with_hello(title, content, "您好", from_name),
                "html",
                "utf-8",
            )
            message["From"] = self.email_from
            message["To"] = to
            message["Cc"] = ",".join(cc)
            message["Subject"] = subject
            message.attach(msg)
            await smtp.send_message(message)
