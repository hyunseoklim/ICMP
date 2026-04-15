from django.db import models
from accounts.models import User


class GasSensor(models.Model):
    STATUS_CHOICES = [('normal', '정상'), ('caution', '주의'), ('danger', '위험'), ('offline', '오프라인')]

    sensor_id = models.CharField('센서ID', max_length=20, unique=True)
    location = models.CharField('위치', max_length=100)
    status = models.CharField('상태', max_length=10, choices=STATUS_CHOICES, default='normal')
    is_connected = models.BooleanField('연결 상태', default=True)
    x_position = models.FloatField('X 좌표', default=0)
    y_position = models.FloatField('Y 좌표', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '유해가스 센서'

    def __str__(self):
        return self.sensor_id


class GasReading(models.Model):
    GAS_TYPES = [
        ('O2', '산소'), ('CO', '일산화탄소'), ('CO2', '이산화탄소'),
        ('H2S', '황화수소'), ('H2', '수소'), ('CH4', '메탄'),
        ('C3H8', '프로판'), ('C4H10', '부탄'),
    ]

    sensor = models.ForeignKey(GasSensor, on_delete=models.CASCADE, related_name='readings')
    gas_type = models.CharField('가스 종류', max_length=10, choices=GAS_TYPES)
    value = models.FloatField('농도')
    unit = models.CharField('단위', max_length=10, default='%')
    danger_level = models.CharField('위험도', max_length=10, default='normal')
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '가스 측정값'
        ordering = ['-recorded_at']


class SmartPowerDevice(models.Model):
    STATUS_CHOICES = [('normal', '정상'), ('caution', '주의'), ('danger', '위험'), ('offline', '오프라인')]

    device_id = models.CharField('설비ID', max_length=20, unique=True)
    name = models.CharField('설비명', max_length=100)
    load_rate = models.FloatField('부하율(%)', default=0)
    temperature = models.FloatField('온도(℃)', default=0)
    status = models.CharField('상태', max_length=10, choices=STATUS_CHOICES, default='normal')
    is_connected = models.BooleanField('연결 상태', default=True)
    x_position = models.FloatField('X 좌표', default=0)
    y_position = models.FloatField('Y 좌표', default=0)

    class Meta:
        verbose_name = '스마트 전력 설비'

    def __str__(self):
        return self.name


class Worker(models.Model):
    STATUS_CHOICES = [('normal', '정상'), ('caution', '주의'), ('danger', '위험')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    worker_id = models.CharField('작업자ID', max_length=20, unique=True)
    status = models.CharField('현재 상태', max_length=10, choices=STATUS_CHOICES, default='normal')
    is_on_site = models.BooleanField('현장 출입 여부', default=False)
    last_connected = models.DateTimeField('마지막 연결 시간', null=True, blank=True)
    app_connected = models.BooleanField('앱 연결 상태', default=False)
    x_position = models.FloatField('X 좌표', default=0)
    y_position = models.FloatField('Y 좌표', default=0)

    class Meta:
        verbose_name = '작업자'

    def __str__(self):
        return f'{self.worker_id} - {self.user.get_full_name()}'

