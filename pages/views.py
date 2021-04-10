from django.shortcuts import render
from visits.models import Visit
from django.contrib.auth.models import User
from django_seed import Seed
from faker import Faker
import random, datetime, socket


def register(request):
    return render(request, 'registration/register.html')

# we keep track of the website visitor from the requests received from the home page
def index(request):
    # get the number the users
    users_count = User.objects.all().count()
    # get the number of the visits data rows
    resultcount = Visit.objects.all().count()
    # check if the database is already seeded
    if resultcount < 1000:
        seeder  = Seed.seeder()
        fake    = Faker()
        # prepare 1000 fake instance to be seeded
        seeder.add_entity(Visit, 1000, {
            'created_at':   lambda x: fake.date_time_between(datetime.datetime(2021, 4, 1, 0, 0, 0), datetime.datetime(2021, 4, 10, 23, 0, 0)), 
            'ip_address':   lambda x: "{}.{}.{}.{}".format(random.randint(1,255), random.randint(1,255), random.randint(1,255), random.randint(1,255)), #Generate fake ip_address
            'user':         lambda x: get_user_or_none(users_count), 
        })
        # insert the fake data into our database 
        seeder.execute()

    # get the client ip address using our helper
    client_ip = get_ip_address()

    # get the visitor last visit by ip_address and user_id/anynomous
    last_visit = Visit.objects.order_by('-created_at').filter(ip_address=client_ip, user_id=request.user.id).first()

    # get the time since the last visit in seconds
    time_since_last_visit = datetime.datetime.now().timestamp() - (last_visit.created_at.timestamp() if last_visit != None else 0)

    # check if the latest visit is more than 2 hours old
    if time_since_last_visit > 7200:
        # create an instance of the visit
        visit = Visit(ip_address = client_ip)
        # check if the visit is by a user or anonymous
        if request.user.is_authenticated:
            visit.user = request.user
        # persiste the visit
        visit.save()
    # return the response as web page (home template)
    return render(request, 'home.html')

# a helper to get the visitor ip address
def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

# if our database contain 3 users so thir method will be allow us to have 50% chance of anonymous visit and 50% chance of user visit
def get_user_or_none(user_count):
    rand_id = random.randint(1,user_count * 2)
    return User.objects.get(pk=rand_id) if rand_id <= user_count else None