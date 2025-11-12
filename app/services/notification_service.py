async def send_email_notification(notification):
    
    print(f"[EMAIL] To user_id={notification.user_id}: {notification.message}")

async def send_sms_notification(notification):
    
    print(f"[SMS] To user_id={notification.user_id}: {notification.message}")
