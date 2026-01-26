from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class EmailConfig(BaseModel):
    """邮件配置模型"""
    smtp_host: str = Field(..., description="SMTP 服务器地址")
    smtp_port: int = Field(default=587, description="SMTP 端口")
    smtp_user: str = Field(..., description="SMTP 用户名")
    smtp_password: str = Field(..., description="SMTP 密码")
    from_email: EmailStr = Field(..., description="发件人邮箱")
    from_name: str = Field(default="Personal Blog", description="发件人名称")
    use_tls: bool = Field(default=True, description="是否使用 TLS")


class EmailSend(BaseModel):
    """发送邮件请求模型"""
    to_email: EmailStr = Field(..., description="收件人邮箱")
    subject: str = Field(..., min_length=1, max_length=200, description="邮件主题")
    content: str = Field(..., min_length=1, description="邮件内容（支持 HTML）")
    content_type: str = Field(default="html", description="内容类型: html/plain")


class EmailTemplate(BaseModel):
    """邮件模板模型"""
    template_type: str = Field(..., description="模板类型: welcome/comment/reply")
    variables: dict = Field(default_factory=dict, description="模板变量")
