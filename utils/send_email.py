from exts import mail


def send_email_async(msg):
    from app import create_app
    app = create_app()
    with app.app_context():
        mail.send(msg)