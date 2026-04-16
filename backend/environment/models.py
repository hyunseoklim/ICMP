from django.db import models


class EnvironmentData(models.Model):
    """
    환경 데이터 (온도, 습도, GPS 위치)
    """
    device_id = models.CharField('장치ID', max_length=50)
    temp      = models.FloatField('온도(°C)', null=True, blank=True)
    humi      = models.FloatField('습도(%)',  null=True, blank=True)
    lat       = models.FloatField('위도',     null=True, blank=True)
    lon       = models.FloatField('경도',     null=True, blank=True)
    timestamp = models.DateTimeField('측정시간', auto_now_add=True)

    class Meta:
        db_table            = 'environment_data'
        ordering            = ['-timestamp']
        verbose_name        = '환경 데이터'
        verbose_name_plural = '환경 데이터 목록'

    def __str__(self):
        return f'[{self.device_id}] {self.timestamp}'
