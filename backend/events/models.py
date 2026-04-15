from django.db import models
from accounts.models import User


class Event(models.Model):
    DANGER_CHOICES = [('caution', '주의'), ('danger', '위험')]
    STATUS_CHOICES = [('pending', '조치 필요'), ('in_progress', '조치 중'), ('completed', '조치 완료')]
    SOURCE_CHOICES = [('gas', '유해가스 센서'), ('power', '스마트 전력'), ('worker', '작업자'), ('area', '위험구역')]

    no = models.AutoField(primary_key=True)
    danger_level = models.CharField('위험 상태', max_length=10, choices=DANGER_CHOICES)
    action_status = models.CharField('조치 상태', max_length=20, choices=STATUS_CHOICES, default='pending')
    event_name = models.CharField('이벤트명', max_length=200)
    source = models.CharField('발생원', max_length=100)
    source_type = models.CharField('발생원 유형', max_length=10, choices=SOURCE_CHOICES)
    detail = models.TextField('상세 내용', blank=True)
    recommended_action = models.TextField('권고 조치', blank=True)
    related_workers = models.ManyToManyField(User, blank=True, verbose_name='연관 작업자')
    occurred_at = models.DateTimeField('발생 시간', auto_now_add=True)
    resolved_at = models.DateTimeField('조치 완료 시간', null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='resolved_events', verbose_name='조치자'
    )

    class Meta:
        verbose_name = '이벤트'
        ordering = ['-occurred_at']

    def __str__(self):
        return f'[{self.get_danger_level_display()}] {self.event_name}'

