import requests
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateUserSerializer

CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET


class RegisterView(APIView):
    permission_classes = [AllowAny]

    # @swagger_auto_schema(operation_description="obtain token", request_body=CreateUserSerializer)
    def post(self, request, *args, **kwargs):

        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            r = requests.post(
                f'{request.scheme}://{get_current_site(request)}/o/token/',
                # headers={'content-type': 'application/json'},
                data={
                    'grant_type': 'password',
                    'username': request.data['username'],
                    'password': request.data['password'],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
            )
            # print(r.status_code)
            return Response(r.json())
        return Response(serializer.errors)


class TokenView(APIView):
    permission_classes = [AllowAny]

    # @swagger_auto_schema(operation_description="obtain token", request_body=LoginUserSerializer)
    def post(self, request, *args, **kwargs):
        r = requests.post(
            f'{request.scheme}://{get_current_site(request)}/o/token/',
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        r = requests.post(
            f'{request.scheme}://{get_current_site(request)}/o/token/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': request.data['refresh_token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())


class RevokeTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        r = requests.post(
            f'{request.scheme}://{get_current_site(request)}/o/revoke_token/',
            data={
                'token': request.data['token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        if r.status_code == requests.codes.ok:
            return Response({'message': 'token revoked'}, r.status_code)
        # Return the error if it goes badly
        return Response(r.json(), r.status_code)
