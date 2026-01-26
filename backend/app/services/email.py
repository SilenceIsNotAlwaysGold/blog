import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.schemas.email import EmailSend


class EmailService:
    """邮件服务类"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        from_email: str,
        from_name: str = "Personal Blog",
        use_tls: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.from_name = from_name
        self.use_tls = use_tls

    async def send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
        content_type: str = "html"
    ) -> bool:
        """发送邮件"""
        try:
            # 创建邮件对象
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            # 添加邮件内容
            mime_type = 'html' if content_type == 'html' else 'plain'
            msg.attach(MIMEText(content, mime_type, 'utf-8'))

            # 连接 SMTP 服务器
            if self.use_tls:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)

            # 登录并发送
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()

            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        """发送欢迎邮件"""
        subject = "Welcome to Personal Blog!"
        content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #409eff;">Welcome, {username}!</h2>
                <p>Thank you for joining our blog community.</p>
                <p>You can now:</p>
                <ul>
                    <li>Read articles on Tech and Life boards</li>
                    <li>Like and comment on articles</li>
                    <li>Explore our projects and skills</li>
                </ul>
                <p>Happy reading!</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">
                    This is an automated message. Please do not reply.
                </p>
            </div>
        </body>
        </html>
        """
        return await self.send_email(to_email, subject, content)

    async def send_comment_notification(
        self,
        to_email: str,
        article_title: str,
        commenter_name: str,
        comment_content: str
    ) -> bool:
        """发送评论通知邮件"""
        subject = f"New comment on: {article_title}"
        content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #409eff;">New Comment</h2>
                <p><strong>{commenter_name}</strong> commented on your article:</p>
                <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p style="margin: 0;">{comment_content}</p>
                </div>
                <p>
                    <a href="#" style="color: #409eff; text-decoration: none;">
                        View article →
                    </a>
                </p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">
                    This is an automated message. Please do not reply.
                </p>
            </div>
        </body>
        </html>
        """
        return await self.send_email(to_email, subject, content)

    async def send_reply_notification(
        self,
        to_email: str,
        article_title: str,
        replier_name: str,
        reply_content: str
    ) -> bool:
        """发送回复通知邮件"""
        subject = f"New reply on: {article_title}"
        content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #67c23a;">New Reply</h2>
                <p><strong>{replier_name}</strong> replied to your comment:</p>
                <div style="background: #f0f9ff; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p style="margin: 0;">{reply_content}</p>
                </div>
                <p>
                    <a href="#" style="color: #409eff; text-decoration: none;">
                        View conversation →
                    </a>
                </p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">
                    This is an automated message. Please do not reply.
                </p>
            </div>
        </body>
        </html>
        """
        return await self.send_email(to_email, subject, content)


# 全局邮件服务实例（从环境变量初始化）
_email_service: Optional[EmailService] = None


def get_email_service() -> Optional[EmailService]:
    """获取邮件服务实例"""
    global _email_service
    if _email_service is None:
        # 从环境变量或配置文件初始化
        # 这里使用占位符，实际应从 app.core.config 读取
        try:
            from app.core.config import settings
            _email_service = EmailService(
                smtp_host=settings.smtp_host,
                smtp_port=settings.smtp_port,
                smtp_user=settings.smtp_user,
                smtp_password=settings.smtp_password,
                from_email=settings.from_email,
                from_name=settings.from_name,
                use_tls=settings.use_tls
            )
        except Exception:
            # 如果配置不存在，返回 None
            pass
    return _email_service
