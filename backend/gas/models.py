from django.db import models
from devices.models import GasSensor


class GasReading(models.Model):
    """
    유해가스 센서 측정 데이터
    에어위드 1분 1회 전송 - 9개 가스 한 행에 저장
    """
    class DangerLevel(models.TextChoices):
        DANGER  = "위험", "위험"
        WARNING = "주의", "주의"
        NORMAL  = "정상", "정상"

    sensor           = models.ForeignKey(GasSensor, on_delete=models.CASCADE, related_name='readings')
    software_version = models.CharField(max_length=20, null=True, blank=True)

    # 9개 가스
    co  = models.FloatField('일산화탄소(ppm)', null=True, blank=True)
    h2s = models.FloatField('황화수소(ppm)',   null=True, blank=True)
    co2 = models.FloatField('이산화탄소(ppm)', null=True, blank=True)
    o2  = models.FloatField('산소(%)',         null=True, blank=True)
    no2 = models.FloatField('이산화질소(ppm)', null=True, blank=True)
    so2 = models.FloatField('이산화황(ppm)',   null=True, blank=True)
    o3  = models.FloatField('오존(ppm)',       null=True, blank=True)
    nh3 = models.FloatField('암모니아(ppm)',   null=True, blank=True)
    voc = models.FloatField('휘발성유기화합물(ppm)', null=True, blank=True)

    danger_level = models.CharField(
        '위험도',
        max_length=5,
        choices=DangerLevel.choices,
        default=DangerLevel.NORMAL,
    )
    measured_at = models.DateTimeField('측정시간', auto_now_add=True)

    def calc_danger_level(self):
        """PDF 임계치 정의서 기반 위험도 자동 판별"""
        if self.o2 is not None:
            if self.o2 < 16:
                return self.DangerLevel.DANGER
            elif self.o2 < 18:
                return self.DangerLevel.WARNING

        thresholds = {
            'co':  (25,   200  ),
            'h2s': (10,   15   ),
            'co2': (1000, 5000 ),
            'no2': (3,    5    ),
            'so2': (2,    5    ),
            'o3':  (0.06, 0.12 ),
            'nh3': (25,   35   ),
            'voc': (0.5,  1.0  ),
        }
        for gas, (warn, danger) in thresholds.items():
            value = getattr(self, gas)
            if value is None:
                continue
            if value >= danger:
                return self.DangerLevel.DANGER
            elif value >= warn:
                return self.DangerLevel.WARNING

        return self.DangerLevel.NORMAL

    def save(self, *args, **kwargs):
        self.danger_level = self.calc_danger_level()
        super().save(*args, **kwargs)

    class Meta:
        db_table            = 'gas_reading'
        ordering            = ['-measured_at']
        verbose_name        = '가스 측정값'
        verbose_name_plural = '가스 측정값 목록'

    def __str__(self):
        return f'[{self.sensor.sensor_id}] {self.measured_at} ({self.danger_level})'
