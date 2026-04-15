from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)

    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception:
        pass
    return Response({'message': '로그아웃되었습니다.'})


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        return Response(UserSerializer(request.user).data)

    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    if not user.check_password(serializer.validated_data['current_password']):
        return Response(
            {'current_password': '현재 비밀번호가 일치하지 않습니다. 다시 확인해 주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if user.check_password(serializer.validated_data['new_password']):
        return Response(
            {'new_password': '현재 사용 중인 비밀번호는 신규 비밀번호로 사용할 수 없습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(serializer.validated_data['new_password'])
    user.save()
    return Response({'message': '비밀번호가 변경되었습니다.'})


# ============ Django Template Views ============

def login_template_view(request):
    """로그인 페이지 (템플릿 기반)"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, '아이디 또는 비밀번호가 일치하지 않습니다.')

    return render(request, 'login.html')


def logout_template_view(request):
    """로그아웃"""
    logout(request)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('login')


@login_required(login_url='login')
def profile_template_view(request):
    """프로필 페이지"""
    user = request.user

    if request.method == 'POST':
        # 비밀번호 변경 처리
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            messages.error(request, '현재 비밀번호가 일치하지 않습니다.')
        elif new_password != confirm_password:
            messages.error(request, '새 비밀번호가 일치하지 않습니다.')
        elif user.check_password(new_password):
            messages.error(request, '현재 사용 중인 비밀번호는 신규 비밀번호로 사용할 수 없습니다.')
        elif len(new_password) < 8:
            messages.error(request, '비밀번호는 8자 이상이어야 합니다.')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, '비밀번호가 변경되었습니다.')
            return redirect('profile')

    return render(request, 'profile.html', {'user': user})
