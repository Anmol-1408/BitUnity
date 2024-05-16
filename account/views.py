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

def login(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        if not User.objects.filter(username=loginusername).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('landing')
         
        # Authenticate the user with the provided username and password
        user = authenticate(username=loginusername, password=loginpassword)
         
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('landing')

        
            login(request, user)
        # else:
        #     messages.error(request, "Invalid credentials! Please try again")
        #     return redirect("landing")

    return render(request, 'login.html')

def signup(request):
    if request.method=="POST":
        # Get the post parameters

        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # if User.exists():
        #     # Display an information message if the username is taken
        #     messages.info(request, "Username already taken!")
        #     return redirect('')

        if (pass1!= pass2):
            messages.error(request, " Passwords do not match")
            return redirect('')

        # check for errorneous input
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('login')

    # else:
    #     return HttpResponse("404 - Not found")
    return render(request, 'signup.html')

def logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('')
