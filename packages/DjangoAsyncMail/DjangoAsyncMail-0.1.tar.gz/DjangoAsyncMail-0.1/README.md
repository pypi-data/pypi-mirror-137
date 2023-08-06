# DjangoAsyncMail


DjangoAsyncMail is a Django app to send email asynchronously. This is a light-weight app using only Python threading for sending emails. It is meant for casual emails, like sending account activation mail from your website when account activation is optional.

Detailed documentation is in [this post](https://jayeshmahato.com/blog/technology/djangoasyncmail).

## Quick start

1. Add "DjangoAsyncMail" to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        ...
        'DjangoAsyncMail',
    ]
    ```

2. Remember to add EMAIL_HOST_USER segment is your main Django project settings like this
    ```
    # SMTP Mail Settings
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.yourdomainname.com'
    EMAIL_USE_TLS = False
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'noreply@yourdomainname.com'
    EMAIL_HOST_PASSWORD = 'your_email_password'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    ```


3. Import and call the send_html_mail function with variables wherever you need like this
    ```
    from DjangoAsyncMail.mail import send_html_mail

    send_html_mail(subject,email_body,recipient_list,reply_to)

    Example:
    send_html_mail('Testing','Test HTML Content',['example@example.com'],['noreply@yourdomainname.com'])
    ```
4. Check email delivery in Recipient's mailbox.
