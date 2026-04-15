from datetime import date, datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

CHECKLIST_ITEMS = [
    {'id': 1, 'category': 'work_area', 'category_name': '작업 구역 안전 확인', 'order': 1, 'content': '작업 구역 내 위험구역 표시 및 출입 통제 상태를 확인하였다.'},
    {'id': 2, 'category': 'work_area', 'category_name': '작업 구역 안전 확인', 'order': 2, 'content': '작업 구역 바닥 상태(미끄럼, 철편, 자재 등)가 안전한 것을 확인하였다.'},
    {'id': 3, 'category': 'work_area', 'category_name': '작업 구역 안전 확인', 'order': 3, 'content': '작업 구역 내 낙하물 위험이 없는 것을 확인하였다.'},
    {'id': 4, 'category': 'work_area', 'category_name': '작업 구역 안전 확인', 'order': 4, 'content': '작업 구역 내 작업 통로 및 이동 동선이 확보되어 있는 것을 확인하였다.'},
    {'id': 5, 'category': 'work_area', 'category_name': '작업 구역 안전 확인', 'order': 5, 'content': '작업 구역 주변에서 크레인 또는 중장비 작업 여부를 확인하였다.'},
    {'id': 6, 'category': 'work_area', 'category_name': '작업 구역 안전 확인', 'order': 6, 'content': '작업 구역 주변 고소 작업이 진행 중인지 확인하였다.'},
    {'id': 7, 'category': 'piping', 'category_name': '배관 작업 안전 확인', 'order': 1, 'content': '작업 대상 배관의 압력 상태를 확인하였다.'},
    {'id': 8, 'category': 'piping', 'category_name': '배관 작업 안전 확인', 'order': 2, 'content': '작업 대상 배관 내 가스 또는 유체 잔존 여부를 확인하였다.'},
    {'id': 9, 'category': 'piping', 'category_name': '배관 작업 안전 확인', 'order': 3, 'content': '배관 차단 밸브 상태를 확인하였다.'},
    {'id': 10, 'category': 'piping', 'category_name': '배관 작업 안전 확인', 'order': 4, 'content': '배관 작업 구역의 누출 위험이 없는 것을 확인하였다.'},
    {'id': 11, 'category': 'piping', 'category_name': '배관 작업 안전 확인', 'order': 5, 'content': '배관 작업 구역의 환기 상태를 확인하였다.'},
    {'id': 12, 'category': 'welding', 'category_name': '용접 및 화기 작업 확인', 'order': 1, 'content': '용접 및 화기 작업 허가서를 확인하였다.'},
    {'id': 13, 'category': 'welding', 'category_name': '용접 및 화기 작업 확인', 'order': 2, 'content': '화기 작업 주변 인화성 물질이 없는 것을 확인하였다.'},
    {'id': 14, 'category': 'welding', 'category_name': '용접 및 화기 작업 확인', 'order': 3, 'content': '화재 감시자가 배치되어 있는 것을 확인하였다.'},
    {'id': 15, 'category': 'welding', 'category_name': '용접 및 화기 작업 확인', 'order': 4, 'content': '소화기 및 화재 대응 장비 위치를 확인하였다.'},
    {'id': 16, 'category': 'high_work', 'category_name': '고소 작업 확인', 'order': 1, 'content': '고소 작업 발판 및 작업대 상태를 확인하였다.'},
    {'id': 17, 'category': 'high_work', 'category_name': '고소 작업 확인', 'order': 2, 'content': '작업 발판이 고정되어 있는 것을 확인하였다.'},
    {'id': 18, 'category': 'high_work', 'category_name': '고소 작업 확인', 'order': 3, 'content': '낙하물 방지 조치가 되어 있는 것을 확인하였다.'},
    {'id': 19, 'category': 'high_work', 'category_name': '고소 작업 확인', 'order': 4, 'content': '작업 구역 하부 접근 통제가 되어 있는 것을 확인하였다.'},
    {'id': 20, 'category': 'equipment', 'category_name': '설비 및 장비 확인', 'order': 1, 'content': '사용 장비(그라인더, 절단기, 용접기 등) 이상 여부를 확인하였다.'},
    {'id': 21, 'category': 'equipment', 'category_name': '설비 및 장비 확인', 'order': 2, 'content': '전기 케이블 및 장비 전원 상태를 확인하였다.'},
    {'id': 22, 'category': 'equipment', 'category_name': '설비 및 장비 확인', 'order': 3, 'content': '이동 장비(지게차, 크레인 등) 작업 반경을 확인하였다.'},
    {'id': 23, 'category': 'equipment', 'category_name': '설비 및 장비 확인', 'order': 4, 'content': '장비 작업 반경 내 접근 위험 요소가 없는 것을 확인하였다.'},
    {'id': 24, 'category': 'gas_env', 'category_name': '가스 및 환경 위험 확인', 'order': 1, 'content': '작업 구역 가스 감지 시스템 상태를 확인하였다.'},
    {'id': 25, 'category': 'gas_env', 'category_name': '가스 및 환경 위험 확인', 'order': 2, 'content': '가스 누출 경고 또는 알림이 없는 것을 확인하였다.'},
    {'id': 26, 'category': 'gas_env', 'category_name': '가스 및 환경 위험 확인', 'order': 3, 'content': '작업 구역 환기 상태를 확인하였다.'},
    {'id': 27, 'category': 'gas_env', 'category_name': '가스 및 환경 위험 확인', 'order': 4, 'content': '밀폐 공간 작업 여부를 확인하였다.'},
    {'id': 28, 'category': 'workers', 'category_name': '주변 작업자 안전 확인', 'order': 1, 'content': '주변 작업자와 작업 구역이 중복되지 않는 것을 확인하였다.'},
    {'id': 29, 'category': 'workers', 'category_name': '주변 작업자 안전 확인', 'order': 2, 'content': '협착 및 충돌 위험이 없는 작업 동선을 확보하였다.'},
    {'id': 30, 'category': 'emergency', 'category_name': '비상 대응 확인', 'order': 1, 'content': '비상 대피 경로를 확인하였다.'},
    {'id': 31, 'category': 'emergency', 'category_name': '비상 대응 확인', 'order': 2, 'content': '비상 상황 발생 시 대응 절차를 인지하였다.'},
    {'id': 32, 'category': 'emergency', 'category_name': '비상 대응 확인', 'order': 3, 'content': '응급 장비 및 비상 연락 체계를 확인하였다.'},
    {'id': 33, 'category': 'final', 'category_name': '최종 확인', 'order': 1, 'content': '작업 전 안전 상태를 모두 확인하였으며 안전 절차를 준수하여 작업을 진행하겠습니다.'},
]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checklist_items(request):
    return Response(CHECKLIST_ITEMS)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def safety_history(request):
    today = date.today()
    mock_history = []
    for i in range(15):
        d = date(today.year, today.month, i + 1) if i + 1 <= today.day else None
        if d:
            mock_history.append({
                'date': str(d),
                'ppe_confirmed': i % 3 != 0,
                'checklist_completed': i % 4 != 1,
                'vr_completed': i % 5 != 2,
            })
    return Response({'month': f'{today.year}-{today.month:02d}', 'history': mock_history})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_checklist(request):
    checked_ids = request.data.get('checked_ids', [])
    total = len(CHECKLIST_ITEMS)
    if len(checked_ids) < total:
        return Response({'error': '모든 항목을 체크해주세요.'}, status=400)
    return Response({'success': True, 'message': '안전 확인 체크리스트가 완료되었습니다.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_vr_progress(request):
    seconds = request.data.get('seconds', 0)
    return Response({'success': True, 'saved_seconds': seconds})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_vr(request):
    return Response({'success': True, 'message': '작업 전 안전 확인이 완료되었습니다.'})


# ============ Django Template Views ============

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, date

@login_required(login_url='login')
def safety_checklist_template_view(request):
    """안전 체크리스트 (템플릿)"""
    if request.method == 'POST':
        checked_ids = request.POST.getlist('checked_ids')
        if len(checked_ids) < len(CHECKLIST_ITEMS):
            return render(request, 'safety_checklist.html', {
                'items': CHECKLIST_ITEMS,
                'checked_ids': checked_ids,
                'error': '모든 항목을 체크해주세요.',
                'today': date.today().strftime('%Y-%m-%d'),
            })
        return redirect('safety_vr')

    categories = {}
    for item in CHECKLIST_ITEMS:
        cat = item['category_name']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    return render(request, 'safety_checklist.html', {
        'items': CHECKLIST_ITEMS,
        'categories': categories,
        'today': date.today().strftime('%Y-%m-%d'),
    })


@login_required(login_url='login')
def safety_vr_template_view(request):
    """VR 교육 (템플릿)"""
    if request.method == 'POST':
        return redirect('safety_history')
    
    return render(request, 'safety_vr.html', {
        'vr_duration': 60,
        'today': date.today().strftime('%Y-%m-%d'),
    })


@login_required(login_url='login')
def safety_history_template_view(request):
    """안전 이력 (템플릿)"""
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month

    # Mock 이력 데이터
    history = [
        {'date': f'{year:04d}-{month:02d}-01', 'ppe_confirmed': False, 'checklist_completed': True, 'vr_completed': True},
        {'date': f'{year:04d}-{month:02d}-02', 'ppe_confirmed': True, 'checklist_completed': False, 'vr_completed': True},
        {'date': f'{year:04d}-{month:02d}-03', 'ppe_confirmed': True, 'checklist_completed': True, 'vr_completed': False},
        {'date': f'{year:04d}-{month:02d}-04', 'ppe_confirmed': True, 'checklist_completed': True, 'vr_completed': True},
    ]

    data = {
        'year': year,
        'month': month,
        'month_name': f'{year}년 {month}월',
        'history': history,
    }
    return render(request, 'safety_history.html', data)
