from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import redirect

from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout

# Create your views here.

def landing(request):
    user = request.user
    context={'user': user.username}
    return render(request, 'landing.html')

def userLogin(request):
    try:
        if request.method == "POST":
            # Get the post parameters
            loginusername = request.POST.get('loginusername')
            loginpassword = request.POST.get('loginpassword')

            if not User.objects.filter(username=loginusername).exists():
                # Display an error message if the username does not exist
                messages.error(request, 'Invalid Username')
                return redirect('landing')
            
            # Authenticate the user with the provided username and password
            user = authenticate(request, username=loginusername, password=loginpassword)
            
            if user is not None:
                # If authentication succeeds, log the user in
                login(request, user)
                return redirect('project-list')
            else:
                # Display an error message if authentication fails (invalid password)
                messages.error(request, "Invalid Password")
                return redirect('landing')
        
        # If the request method is not POST, render the login page
        return render(request, 'login.html')

    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)

def signup(request):
    try:
        if request.method == "POST":
            # Get the post parameters
            username = request.POST.get('username')
            email = request.POST.get('email')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                # Display an information message if the username is taken
                messages.info(request, "Username already taken!")
                return redirect('signup')

            # Check if passwords match
            if pass1 != pass2:
                messages.error(request, "Passwords do not match")
                return redirect('signup')

            # Create the user
            myuser = User.objects.create_user(username, email=email, password=pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            messages.success(request, "Your account has been successfully created")
            return redirect('login')
        
        # If the request method is not POST, render the signup page
        return render(request, 'signup.html')

    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)

def userLogout(request):
    try:
        # Call Django's logout function to log out the user
        logout(request)
        messages.success(request, "Successfully logged out")
        return redirect('landing')
    
    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)
