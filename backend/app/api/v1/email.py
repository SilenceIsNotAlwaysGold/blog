from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.email import EmailSend
from app.services.email import get_email_service
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.utils.response import success, error

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/send", response_model=dict)
async def send_email(
    email_data: EmailSend,
    current_user: User = Depends(get_current_user)
):
    """发送邮件（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can send emails"
        )

    email_service = get_email_service()
    if not email_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email service not configured"
        )

    success_sent = await email_service.send_email(
        to_email=email_data.to_email,
        subject=email_data.subject,
        content=email_data.content,
        content_type=email_data.content_type
    )

    if not success_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email"
        )

    return success(message="Email sent successfully")


@router.post("/test", response_model=dict)
async def test_email(
    to_email: str,
    current_user: User = Depends(get_current_user)
):
    """发送测试邮件（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can send test emails"
        )

    email_service = get_email_service()
    if not email_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email service not configured"
        )

    success_sent = await email_service.send_email(
        to_email=to_email,
        subject="Test Email from Personal Blog",
        content="<p>This is a test email. If you received this, the email service is working correctly.</p>",
        content_type="html"
    )

    if not success_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send test email"
        )

    return success(message="Test email sent successfully")
