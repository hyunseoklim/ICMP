from django.db import models
from devices.models import SmartPowerDevice


class PowerReading(models.Model):
    """
    스마트 파워 시스템 전력 측정 데이터
    PDF 기준 - 채널 16개 (slave01~slave16), 전류/전압/전력
    통신 불능 시 -1
    """
    device           = models.ForeignKey(SmartPowerDevice, on_delete=models.CASCADE, related_name='readings')
    software_version = models.CharField(max_length=20, null=True, blank=True)

    channel     = models.CharField('채널', max_length=10, help_text='slave01~slave16')
    current     = models.FloatField('전류(A)', null=True, blank=True, help_text='통신불능=-1')
    voltage     = models.FloatField('전압(V)', null=True, blank=True, help_text='통신불능=-1')
    power_usage = models.FloatField('전력(W)', null=True, blank=True, help_text='통신불능=-1')
    relay_state = models.BooleanField('릴레이 상태', default=False, help_text='전원 ON=True / OFF=False')

    measured_at = models.DateTimeField('측정시간', auto_now_add=True)

    class Meta:
        db_table            = 'power_reading'
        ordering            = ['-measured_at']
        verbose_name        = '전력 측정값'
        verbose_name_plural = '전력 측정값 목록'

    def __str__(self):
        status = 'ON' if self.relay_state else 'OFF'
        return f'[{self.device.device_id}] {self.channel} {status} {self.measured_at}'
