from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class Post(models.Model):
    title = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )

    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)


class Read(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_reads',
        verbose_name='Пользователь'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='read_posts',
        verbose_name='Пост'
    )

    class Meta:
        verbose_name = 'Прочитанный'
        verbose_name_plural = 'Прочитанные'
