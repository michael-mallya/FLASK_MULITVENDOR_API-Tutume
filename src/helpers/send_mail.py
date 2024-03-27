
from flask_mail import Message
from src.extension import mail
from flask import render_template
from src.helpers.gen_token import get_token
from src.settings import SITE_NAME,MAIL_USERNAME,EMAIL_VERIFICATION


def send_email(user, subject, template):
    """ Send email """
    token = get_token(user.get("id"))
    if EMAIL_VERIFICATION:
        msg = Message(subject,
                    sender=(SITE_NAME,MAIL_USERNAME), recipients=[user.get('email')])
        msg.html = render_template(template, user=user, token=token)

        mail.send(msg)
    return token 