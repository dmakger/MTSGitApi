from rest_framework import status as st
from rest_framework.response import Response

COUNT_LAST_MESSAGES = 150


ERROR_PROFILE_NOT_FOUND = {
    'error': "Такого пользователя не существует",
    'status': st.HTTP_404_NOT_FOUND,
}

ERROR_CHAT_NOT_FOUND = {
    'error': "Такого чата не существует",
    'status': st.HTTP_404_NOT_FOUND,
}

ERROR_USER_NOT_FOUND = {
    'error': "У вас нет доступа к этому чату",
    'status': st.HTTP_404_NOT_FOUND,
}


def get_error(error: str, status: int):
    return Response(
        {'error': error},
        status=status,
    )
