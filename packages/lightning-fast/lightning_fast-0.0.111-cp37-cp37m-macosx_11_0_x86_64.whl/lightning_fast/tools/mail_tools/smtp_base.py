from datetime import date


class SmtpBase:
    @classmethod
    def get_common_html_email_content(
        cls,
        title: str,
        content: str,
        to: str,
        from_name: str = None,
        to_name: str = None,
    ) -> str:
        """
        :param title: 邮件正文中的标题
        :param content: 邮件内容
        :param to: 邮件发送至地址
        :param from_name: 邮件发送名字
        :param to_name: 邮件发送至名字
        :return: html版内容
        """
        to_name = to_name if to_name else to
        time_string = date.today()
        email_content = f"""
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
            "https://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="https://www.w3.org/1999/xhtml">
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                    <title>{title}</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                </head>
                <body style="margin: 0; padding: 0;">
                    <div>Hi {to_name},</div>
                    <p>{content}</p>
                    <div style="position: fixed; right: 0; bottom: 0;">
                        <div>{'统计服务' if not from_name else from_name}</div>
                        <div>{time_string}</div>
                    </div>
                </body>
            </html>
        """
        return email_content

    @classmethod
    def get_html_content_with_hello(
        cls,
        title: str,
        content: str,
        hello: str,
        from_name: str,
    ) -> str:
        """
        :param title: 邮件正文中的标题
        :param content: 邮件内容
        :param hello: 邮件第一行
        :param from_name: 邮件发送人名字
        :return: html版内容
        """
        time_string = date.today()
        email_content = f"""
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
            "https://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="https://www.w3.org/1999/xhtml">
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                    <title>{title}</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                </head>
                <body style="margin: 0; padding: 0;">
                    <div>{hello},</div>
                    <p>{content}</p>
                    <div style="position: fixed; right: 0; bottom: 0;">
                        <div>{from_name}</div>
                        <div>{time_string}</div>
                    </div>
                </body>
            </html>
        """
        return email_content
