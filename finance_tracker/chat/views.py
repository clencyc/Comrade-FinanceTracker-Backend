from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .services import get_chatbot_response


class ChatbotView(APIView):
    def post(self, request):
        user_input = request.data.get('message')
        if not user_input:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response = get_chatbot_response(user_input)
        return Response({"response": response}, status=status.HTTP_200_OK)