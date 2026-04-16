from django.db import models
from accounts.models import User


class Worker(models.Model):
    """
    현장 작업자 정보
    """
    STATUS_CHOICES = [
        ('normal',  '정상'),
        ('caution', '주의'),
        ('danger',  '위험'),
    ]

    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    worker_id      = models.CharField('작업자ID', max_length=20, unique=True)
    status         = models.CharField('현재 상태', max_length=10, choices=STATUS_CHOICES, default='normal')
    is_on_site     = models.BooleanField('현장 출입 여부', default=False)
    last_connected = models.DateTimeField('마지막 연결 시간', null=True, blank=True)
    app_connected  = models.BooleanField('앱 연결 상태', default=False)
    x_position     = models.FloatField('X 좌표', default=0)
    y_position     = models.FloatField('Y 좌표', default=0)

    class Meta:
        db_table            = 'worker'
        verbose_name        = '작업자'
        verbose_name_plural = '작업자 목록'

    def __str__(self):
        return f'{self.worker_id} - {self.user.get_full_name()}'
