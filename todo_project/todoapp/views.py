from django.shortcuts import render, redirect
from todo.models import Todo, Users
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.hashers import make_password  
from django.contrib.auth.hashers import check_password

def tododetails(request):
    user_id = request.session.get('userid')
    query = request.GET.get('q')
    criteria = request.GET.get('criteria')
    todo_objs = None
    
    if user_id:
        try:
            user = Users.objects.get(id=user_id)
            if query:
                if criteria == 'title':
                    todo_objs = Todo.objects.filter(user=user, title__icontains=query)
                elif criteria == 'category':
                    todo_objs = Todo.objects.filter(user=user, category__icontains=query)
                elif criteria == 'duedate':
                    todo_objs = Todo.objects.filter(user=user, duedate__icontains=query)
            else:
                todo_objs = Todo.objects.filter(user=user)
            if todo_objs:
                return render(request, "tododetails.html", {'todo_objs': todo_objs})
        except Users.DoesNotExist:
            pass  

    return render(request, "tododetails.html", {})

def register(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        existing_user_email = Users.objects.filter(email=email).first()
        
        if existing_user_email:
            messages.info(request, 'Email is already used')
            return redirect('todoapp:register')
        hashed_password = make_password(password)
        obj = Users.objects.create(
                    email=email,
                    password=hashed_password,
                    is_verified=True
        )

        messages.success(request, "User Created Successfully!")
        
        return redirect('todoapp:login')  
    return render(request,'register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = Users.objects.filter(email=email).first()     
           
        if user:
            if check_password(password, user.password):
                request.session['userid'] = user.id  
                return redirect('todoapp:index')  
            else:
                messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')


def logout_view(request):
    if 'userid' in request.session:
        request.session.pop('userid')
    return redirect('todoapp:login')

def save_todo(request):

    user_id = request.session.get('userid')
    if user_id:

        if request.method == 'POST':
            title = request.POST.get('title')
            category = request.POST.get('category')
            duedate = request.POST.get('duedate')
            description = request.POST.get('description')

            user_id = request.session.get('userid')
            if user_id:
                try:
                    todo = Todo.objects.create(
                        user_id=user_id,
                        title=title,
                        category=category,
                        duedate=duedate,
                        description=description
                    )
                    # Optionally, you can do something after creating the todo, like redirecting
                    
                    return redirect('todoapp:index')
                except Exception as e:
                    print("Error:", e)  # Handle error gracefully, maybe show an error message to the user

        return redirect('todoapp:index')



def delete_todo(request, todo_id):
    user_id = request.session.get('userid')
    if user_id:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return redirect('todoapp:index')


def edit_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)

    if request.method == 'POST':
        # Update the todo object with the new data from the form
        todo.title = request.POST.get('title', "")
        todo.category = request.POST.get('category', "")
        todo.duedate = request.POST.get('duedate', "")
        todo.description = request.POST.get('description', "")
        todo.save()
        
        return redirect('todoapp:index')  # Redirect to the todo list page after editing
    
    return render(request, 'edit_todo.html', {'todo': todo})