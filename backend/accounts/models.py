from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('worker', '작업자'),
        ('manager', '관리자'),
        ('admin', '시스템관리자'),
    ]

    department = models.CharField('소속', max_length=100, blank=True)
    position = models.CharField('직급', max_length=50, blank=True)
    phone = models.CharField('연락처', max_length=20, blank=True)
    role = models.CharField('역할', max_length=20, choices=ROLE_CHOICES, default='worker')
    employee_id = models.CharField('사번', max_length=20, blank=True)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return f'{self.get_full_name()} ({self.username})'
