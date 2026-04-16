from django.db import models


STATUS_CHOICES = [
    ('normal',  '정상'),
    ('caution', '주의'),
    ('danger',  '위험'),
    ('offline', '오프라인'),
]


class GasSensor(models.Model):
    """
    유해가스 센서 장치 메타 정보
    """
    sensor_id        = models.CharField('센서ID', max_length=50, unique=True)
    device_name      = models.CharField('장치명', max_length=100, null=True, blank=True)
    software_version = models.CharField('소프트웨어 버전', max_length=20, null=True, blank=True)
    location         = models.CharField('위치', max_length=100)
    status           = models.CharField('상태', max_length=10, choices=STATUS_CHOICES, default='normal')
    is_connected     = models.BooleanField('연결 상태', default=True)
    x_position       = models.FloatField('X 좌표', default=0)
    y_position       = models.FloatField('Y 좌표', default=0)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'gas_sensor'
        verbose_name        = '유해가스 센서'
        verbose_name_plural = '유해가스 센서 목록'

    def __str__(self):
        return self.sensor_id


class SmartPowerDevice(models.Model):
    """
    스마트 전력 설비 장치 메타 정보
    """
    device_id        = models.CharField('설비ID', max_length=50, unique=True)
    device_name      = models.CharField('설비명', max_length=100, null=True, blank=True)
    software_version = models.CharField('소프트웨어 버전', max_length=20, null=True, blank=True)
    status           = models.CharField('상태', max_length=10, choices=STATUS_CHOICES, default='normal')
    is_connected     = models.BooleanField('연결 상태', default=True)
    x_position       = models.FloatField('X 좌표', default=0)
    y_position       = models.FloatField('Y 좌표', default=0)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'smart_power_device'
        verbose_name        = '스마트 전력 설비'
        verbose_name_plural = '스마트 전력 설비 목록'

    def __str__(self):
        return self.device_id
