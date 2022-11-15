from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailSenderMixin:
    queryset = None
    message_template_name: str = None
    subject: str = 'Message subject'
    recipients: list = ['some_user_email@mail.ru', ]
    from_email: str = f'TestingSystem <{settings.EMAIL_HOST_USER}>'
    email_context: dict = {'username': 'SomeUser', 'test_name': 'SomeTest'}

    def get_recipient_list(self):
        return self.recipients

    def get_email_context(self):
        return self.email_context

    def get_queryset(self):
        return self.queryset

    def send_email(self):
        mail_context = self.get_email_context()
        html_message = render_to_string(f'moder_app/email_messages/{self.message_template_name}', mail_context)
        text_message = strip_tags(html_message)
        is_send = send_mail(
            subject=self.subject,
            message=text_message,
            from_email=self.from_email,
            recipient_list=self.get_recipient_list(),
            html_message=html_message
        )
        return is_send
