from .serializers import UserSerializer


def skb_jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "user": UserSerializer(user, context={'request': request}).data["username"]
    }
