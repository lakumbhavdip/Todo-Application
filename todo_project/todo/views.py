from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo, Users
from todo_project.settings import EMAIL_HOST_USER
from .serializers import TodoSerializer, TodoUpdateSerializer, UserRegisterSerializer
from rest_framework.authtoken.models import Token
from utils import send_email
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserRegisterViewAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
            return Response({'status': 400, 'message':'email field is required.' }, status=status.HTTP_200_OK)
        if not password:
            return Response({'status': 400, 'message':'Password is required.'}, status=status.HTTP_200_OK)

        existing_user_email = Users.objects.filter(email=email).first()
        if existing_user_email:
            return Response({'status': 400, 'message':'Users with this email already exist.'})
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token, _ = Token.objects.get_or_create(user=user)  # Generate or retrieve the token for the user

            verification_link = f'http://127.0.0.1:8000/verify_email?email={email}&token={token}'

            try:
                subject = " Register Email Verification."
                body = f'''<html>
                <body>
                    <p>Dear {email},</p>
                    <p>Thank you for registering. Please click the following link to activate your account:</p>
                    <p><a href="{verification_link}">Verification Link</a></p>
                </body>
               </html>'''
                recipient_email = email
                send_email(subject, body, recipient_email)
            except Exception as e:
                return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            
            response_data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Registration successful',
                'user_id': user.id,
                'token': token.key,
                'email': user.email,
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_200_OK)
     
class VerifyEmailAPIView(APIView):
    def get(self, request):
        token = request.GET.get('token')  # Retrieve token from URL parameters
        email = request.GET.get('email')[:-1]  # Retrieve email from URL parameters
    
        # print("token: ", token)
        # print("email: ", email)
        
        if not token or not email:
            return Response({'status': 400, 'message': 'Token and email are required.'}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            user_obj = Users.objects.filter(email=email).first()
            user_token = Token.objects.get(user=user_obj).key

            is_verified = False

            if token == user_token:
                user_obj.is_verified = True
                is_verified = True
                user_obj.save()

            response_data = {
                'status': 200,
                'message': 'Email verification response.',
                'data': {'email_verify': is_verified}
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 500, 'message': f'Error verifying email: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
                    
        if not email:
            return Response({'status': 400, 'message': 'Email is a required field.'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'status': 400, 'message': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({'status': 404, 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(password, user.password):
            return Response({'status': 400, 'message': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_verified:
            return Response({'status': 400, 'message': 'Email is not verified.'}, status=status.HTTP_400_BAD_REQUEST)

        Token.objects.filter(user=user).delete()

        token = Token.objects.create(user=user)

        return Response({
            'status': 200,
            'message': 'Login successfully.',
            'token': token.key,
            'id': user.id,
        }, status=status.HTTP_200_OK)
        
class TodoAddAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"status": 201, "message": "Todo created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": 400, "message": "Invalid data.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class TodoUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user

        todo_id = request.data.get('id')
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            return Response({"status": 404, "message": "Todo item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoUpdateSerializer(todo, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "message": "Todo updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": 400, "message": "Invalid data.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
              
class DeleteCustomerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        
        todo_id = request.data.get('id')
      
        if not todo_id:
            return Response({'status': 400, 'message': 'todo id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            todo_obj = Todo.objects.get(id=todo_id)
            todo_obj.delete()  
            response_data = {
                'status': 200, 
                'message': 'Deleted successfully.',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response({'status': 404, 'message': 'Data not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 500, 'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TodoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user

        title = request.data.get('title', None)
        category = request.data.get('category')
        due_date = request.data.get('due_date', None)
        todos = Todo.objects.filter(user=user)

        if title:
            todos = todos.filter(title=title)
        if category:
            todos = todos.filter(category=category)
        if due_date:
            todos = todos.filter(duedate__date=due_date)

        serializer = TodoSerializer(todos, many=True)
        
        return Response(serializer.data)

