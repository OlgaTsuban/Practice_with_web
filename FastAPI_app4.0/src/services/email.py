from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from src.conf.config import config
from src.services.auth import auth_service
from pathlib import Path # TEMPLATE_FOLDER=Path(__file__).parent / 'templates'

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_USERNAME,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME="Your Contacts Systems",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER="/Users/olgatsyban/Documents/GoIT/FastAPI_app/src/services/templates",
    
)

# This function has responsibility to send emails
async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to verify their account.
        The function takes in three parameters:
            - email: the user's email address, which is used as a unique identifier for each account.
            - username: the name of the user that will be displayed on their profile page and in other places throughout Contacts Systems.  This parameter is not required, but it helps personalize emails sent by Contacts Systems and makes them more friendly for users who are new to our service.
            - host: this parameter specifies where we want users to go when they click on links contained within emails sent
    
    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Pass the username to the template
    :param host: str: Pass the hostname of the server to the email template
    :return: A coroutine object
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Your Contacts Systems",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="verify_email.html")
    except ConnectionErrors as err:
        print(err)

# This function has responsibility to send emails for reset password
async def send_email_reset_password(email: EmailStr, username: str, host: str):
    """
    The send_email_reset_password function sends an email to the user with a link to reset their password.
        The function takes in three parameters:
            - email: the user's email address, as a string.
            - username: the user's username, as a string.  This is used for personalization of the message body and subject line.
            - host: this is used for personalization of the message body and subject line.
    
    :param email: EmailStr: Specify the email address of the user
    :param username: str: Pass the username of the user to be sent an email
    :param host: str: Pass the hostname of the server to be used in the email template
    :return: A response object
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Your Contacts Systems",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        #response = 
        await fm.send_message(message, template_name="reset_password.html")
        # print("Email sent successfully")
        # print("Response:", response)
    
    except ConnectionErrors as err:
        print(err)