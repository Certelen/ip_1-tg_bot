from django.db import models


class Channel(models.Model):
    name = models.CharField(
        'Название канала',
        max_length=200
    )
    tg_id = models.CharField(
        'id канала'
    )
    tg_link = models.CharField(
        'Ссылка на канал',
        max_length=200
    )

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    def __str__(self):
        return 'Канал ' + self.name


class FAQ(models.Model):
    quituestion = models.CharField(
        'Вопрос',
        max_length=200
    )
    answer = models.CharField(
        'Ответ',
        max_length=200
    )

    class Meta:
        verbose_name = 'Часто задаваемый вопросы'
        verbose_name_plural = 'Часто задаваемые вопросы'
