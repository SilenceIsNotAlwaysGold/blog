import pytest
from app.schemas.email import EmailSend, EmailConfig, EmailTemplate


def test_email_send_schema():
    """测试发送邮件模型"""
    email_data = {
        "to_email": "user@example.com",
        "subject": "Test Email",
        "content": "<p>Hello World</p>",
        "content_type": "html"
    }

    email = EmailSend(**email_data)
    assert email.to_email == "user@example.com"
    assert email.subject == "Test Email"
    assert email.content == "<p>Hello World</p>"
    assert email.content_type == "html"


def test_email_send_validation():
    """测试邮件发送验证"""
    # 测试无效邮箱
    with pytest.raises(ValueError):
        EmailSend(
            to_email="invalid-email",
            subject="Test",
            content="Content"
        )

    # 测试空主题
    with pytest.raises(ValueError):
        EmailSend(
            to_email="user@example.com",
            subject="",
            content="Content"
        )

    # 测试空内容
    with pytest.raises(ValueError):
        EmailSend(
            to_email="user@example.com",
            subject="Test",
            content=""
        )


def test_email_config_schema():
    """测试邮件配置模型"""
    config_data = {
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_user": "user@gmail.com",
        "smtp_password": "password123",
        "from_email": "noreply@example.com",
        "from_name": "My Blog",
        "use_tls": True
    }

    config = EmailConfig(**config_data)
    assert config.smtp_host == "smtp.gmail.com"
    assert config.smtp_port == 587
    assert config.use_tls is True


def test_email_config_defaults():
    """测试邮件配置默认值"""
    config_data = {
        "smtp_host": "smtp.gmail.com",
        "smtp_user": "user@gmail.com",
        "smtp_password": "password123",
        "from_email": "noreply@example.com"
    }

    config = EmailConfig(**config_data)
    assert config.smtp_port == 587  # 默认值
    assert config.from_name == "Personal Blog"  # 默认值
    assert config.use_tls is True  # 默认值


def test_email_template_schema():
    """测试邮件模板模型"""
    template_data = {
        "template_type": "welcome",
        "variables": {
            "username": "John",
            "email": "john@example.com"
        }
    }

    template = EmailTemplate(**template_data)
    assert template.template_type == "welcome"
    assert template.variables["username"] == "John"


def test_email_content_type_default():
    """测试内容类型默认值"""
    email_data = {
        "to_email": "user@example.com",
        "subject": "Test",
        "content": "Plain text content"
    }

    email = EmailSend(**email_data)
    assert email.content_type == "html"  # 默认值
