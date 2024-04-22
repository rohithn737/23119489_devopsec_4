import json
import requests
from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, ThoughtForm, UpdateUserForm, UpdateProfileForm, FitnessTrackForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required 

from django.contrib import messages

from . models import Thought, Profile, FitnessTrack #Importing thought from model.py

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def homepage(request):

    return render(request, 'journal/index.html')

def register(request):

    form = CreateUserForm() #Assign your model form to a variable

    if request.method == 'POST':

        form = CreateUserForm(request.POST) #Posting the valid things i.e usrname,email,password to the form

        if form.is_valid(): #Check if the form is valid or not

            current_user = form.save(commit= False) #this will not save the file immediately to our database

            form.save()

            profile = Profile.objects.create(user = current_user) #Create a profile model and bind it to the newly created user

            #This profile we have used for uploading images to the newly created user

            messages.success(request, 'User Created!') #Setting up message based on successful user creation, messages need to be imported at the top

            return redirect('my-login') #For this redirect needs to be added at the top, redirecting back to my login page

    context = {'RegistrationForm': form} #Context dictionary

    return render(request, 'journal/register.html', context)

def my_login(request):

    form = LoginForm() #Assign your model form to a variable

    if request.method == 'POST':
    
        form = LoginForm(request, data=request.POST) #the post request is stored in the form

        if form.is_valid(): #Check if the form is valid or not

            username = request.POST.get('username') #Getting the username and password that has been entered
            password = request.POST.get('password')

            user = authenticate(request, username=username, password= password) #Matching the password and username with the stored in database creds

            if user is not None: #If user is valid in the database

                auth.login (request, user)

                return redirect('dashboard')
    
    context = {'LoginForm': form}

    return render(request, 'journal/my-login.html', context)

def user_logout(request):

    auth.logout(request)

    return redirect('') #Redirecting to our homepage

@login_required(login_url = 'my-login')
def dashboard(request):

    #Adding profile pic of logged in user in dashboard

    profile_pic = Profile.objects.get(user=request.user) #User asking request 

    context = {'profilePic': profile_pic }

    return render(request, 'journal/dashboard.html', context)

@login_required(login_url = 'my-login')
def create_tasks(request):

    form = ThoughtForm()

    if request.method == 'POST':

        form = ThoughtForm(request.POST)

        if form.is_valid(): #Check if the form is valid or not

            thought = form.save(commit = False) #Adding the form to thought variable. 
            #Commit = False as asking the django to wait till the user details are added

            thought.user = request.user #Making the post request to the person who is logged in , basically matching the correct person

            thought.save() #Now asking the database after matching the user to save it to the database

            return redirect ('my-tasks')

    context = {'CreateThoughtForm': form}

    return render(request, 'journal/create-tasks.html', context)




@login_required(login_url = 'my-login')
def my_tasks(request):

    current_user = request.user.id #request the id if the user whi is currently logged in

    thought = Thought.objects.all().filter(user=current_user) #we are trying to fetch the thought objects of the current logged in user
    #when the user is trying to click on my-thouhts button/link

    context = {'AllThoughts': thought}


    return render(request, 'journal/my-tasks.html', context)


@login_required(login_url = 'my-login')
def update_tasks(request, pk):

    #the try and except usecase is to handle the users trying to login into other users account
    try:
        
        thought = Thought.objects.get(id=pk, user=request.user) #check id with the place holder value
        #user=request.user will check the id the logged in user ---- Correct logged in user can only change the details
    
    except:

        return redirect('my-tasks')

    form = ThoughtForm(instance = thought)#Gettting the instance of the thought which has been validated above
    if request.method == 'POST':
        
        form = ThoughtForm(request.POST, instance =thought) #instance = thought

        if form.is_valid(): #Check if the form is valid or not

            form.save()

        return redirect('my-tasks')

    context = {'UpdateThought': form}

    return render(request, 'journal/update-tasks.html', context)

@login_required(login_url = 'my-login')
def delete_tasks(request, pk):

    try:
        
        thought = Thought.objects.get(id=pk, user=request.user) #check id with the place holder value
        #user=request.user will check the id the logged in user ---- Correct logged in user can only change the details
    
    except:

        return redirect('my-tasks')

    if request.method == 'POST':

        thought.delete()

        return redirect('my-tasks')


    return render(request, 'journal/delete-tasks.html')


@login_required(login_url = 'my-login')
def profile_management(request):

    form = UpdateUserForm(instance=request.user) #this -- "instance=request.user" will pre upload the existing data

    profile = Profile.objects.get(user = request.user) #To get the objects 

    
    form_2 = UpdateProfileForm(instance = profile)

    if request.method == 'POST':

        form = UpdateUserForm(request.POST, instance=request.user)

        form_2 = UpdateProfileForm(request.POST, request.FILES,instance=profile) #If someone wants to send a file , 
        #then a post request will be sent with logged user getting matched.


        if form.is_valid(): #Check if the form is valid or not

            form.save()#Then save the form to database

            return redirect('dashboard')

        if form_2.is_valid(): #Check if the form is valid or not

            form_2.save()#Then save the form to database

            return redirect('dashboard')

        
    context = {'UserUpdateForm': form, 'ProfileUpdateForm': form_2}

    return render(request, 'journal/profile-management.html', context)

