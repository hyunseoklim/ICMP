# 산재 예방 통합 관제 시스템 (ICMP)

Industrial accident prevention integrated control and monitoring platform built with Django and Chart.js

## 🎯 프로젝트 목표

- **Figma 기반 관제 화면 구현**: 웹 UI 디자인을 실제 웹 화면으로 구현
- **실시간 센서 데이터 대시보드**: 가스, 전력, 작업자 상태를 실시간으로 모니터링
- **사용자 편의성**: 운영자가 주요 상태를 한눈에 파악할 수 있는 인터페이스

## 📋 주요 기능

### 1단계 (현재)
- ✅ Django Template 기반 UI 구현
- ✅ 12개 주요 페이지 구현
  - 인증: 로그인, 프로필
  - 모니터링: 대시보드, 실시간 지도, 가스 센서, 전력 기기, 작업자
  - 이벤트: 목록, 상세 정보
  - 안전: 체크리스트, VR 교육, 이력
- ✅ Chart.js 기반 데이터 시각화
- ✅ Mock 데이터 바인딩
- ✅ 상태별 색상 분류 (정상/주의/위험)

### 2단계 (예정)
- WebSocket 실시간 데이터 연결
- FastAPI 백엔드 통합
- 센서 데이터 실시간 갱신
- 고급 예외 처리

## 🚀 빠른 시작

### 설치
```bash
cd backend
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
```

### 실행
```bash
python3 manage.py runserver 0.0.0.0:8000
```

### 접속
- URL: `http://localhost:8000`
- 테스트 계정: `testuser` / `testpass123`

## 📁 프로젝트 구조

```
ICMP/
├── backend/
│   ├── config/              # Django 프로젝트 설정
│   ├── templates/           # HTML 템플릿 (12개 페이지)
│   ├── static/              # CSS, JavaScript
│   ├── accounts/            # 인증 앱
│   ├── monitoring/          # 모니터링 앱
│   ├── events/              # 이벤트 앱
│   ├── safety/              # 안전 앱
│   ├── manage.py
│   └── requirements.txt
└── venv/                    # Python 가상환경
```

## 📊 주요 페이지

| 페이지 | URL | 기능 |
|--------|-----|------|
| 대시보드 | `/dashboard/` | 센서 요약, Chart.js 차트, 작업자 현황 |
| 실시간 모니터링 | `/monitoring/realtime/` | SVG 지도, 위험구역, 센서 위치 |
| 가스 모니터링 | `/monitoring/gas/` | CO, H2S, CO2 등 8개 가스 신호 |
| 전력 모니터링 | `/monitoring/power/` | 설비 로드율, 온도 모니터링 |
| 작업자 현황 | `/monitoring/workers/` | 작업자 위치, 상태, 알림 |
| 이벤트 | `/events/` | 조치 필요/진행中/완료 필터링 |
| 안전 체크리스트 | `/safety/checklist/` | 33개 항목 체크리스트 |
| VR 교육 | `/safety/vr/` | 60초 타이머 기반 교육 |
| 안전 이력 | `/safety/history/` | 월별 안전 이력 캘린더 |

## 🛠️ 기술 스택

- **백엔드**: Django 6.0+, Django REST Framework
- **프론트엔드**: Django Template, Tailwind CSS, Chart.js
- **인증**: Django Session, JWT (이후 추가)
- **데이터**: Mock Data (Python dict), SQLite (개발용)
- **실시간**: WebSocket (준비 중)

## 📝 입력 데이터 형식

```json
{
  "timestamp": "2026-04-15T10:00:00",
  "device_id": "sensor_01",
  "worker_id": "worker_01",
  "location": { "x": 120, "y": 240 },
  "gas": {
    "co": 18,
    "h2s": 6,
    "co2": 820,
    "o2": 20.3
  },
  "power": {
    "current": 12.4,
    "voltage": 220.1,
    "watt": 2710
  },
  "status": "normal"
}
```

## ✅ 완료 기준

- ✅ 페이지 로딩 시 주요 카드, 차트, 알람 영역 정상 출력
- ✅ 더미 데이터 동일 구조로 화면 반영
- ✅ Chart.js 지속적 데이터 표시
- ✅ 상태값에 따라 색상 즉시 반영
- ✅ 비정상 데이터도 UI 안정성 유지
- ⏳ (다음) WebSocket 실시간 갱신

## 🔗 관련 문서

- [작업 요구사항](./REQUIREMENTS.md) (미구현)
- [API 문서](./API.md) (예정)
- [배포 가이드](./DEPLOY.md) (예정)

## 📞 문의

- 프로젝트 관리자: @hyunseoklim

---

**상태**: 🔄 개발 중 (1단계 완료, 2단계 준비 중)
