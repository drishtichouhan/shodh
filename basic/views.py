from django.shortcuts import render
import dateutil.parser
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from basic.graph_helper import get_user, get_calendar_events
from basic.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from basic.models import User,  Student, Professor, Vacancy

profstat = False
studstat = False
myuser = {}
mycontext = {}
x = 1

def index(request):
    return render(request,'basic/index.html')

def profhome(request):

  context = initialize_context(request)
  global mycontext
  mycontext = context
  global myuser
  myuser = context.get('user')
  print(myuser)
  vacancies = Vacancy.objects.filter(prof_email = context['user']['email'])
  data = [{'name': vacancy.name,
           'department' : vacancy.department,
           'vacancyid' : vacancy.vacancyid,
           'isopen' : vacancy.isopen} for vacancy in vacancies]
  print(data)
  context.update({'data' : data})

  return render(request, 'basic/prof_home.html', context)

def home(request):
  context = initialize_context(request)
  global mycontext
  mycontext = context
  global myuser
  myuser = context.get('user')
  print(myuser)
  vacancies = Vacancy.objects.all()
  data = [{'name': vacancy.name,
           'department' : vacancy.department,
           'isopen' : vacancy.isopen,
           'vacancyid' : vacancy.vacancyid,
           'prof_name' : vacancy.prof_name,
           'prof_email' : vacancy.prof_email} for vacancy in vacancies]
  print(data)
  context.update({'data' : data})

  return render(request, 'basic/home.html', context)

def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

def sign_in_s(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  global profstat
  profstat = False
  global studstat
  studstat = True
  return HttpResponseRedirect(sign_in_url)

def sign_in_p(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  global profstat
  profstat = True
  global studstat
  studstat = False
  return HttpResponseRedirect(sign_in_url)

def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)
  print(profstat)
  print(studstat)
  print(user)
  # Save token and user
  store_token(request, token)
  store_user(request, user)

  if User.objects.filter(username = user['surname']).exists():
        print("Exists")
  else:
        new_user = User()
        new_user.is_student = studstat
        new_user.is_professor = profstat
        new_user.username = user['surname']
        new_user.first_name = user['displayName'].split(" ")[0]
        new_user.last_name = user['displayName'].split(" ")[1]
        new_user.email = user['mail'] if (user['mail'] != None) else user['userPrincipalName']
        print(new_user)
        new_user.save()
        store(new_user,studstat,profstat)



  if studstat==True:
    return HttpResponseRedirect(reverse('home'))
  else:
    return HttpResponseRedirect(reverse('profhome'))


def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('index'))

def calendar(request):
  context = initialize_context(request)

  token = get_token(request)

  events = get_calendar_events(token)

  if events:
    # Convert the ISO 8601 date times to a datetime object
    # This allows the Django template to format the value nicely
    for event in events['value']:
      event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
      event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

    context['events'] = events['value']

  return render(request, 'basic/calendar.html', context)

def store(myuser,studstat,profstat):

    if studstat == True:
        new_student = Student()
        new_student.user = myuser
        new_student.rollnumber = myuser.username

        new_student.save()

    if profstat == True:
        new_prof = Professor()
        new_prof.user = myuser
        new_prof.save()

def create_vacancy(request):
      created = False
      if request.method == "POST" :

          name = request.POST.get('name')
          department = request.POST.get('department')
          # vacancy_form = VacancyForm(data = request.POST)
          global x
          x = x + 1
          if name:
              # vacancy = vacancy_form.save()
              vacancy = Vacancy()
              vacancy.name = name
              vacancy.department = department
              print(myuser.get('name'))
              vacancy.prof_name = myuser.get('name')
              vacancy.prof_email = myuser.get('email')
              vacancy.isopen = True
              vacancy.vacancyid = x
              vacancy.save()
              created = True


          else:
              print("Enter name")
      else:
          created = False
          return render(request, 'basic/createvacancy.html')

      return HttpResponseRedirect(reverse('profhome'))

def delete_vacancy(request,id):
    print("ID is"+ str(id))
    object = Vacancy.objects.get(vacancyid=id)
    print(object)
    object.delete()
    return HttpResponseRedirect(reverse('profhome'))

    # if request.method == "POST":
    #     object = Vacancy.objects.get(vacancyid=id)
    #     object.delete()
    #     return HttpResponseRedirect(reverse('profhome'))
    # else:
    #     object = Vacancy.objects.get(vacancyid=id)
    #     object.delete()
    #     return HttpResponseRedirect(reverse('profhome'))

def toggle_vacancy(request,id):
    print("ID is"+ str(id))
    object = Vacancy.objects.get(vacancyid=id)
    print(object)

    object.isopen = not object.isopen
    object.save()
    return HttpResponseRedirect(reverse('profhome'))
