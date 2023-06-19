from django.core.mail import send_mail

#DOMAIN_NAME = 'http://localhost:8080'
DOMAIN_NAME = "http://themebuysell.com"
EMAIL_URL = "{}/#/confirm-email-done".format(DOMAIN_NAME)
PASSWORD_RESET_URL = "{}/#/set-new-password".format(DOMAIN_NAME)
FROM_EMAIL = 'bflsample2018@gmail.com'


class Verification:
    def send_email_verification_code(self, email, code):
        make_url = "{}/{}/{}/".format(EMAIL_URL, email, code)
        send_mail(
            'Email Verification',
            "Please clicked on the bellow link or paste it to the browser to verify your account :\n\n {}"
            .format(make_url),
            FROM_EMAIL,
            [email],
            fail_silently=False,
        )

    def send_password_reset_email(self, email, code):
        make_url = "{}/{}/{}/".format(PASSWORD_RESET_URL, email, code)
        send_mail(
            'Password Reset',
            "Please clicked on the bellow link or paste it to the browser to reset password :\n\n {}"
            .format(make_url),
            FROM_EMAIL,
            [email],
            fail_silently=False,
        )

    def send_order_confirmation_email(self, email, subject, message):
        send_mail(
            subject,
            message,
            FROM_EMAIL,
            [email],
            fail_silently=False,
        )
