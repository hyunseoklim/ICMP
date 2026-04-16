from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workers_list(request):
    return Response({'total': 0, 'on_site': 0, 'workers': []})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    return Response({'success': True, 'message': '알림이 전송되었습니다.'})
