import datetime

from django.conf import settings
from celery import shared_task
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from newsapp.models import Post, Category


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/{pk}'

        }
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def email_after_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()

    subscribers: list[str] = []
    for category in categories:
        subscribers += User.objects.filter(
            subscriptions__category=category
        ).all()

    subscribers = [s.email for s in subscribers]

    send_notifications(post.preview(), post.pk, post.title, subscribers)


@shared_task
def posts_email_weekly():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)

    categories = []
    for post in posts:
        categories += post.postCategory.all()
    categories = set(categories)

    subscribers = []
    for category in categories:
        subscribers += User.objects.filter(
            subscriptions__category=category
        ).all()
    subscribers = set(subscribers)

    for subscriber in subscribers:
        subscriber_categories = []
        subscriber_categories += Category.objects.filter(subscriptions__user=subscriber).all()

        subscribers_posts = []
        for post in posts:
            cats = post.postCategory.all()
            if any(map(lambda v: v in cats, subscriber_categories)):
                subscribers_posts.append(post)

        html_content = render_to_string(
            'daily_post.html',
            {
                'posts': subscribers_posts,
                'link': f'http://127.0.0.1:8000/'

            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
