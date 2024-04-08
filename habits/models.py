from django.conf import settings
from django.db import models


NULLABLE = {'blank': True, 'null': True}

class Habit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=150, verbose_name='место')
    time = models.TimeField(default='12:00:00', verbose_name='время')
    date = models.DateField(verbose_name='дата', **NULLABLE)
    action = models.CharField(max_length=100, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      verbose_name='связанная привычка', **NULLABLE)
    reward = models.CharField(max_length=250, verbose_name='вознаграждение', **NULLABLE)
    duration = models.PositiveIntegerField(verbose_name='длительность выполнения', ** NULLABLE)
    periodicity = models.IntegerField(default=1, verbose_name='периодичность', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f'{self.owner} будет {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
