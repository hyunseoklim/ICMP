from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gas_sensors_list(request):
    return Response([])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gas_sensor_detail(request, sensor_id):
    return Response({'error': '센서를 찾을 수 없습니다.'}, status=404)
