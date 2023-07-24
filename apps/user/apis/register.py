from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password

from ..services import register
from ..selectors import get_profile

User = get_user_model()


class RegisterApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        username = serializers.CharField(
            validators=(
                UnicodeUsernameValidator(),
                UniqueValidator(
                    queryset=User.objects.all()
                )
            ),
            max_length=150,
        )
        email = serializers.EmailField(max_length=255)
        bio = serializers.CharField(max_length=1000, required=False)
        last_name = serializers.CharField(max_length=150, required=True)
        first_name = serializers.CharField(max_length=150, required=True)

        password = serializers.CharField(
            validators=(validate_password,)
        )
        confirm_password = serializers.CharField(max_length=255)

        def validate(self, data):

            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError(
                    "Please fill password and confirm password"
                )

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError(
                    "confirm password is not equal to password"
                )
            return data

    class OutPutRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = User
            fields = ("username", "token", "date_joined")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(
        request=InputRegisterSerializer,
        responses=OutPutRegisterSerializer
    )
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                bio=serializer.validated_data.get("bio"),
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                username=serializer.validated_data.get("username"),
                last_name=serializer.validated_data.get("last_name"),
                first_name=serializer.validated_data.get("first_name"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            self.OutPutRegisterSerializer(
                user,
                context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED
        )
