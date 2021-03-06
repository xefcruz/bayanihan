from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Business, Organization
import bcrypt

def index(request):
    return render(request, "index.html")

#LOGIN/REGISTER#
def register(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            user_name = request.POST['user_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['user_id'] = new_user.id
        return redirect("/dashboard")
    
def login(request):
    user_list = User.objects.filter(email = request.POST['email'])
    if len(user_list) == 0:
        messages.error(request, "INVALID CREDENTIALS")
        return redirect("/")
    logged_user = user_list[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['user_id'] = logged_user.id
        return redirect("/dashboard")
    else:
        messages.error(request, "INVALID CREDENTIALS")
        return redirect("/")
#LOGIN/REGISTER#

def dashboard(request):
    sortedbusiness = Business.objects.order_by('-id')[:5]
    sortedorganization = Organization.objects.order_by('-id')[:3]
    context = {
        "logged_in_user" : User.objects.get(id = request.session['user_id']),
        "sorted_business" : sortedbusiness,
        "sorted_organization" : sortedorganization,
        "user_ids" : User.objects.all() 
    }
    return render(request, "dashboard.html", context) 

def browse(request):
    sortedbusiness = Business.objects.order_by('business')
    sortedorganization = Organization.objects.order_by('organization')
    context = {
        "logged_in_user" : User.objects.get(id = request.session['user_id']),
        "sorted_business" : sortedbusiness,
        "sorted_organization" : sortedorganization,
    }
    return render(request, "browse.html", context) 

#START BUSINESS#

def new_bus(request):
    context = {
        "logged_in_user" : User.objects.get(id = request.session['user_id']),
    }
    return render(request, "new_bus.html", context)

def process_bus(request):
    errors = Business.objects.validate_business(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/business/new")

    creator = User.objects.get(id = request.session['user_id'])

    new_business = Business.objects.create(
        business = request.POST['business'],
        bus_type = request.POST['bus_type'],
        address = request.POST['address'],
        city = request.POST['city'],
        state = request.POST['state'],
        description = request.POST['description'],
        email = request.POST['email'],
        telephone = request.POST['telephone'],
        website = request.POST['website'],
        user = creator
    )
    
    return redirect("/dashboard") 

def business(request, bus_id):
    business = Business.objects.get(id = bus_id)
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "one_business" : business,
        "logged_in_user" : user,
    }
    return render(request, "business.html", context)

def edit_bus(request, bus_id):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "edit_bus" : Business.objects.get(id = bus_id),
        "logged_in_user" : user,
    }
    return render(request, "edit_bus.html", context)

def update_bus(request, bus_id):
    errors = Business.objects.validate_business(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/business/edit/{bus_id}")

    bus_to_update = Business.objects.get(id = bus_id)

    bus_to_update.business =  request.POST['business']
    bus_to_update.bus_type =  request.POST['bus_type']
    bus_to_update.address =  request.POST['address']
    bus_to_update.city =  request.POST['city']
    bus_to_update.state =  request.POST['state']
    bus_to_update.description =  request.POST['description']
    bus_to_update.email =  request.POST['email']
    bus_to_update.telephone =  request.POST['telephone']
    bus_to_update.website =  request.POST['website']

    bus_to_update.save()

    return redirect("/dashboard")

def delete_bus(request, bus_id):
    bus_to_delete = Business.objects.get(id = bus_id)
    bus_to_delete.delete()
    return redirect("/dashboard")

#END BUSINESS#

#START ORGANIZATION#

def new_org(request):
    context = {
        "logged_in_user" : User.objects.get(id = request.session['user_id']),
    }
    return render(request, "new_org.html", context)

def process_org(request):
    errors = Organization.objects.validate_organization(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/organization/new")

    creator = User.objects.get(id = request.session['user_id'])

    new_organization = Organization.objects.create(
        organization = request.POST['organization'],
        address = request.POST['address'],
        city = request.POST['city'],
        state = request.POST['state'],
        description = request.POST['description'],
        email = request.POST['email'],
        telephone = request.POST['telephone'],
        website = request.POST['website'],
        user = creator
    )
    return redirect("/dashboard") 

def organization(request, org_id):
    organization = Organization.objects.get(id = org_id)
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "one_organization" : organization,
        "logged_in_user" : user,
    }
    return render(request, "organization.html", context)

def edit_org(request, org_id):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "edit_org" : Organization.objects.get(id = org_id),
        "logged_in_user" : user,
    }
    return render(request, "edit_org.html", context)

def update_org(request, org_id):
    errors = Organization.objects.validate_organization(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/organization/edit/{org_id}")

    org_to_update = Organization.objects.get(id = org_id)

    org_to_update.organization =  request.POST['organization']
    org_to_update.address =  request.POST['address']
    org_to_update.city =  request.POST['city']
    org_to_update.state =  request.POST['state']
    org_to_update.description =  request.POST['description']
    org_to_update.email =  request.POST['email']
    org_to_update.telephone =  request.POST['telephone']
    org_to_update.website =  request.POST['website']

    org_to_update.save()

    return redirect("/dashboard")

def delete_org(request, org_id):
    org_to_delete = Organization.objects.get(id = org_id)
    org_to_delete.delete()
    return redirect("/dashboard")

#END ORGANIZATION#

def user(request, user_id):
    bus = Business.objects.filter(user=User.objects.get(id=user_id))
    org = Organization.objects.filter(user=User.objects.get(id=user_id))
    context = {
        "one_user" : User.objects.get(id = user_id),
        "all_bus" : bus,
        "all_org" : org,
    }
    return render(request, "user.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

#SEARCH#
# def HomePage(request):
#     return render(request, 'home_page.html')

# def SearchPage(request):
#     search = request.GET['query']
#     business = Business.objects.filter(name__icontains=search)
#     params = {
#         'products': business, 
#         'search':srh
#     }
#     return render(request, 'search page.html', params)


#END SEARCH#