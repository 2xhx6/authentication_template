from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from dj_rest_auth.views import UserDetailsView


UserDetailsView.__doc__ = """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name, birth_date, gender
    Default display fields: pk, username, email, first_name, last_name, birth_date, gender
    Read-only fields: pk, email

    Returns UserModel fields.
    """


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in get_user_model().objects.all()]
        return Response(usernames)