@login_required(login_url = 'my-login')
def delete_account(request):

    if request.method == 'POST':

        #from django.contrib.auth.models import User -- need to import this model before proceeding further
        deleteUser = User.objects.get(username=request.user) #Checking the username before deleting the account

        deleteUser.delete()

        return redirect('')

    return render(request, 'journal/delete-account.html')



#This below section is to track the fitness of the registered users
@login_required(login_url = 'my-login')
def create_fit(request):

    form = FitnessTrackForm() #empty form

    if request.method == 'POST':

        form = FitnessTrackForm(request.POST, request.FILES)

        if form.is_valid(): #Check if the form is valid or not

            fit = form.save(commit = False) #Adding the form to thought variable. 
            #Commit = False as asking the django to wait till the user details are added

            fit.user = request.user #Making the post request to the person who is logged in , basically matching the correct person

            fit.save() #Now asking the database after matching the user to save it to the database

            return redirect ('my-fit')

    context = {'CreateFitForm': form}

    return render(request, 'journal/create-fit.html', context)


@login_required(login_url = 'my-login')
def my_fit(request):

    current_user = request.user.id #request the id if the user whi is currently logged in

    fit = FitnessTrack.objects.all().filter(user=current_user) #we are trying to fetch the thought objects of the current logged in user
    #when the user is trying to click on my-thouhts button/link

    context = {'FitThoughts': fit}


    return render(request, 'journal/my-fit.html', context)

@login_required(login_url = 'my-login')
def update_fit(request, pk):

    #the try and except usecase is to handle the users trying to login into other users account
    try:
        
        fit = FitnessTrack.objects.get(id=pk, user=request.user) #check id with the place holder value
        #user=request.user will check the id the logged in user ---- Correct logged in user can only change the details
    
    except:

        return redirect('my-fit')

    form = FitnessTrackForm(instance = fit)#Gettting the instance of the thought which has been validated above
    if request.method == 'POST':
        
        form = FitnessTrackForm(request.POST, instance =fit) #instance = thought

        if form.is_valid(): #Check if the form is valid or not

            form.save()

        return redirect('my-fit')

    context = {'UpdateFitForm': form}

    return render(request, 'journal/update-fit.html', context)

@login_required(login_url = 'my-login')
def delete_fit(request, pk):

    try:
        
        fit = FitnessTrack.objects.get(id=pk, user=request.user) #check id with the place holder value
        #user=request.user will check the id the logged in user ---- Correct logged in user can only change the details
    
    except:

        return redirect('my-fit')

    if request.method == 'POST':

        fit.delete()

        return redirect('my-fit')


    return render(request, 'journal/delete-fit.html')


from django.shortcuts import render
import requests

@csrf_protect
def call_api_view(request):
    if request.method == 'POST':
        # Get data from the form
        key1 = request.POST.get('key1')
        key2 = request.POST.get('key2')

        # Define the payload
        payload = {
            'key1': key1,
            'key2': key2
            # Add more key-value pairs as needed
        }
        print(request)
        # Make the API call
        response = requests.post('https://0zgcydxjzg.execute-api.eu-west-1.amazonaws.com/STAGE/testing', json=payload)
        print(response)
        # Process the response
        if response.status_code == 200:
            api_data = response.json()
            return render(request, 'journal/result.html', {'api_data': api_data})
        else:
            return render(request, 'journal/error.html')

    return render(request, 'journal/call-api.html')

def convert(request):
    context = {}
    
    if 'bmi_submit' in request.POST:
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        print(request.POST)

        context['bmi_result'] = bmi_converter(height, weight)
        print([context])
        
    return render(request, 'journal/bmi-converter.html', context)

def bmi_converter(height, weight):

        api_url = "https://0zgcydxjzg.execute-api.eu-west-1.amazonaws.com/STAGE/testing"

        params = {
            'height': height,
            'weight': weight,
        }

        try:
            response = requests.post(api_url, json=params)

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                error = 'API request failed with status code {}'.format(response.status_code)
                return error
        
        except Exception as e:
            error = 'Failed to connect to the API. Try Again!'

def calorie_cal(request):

    if request.method == 'POST':

        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key': 'H8nPHiu7z6YsQ3SiGVTS8w==dmJvlPZwfwKKjbYo'})
    
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exceptions as e:
            api = "Oops ! There was an error"
            print(e)
        return render(request, 'journal/calorie-cal.html', {'api':api})
    else:
        return render(request, 'journal/calorie-cal.html', {'query':'Enter a valid query'})
    
def convert_time(request):
    context = {}
    
    if 'timezone_submit' in request.POST:
        country = request.POST.get('country')
        city = request.POST.get('city')

        print(request.POST)

        context['timezone_result'] = timezone_converter(country, city)
        print([context])
        
    return render(request, 'journal/timezone-converter.html', context)
    
def timezone_converter(country, city):

        api_url = "http://www.arunangshunayak.software/api/TimeZone"

        params = {
            'country': country,
            'city': city,
        }

        try:
            response = requests.post(api_url, json=params)

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                error = 'API request failed with status code {}'.format(response.status_code)
                return error
        
        except Exception as e:
            error = 'Failed to connect to the API. Try Again!'

