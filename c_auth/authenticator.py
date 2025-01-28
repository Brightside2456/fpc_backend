from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)
        cookie_token = request.COOKIES.get('access_token')
        if not cookie_token:
            return None
        validated_token = self.get_validated_token(raw_token=cookie_token)
        return self.get_user(validated_token=validated_token), validated_token
