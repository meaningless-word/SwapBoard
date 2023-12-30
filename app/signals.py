from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment


@receiver(post_save, sender=Comment)
def comment_created(instance, created, **kwargs):
    if created:
        subject = f'интерес к вашему объявлению'
        text_content = (
            f'Пользователь {instance.linkedUser.username} <{instance.linkedUser.email}>\n'
            f'оставил комментарий {instance.commentText}\n'
            f'к вашему объявлению\n'
        )
        html_content = (
            f'Пользователь {instance.linkedUser.username} <{instance.linkedUser.email}><br>'
            f'оставил комментарий {instance.commentText}<br>'
            f'к вашему объявлению<br>'
        )

        msg = EmailMultiAlternatives(subject, text_content, None, [instance.linkedUser.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

