import random
import json
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def make_trend(base, caution, danger, points=24):
    data = []
    now = datetime.now()
    for i in range(points):
        t = now - timedelta(hours=points - i)
        noise = random.uniform(-base * 0.05, base * 0.05)
        val = round(base + noise, 2)
        level = 'danger' if val >= danger else ('caution' if val >= caution else 'normal')
        data.append({'time': t.strftime('%H:%M'), 'value': val, 'level': level})
    return data


GAS_SENSORS = [
    {
        'sensor_id': 'GAS-001', 'location': '공정구역 A', 'status': 'danger',
        'is_connected': True, 'x_position': 45, 'y_position': 35,
        'gases': [
            {'gas_type': 'O2', 'name': '산소', 'value': 20.0, 'unit': '%', 'danger_level': 'danger', 'caution_threshold': 19.5, 'danger_threshold': 19.0},
            {'gas_type': 'CO', 'name': '일산화탄소', 'value': 890, 'unit': 'ppm', 'danger_level': 'danger', 'caution_threshold': 25, 'danger_threshold': 50},
            {'gas_type': 'CO2', 'name': '이산화탄소', 'value': 9480, 'unit': 'ppm', 'danger_level': 'caution', 'caution_threshold': 5000, 'danger_threshold': 10000},
            {'gas_type': 'H2S', 'name': '황화수소', 'value': 78, 'unit': 'ppm', 'danger_level': 'danger', 'caution_threshold': 5, 'danger_threshold': 10},
            {'gas_type': 'H2', 'name': '수소', 'value': 26040, 'unit': 'ppm', 'danger_level': 'danger', 'caution_threshold': 10000, 'danger_threshold': 20000},
            {'gas_type': 'CH4', 'name': '메탄', 'value': 10, 'unit': '%', 'danger_level': 'caution', 'caution_threshold': 5, 'danger_threshold': 10},
            {'gas_type': 'C3H8', 'name': '프로판', 'value': 2.1, 'unit': '%', 'danger_level': 'normal', 'caution_threshold': 1.7, 'danger_threshold': 2.1},
            {'gas_type': 'C4H10', 'name': '부탄', 'value': 1.8, 'unit': '%', 'danger_level': 'normal', 'caution_threshold': 1.4, 'danger_threshold': 1.8},
        ]
    },
    {'sensor_id': 'GAS-002', 'location': '배관구역 B', 'status': 'caution', 'is_connected': True, 'x_position': 65, 'y_position': 25, 'gases': []},
    {'sensor_id': 'GAS-003', 'location': '용접구역 C', 'status': 'normal', 'is_connected': True, 'x_position': 30, 'y_position': 60, 'gases': []},
    {'sensor_id': 'GAS-004', 'location': '창고 D', 'status': 'offline', 'is_connected': False, 'x_position': 75, 'y_position': 70, 'gases': []},
]

POWER_DEVICES = [
    {'device_id': 'DEV-001', 'name': '설비 1', 'load_rate': 92, 'temperature': 125, 'status': 'danger', 'is_connected': True},
    {'device_id': 'DEV-002', 'name': '설비 2', 'load_rate': 92, 'temperature': 125, 'status': 'danger', 'is_connected': True},
    {'device_id': 'DEV-003', 'name': '설비 3', 'load_rate': 75, 'temperature': 110, 'status': 'caution', 'is_connected': True},
    {'device_id': 'DEV-004', 'name': '설비 4', 'load_rate': 60, 'temperature': 95, 'status': 'caution', 'is_connected': True},
    {'device_id': 'DEV-005', 'name': '설비 5', 'load_rate': 40, 'temperature': 75, 'status': 'normal', 'is_connected': True},
    {'device_id': 'DEV-006', 'name': '설비 6', 'load_rate': 35, 'temperature': 70, 'status': 'normal', 'is_connected': True},
    {'device_id': 'DEV-007', 'name': '설비 7', 'load_rate': 50, 'temperature': 80, 'status': 'normal', 'is_connected': True},
    {'device_id': 'DEV-008', 'name': '설비 8', 'load_rate': 0, 'temperature': 0, 'status': 'offline', 'is_connected': False},
]

