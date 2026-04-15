from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        import re
        if not re.match(r'^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError('아이디는 영문 또는 숫자만 입력할 수 있습니다.')
        if len(value) < 4 or len(value) > 20:
            raise serializers.ValidationError('아이디를 4~20자로 입력해주세요.')
        return value

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError({'non_field_errors': '아이디 또는 비밀번호가 올바르지 않습니다.'})
        if not user.is_active:
            raise serializers.ValidationError({'non_field_errors': '비활성화된 계정입니다.'})
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'department', 'position', 'phone', 'role', 'employee_id']
        read_only_fields = ['id', 'username']


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        import re
        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError('8~16자의 영문, 숫자, 특수문자를 조합하여 입력해 주세요.')
        has_alpha = bool(re.search(r'[a-zA-Z]', value))
        has_digit = bool(re.search(r'\d', value))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', value))
        if sum([has_alpha, has_digit, has_special]) < 2:
            raise serializers.ValidationError('8~16자의 영문, 숫자, 특수문자를 조합하여 입력해 주세요.')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '입력하신 신규 비밀번호와 일치하지 않습니다.'})
        return attrs
