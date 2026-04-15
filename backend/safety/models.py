from django.db import models
from accounts.models import User


class SafetyChecklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='safety_checklists')
    date = models.DateField('점검 날짜')
    checklist_completed = models.BooleanField('체크리스트 완료', default=False)
    vr_completed = models.BooleanField('VR 교육 완료', default=False)
    ppe_confirmed = models.BooleanField('PPE 착용 확인', default=False)
    vr_progress_seconds = models.IntegerField('VR 진행 시간(초)', default=0)
    completed_at = models.DateTimeField('완료 시간', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '안전 확인 이력'
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.date}'


class ChecklistItem(models.Model):
    CATEGORY_CHOICES = [
        ('work_area', '작업 구역 안전 확인'),
        ('piping', '배관 작업 안전 확인'),
        ('welding', '용접 및 화기 작업 확인'),
        ('high_work', '고소 작업 확인'),
        ('equipment', '설비 및 장비 확인'),
        ('gas_env', '가스 및 환경 위험 확인'),
        ('workers', '주변 작업자 안전 확인'),
        ('emergency', '비상 대응 확인'),
        ('final', '최종 확인'),
    ]

    category = models.CharField('카테고리', max_length=20, choices=CATEGORY_CHOICES)
    order = models.IntegerField('순서')
    content = models.TextField('항목 내용')
    is_active = models.BooleanField('활성화', default=True)

    class Meta:
        verbose_name = '체크리스트 항목'
        ordering = ['category', 'order']

    def __str__(self):
        return f'[{self.get_category_display()}] {self.content[:50]}'


class ChecklistResponse(models.Model):
    checklist = models.ForeignKey(SafetyChecklist, on_delete=models.CASCADE, related_name='responses')
    item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE)
    is_checked = models.BooleanField('체크 여부', default=False)

    class Meta:
        unique_together = ['checklist', 'item']