WORKERS = [
    {'worker_id': 'W-001', 'name': '홍길동', 'department': '공정관리팀', 'position': '대리', 'email': 'hong@example.com', 'phone': '010-1234-5678', 'status': 'danger', 'is_on_site': True, 'app_connected': True, 'x_position': 42, 'y_position': 38},
    {'worker_id': 'W-002', 'name': '김철수', 'department': '공정관리팀', 'position': '과장', 'email': 'kim@example.com', 'phone': '010-2345-6789', 'status': 'caution', 'is_on_site': True, 'app_connected': True, 'x_position': 55, 'y_position': 45},
    {'worker_id': 'W-003', 'name': '이영희', 'department': '설비보전팀', 'position': '차장', 'email': 'lee@example.com', 'phone': '010-3456-7890', 'status': 'normal', 'is_on_site': True, 'app_connected': True, 'x_position': 30, 'y_position': 55},
    {'worker_id': 'W-004', 'name': '박민준', 'department': '안전팀', 'position': '사원', 'email': 'park@example.com', 'phone': '010-4567-8901', 'status': 'normal', 'is_on_site': True, 'app_connected': False, 'x_position': 70, 'y_position': 30},
    {'worker_id': 'W-005', 'name': '최수진', 'department': '공정관리팀', 'position': '부장', 'email': 'choi@example.com', 'phone': '010-5678-9012', 'status': 'normal', 'is_on_site': False, 'app_connected': False, 'x_position': 0, 'y_position': 0},
]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    now = datetime.now()
    return Response({
        'current_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'last_updated': now.strftime('%Y-%m-%d %H:%M:%S'),
        'workers': {
            'total': len(WORKERS),
            'on_site': sum(1 for w in WORKERS if w['is_on_site']),
            'danger': sum(1 for w in WORKERS if w['status'] == 'danger'),
            'caution': sum(1 for w in WORKERS if w['status'] == 'caution'),
            'normal': sum(1 for w in WORKERS if w['status'] == 'normal'),
        },
        'gas_sensors': {
            'total': len(GAS_SENSORS),
            'danger': sum(1 for s in GAS_SENSORS if s['status'] == 'danger'),
            'caution': sum(1 for s in GAS_SENSORS if s['status'] == 'caution'),
            'normal': sum(1 for s in GAS_SENSORS if s['status'] == 'normal'),
        },
        'power_devices': {
            'total': len(POWER_DEVICES),
            'total_power_mw': 1280,
            'danger': sum(1 for d in POWER_DEVICES if d['status'] == 'danger'),
            'caution': sum(1 for d in POWER_DEVICES if d['status'] == 'caution'),
        },
        'my_safety': {
            'ppe_confirmed': True,
            'checklist_completed': False,
            'vr_completed': False,
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gas_sensors_list(request):
    return Response(GAS_SENSORS)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gas_sensor_detail(request, sensor_id):
    sensor = next((s for s in GAS_SENSORS if s['sensor_id'] == sensor_id), None)
    if not sensor:
        return Response({'error': '센서를 찾을 수 없습니다.'}, status=404)
    trend_data = {
        g['gas_type']: make_trend(g['value'], g['caution_threshold'], g['danger_threshold'])
        for g in sensor.get('gases', [])
    }
    return Response({**sensor, 'trend_data': trend_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def power_devices_list(request):
    return Response(POWER_DEVICES)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def power_device_detail(request, device_id):
    device = next((d for d in POWER_DEVICES if d['device_id'] == device_id), None)
    if not device:
        return Response({'error': '설비를 찾을 수 없습니다.'}, status=404)
    return Response({**device, 'trend_data': make_trend(device['load_rate'], 70, 90)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workers_list(request):
    return Response({
        'total': len(WORKERS),
        'on_site': sum(1 for w in WORKERS if w['is_on_site']),
        'workers': WORKERS,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    worker_ids = request.data.get('worker_ids', [])
    is_all = request.data.get('is_all', False)
    return Response({
        'success': True,
        'message': f'{"전체" if is_all else len(worker_ids)}명에게 알림이 전송되었습니다.',
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def realtime_map(request):
    return Response({
        'gas_sensors': GAS_SENSORS,
        'power_devices': POWER_DEVICES,
        'workers': WORKERS,
        'danger_zones': [
            {'id': 'DZ-001', 'name': '위험구역 A', 'x': 40, 'y': 30, 'radius': 15, 'status': 'danger'},
        ]
    })


# ============ Django Template Views ============

@login_required(login_url='login')
def dashboard_template_view(request):
    """대시보드 (템플릿)"""
    dashboard_data = {
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'workers': {
            'total': len(WORKERS),
            'on_site': sum(1 for w in WORKERS if w['is_on_site']),
            'danger': sum(1 for w in WORKERS if w['status'] == 'danger'),
            'caution': sum(1 for w  in WORKERS if w['status'] == 'caution'),
            'normal': sum(1 for w in WORKERS if w['status'] == 'normal'),
        },
        'gas_sensors': {
            'total': len(GAS_SENSORS),
            'danger': sum(1 for s in GAS_SENSORS if s['status'] == 'danger'),
            'caution': sum(1 for s in GAS_SENSORS if s['status'] == 'caution'),
        },
        'power_devices': {
            'total': len(POWER_DEVICES),
            'total_power_mw': 1280,
            'danger': sum(1 for d in POWER_DEVICES if d['status'] == 'danger'),
        },
        'my_safety': {
            'ppe_confirmed': False,
            'checklist_completed': True,
            'vr_completed': False,
        },
        'gas_sensors_data': GAS_SENSORS,
        'power_devices_data': POWER_DEVICES,
    }
    return render(request, 'dashboard.html', dashboard_data)


@login_required(login_url='login')
def realtime_monitoring_template_view(request):
    """실시간 모니터링 (템플릿)"""
    data = {
        'gas_sensors': GAS_SENSORS,
        'workers': WORKERS,
        'power_devices': POWER_DEVICES,
        'danger_zones': [
            {'id': 'DZ-001', 'name': '위험구역 A', 'x': 40, 'y': 30, 'radius': 15, 'diameter': 30},
        ]
    }
    return render(request, 'realtime_monitoring.html', data)


@login_required(login_url='login')
def gas_monitoring_template_view(request):
    """유해가스 모니터링 (템플릿)"""
    data = {
        'sensors': GAS_SENSORS,
        'selected_sensor': GAS_SENSORS[0] if GAS_SENSORS else None,
    }
    return render(request, 'gas_monitoring.html', data)


@login_required(login_url='login')
def power_monitoring_template_view(request):
    """스마트 전력 모니터링 (템플릿)"""
    data = {'devices': POWER_DEVICES}
    return render(request, 'power_monitoring.html', data)


@login_required(login_url='login')
def workers_template_view(request):
    """작업자 현황 (템플릿)"""
    data = {
        'total': len(WORKERS),
        'on_site': sum(1 for w in WORKERS if w['is_on_site']),
        'workers': WORKERS,
    }
    return render(request, 'workers.html', data)

