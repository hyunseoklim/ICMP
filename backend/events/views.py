from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

MOCK_EVENTS = [
    {
        'no': 1, 'danger_level': 'danger', 'action_status': 'pending',
        'event_name': '유해가스 초과', 'source': 'GAS-001', 'source_type': 'gas',
        'detail': 'GAS-001 센서 농도 21.00% 위험 도달, 즉시 대피하십시오!\n근근 작업자 즉시 대피가 필요하며 연동 통기 및 누출 원인 점검이 요구됩니다.',
        'recommended_action': '1. 작업자 전원 긴급 알림 발송\n2. 현장 작업 중지 및 대피 안내\n3. 환기 설비 기동\n4. 센서/설비 상태 점검 후 조치 상태 갱신',
        'related_target': '타입: 유해가스 센서\n대상 ID: GAS-001 / 연관 작업자: W-003, W-004',
        'trend': '최근 10분간 O2 농도 상승 추세, 임계치 재도달 가능성 높음',
        'occurred_at': '2026-01-15 12:00:00', 'related_workers': ['W-001', 'W-003'],
    },
    {
        'no': 2, 'danger_level': 'danger', 'action_status': 'in_progress',
        'event_name': '유해가스 초과', 'source': 'GAS-001', 'source_type': 'gas',
        'detail': 'GAS-001 센서 CO 농도 890ppm 위험 수준 초과',
        'recommended_action': '1. 해당 구역 즉시 대피\n2. 환기 강화\n3. 누출 원인 조사',
        'related_target': '대상 ID: GAS-001 / 연관 작업자: W-001',
        'trend': '지속 상승 추세',
        'occurred_at': '2026-01-15 12:00:30', 'related_workers': ['W-001'],
    },
    {
        'no': 3, 'danger_level': 'caution', 'action_status': 'pending',
        'event_name': '전력 과부하 경고', 'source': 'DEV-001', 'source_type': 'power',
        'detail': '설비 1 부하율 92% 초과, 과열 위험',
        'recommended_action': '1. 부하 분산 조치\n2. 냉각 시스템 점검\n3. 설비 재가동 준비',
        'related_target': '설비: DEV-001 설비 1',
        'trend': '지속 증가 추세',
        'occurred_at': '2026-01-15 11:30:00', 'related_workers': [],
    },
    {
        'no': 4, 'danger_level': 'danger', 'action_status': 'completed',
        'event_name': '작업자 위험구역 진입', 'source': 'W-001', 'source_type': 'worker',
        'detail': '작업자 홍길동(W-001)이 위험구역 A에 진입하였습니다.',
        'recommended_action': '즉시 대피 지시 및 위험 구역 접근 통제',
        'related_target': '작업자: W-001 홍길동',
        'trend': '-',
        'occurred_at': '2026-01-15 10:00:00', 'related_workers': ['W-001'],
    },
]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_list(request):
    action_filter = request.query_params.get('status', None)
    events = MOCK_EVENTS
    if action_filter:
        events = [e for e in events if e['action_status'] == action_filter]
    return Response({
        'total': len(events),
        'pending': sum(1 for e in MOCK_EVENTS if e['action_status'] == 'pending'),
        'in_progress': sum(1 for e in MOCK_EVENTS if e['action_status'] == 'in_progress'),
        'completed': sum(1 for e in MOCK_EVENTS if e['action_status'] == 'completed'),
        'events': events,
    })


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def event_detail(request, no):
    event = next((e for e in MOCK_EVENTS if e['no'] == int(no)), None)
    if not event:
        return Response({'error': '이벤트를 찾을 수 없습니다.'}, status=404)

    if request.method == 'PATCH':
        new_status = request.data.get('action_status')
        if new_status in ['pending', 'in_progress', 'completed']:
            event['action_status'] = new_status
            if new_status == 'completed':
                event['resolved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return Response(event)

    return Response(event)


# ============ Django Template Views ============

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def events_template_view(request):
    """이벤트 목록 (템플릿)"""
    action_filter = request.GET.get('status', 'all')
    events_data = MOCK_EVENTS
    if action_filter != 'all':
        events_data = [e for e in events_data if e['action_status'] == action_filter]
    
    data = {
        'events': events_data,
        'total': len(MOCK_EVENTS),
        'pending': sum(1 for e in MOCK_EVENTS if e['action_status'] == 'pending'),
        'in_progress': sum(1 for e in MOCK_EVENTS if e['action_status'] == 'in_progress'),
        'completed': sum(1 for e in MOCK_EVENTS if e['action_status'] == 'completed'),
        'filter': action_filter,
    }
    return render(request, 'events.html', data)


@login_required(login_url='login')
def event_detail_template_view(request, id):
    """이벤트 상세 (템플릿)"""
    event = next((e for e in MOCK_EVENTS if e['no'] == int(id)), None)
    if not event:
        return render(request, '404.html', {'message': '이벤트를 찾을 수 없습니다.'}, status=404)

    if request.method == 'POST':
        new_status = request.POST.get('action_status')
        if new_status in ['pending', 'in_progress', 'completed']:
            event['action_status'] = new_status
            if new_status == 'completed':
                event['resolved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render(request, 'event_detail.html', {'event': event})
