from django.shortcuts import render,redirect
from app_one.models import Users, Items
from django.contrib import messages
import bcrypt
from time import gmtime, strftime


# Create your views here.

def mainPage(request):
        return render(request, 'registration_login.html')

def registeration(request):
    if request.method == 'POST':
        if request.POST['check'] == 'registration':
            any_errors = Users.objects.basic_validator_registration(request.POST)
            if len(any_errors) > 0:
                for key, value in any_errors.items():
                    messages.error(request, value)
                return redirect('/registeration')
            else:
                if (int(request.POST['reg_pass']) == int(request.POST['con_ps'])):
                    the_name= request.POST['the_name']
                    username= request.POST['user_name']
                    passw= request.POST['reg_pass']
                    date_hired= request.POST['date_hired']
                    pass_hash= bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
                    new_user= Users.objects.create(name= the_name, user_name= username, password= pass_hash, hired_date= date_hired)
                    request.session['user_id']= new_user.id
                    messages.success(request, 'The user has been added successfully :)')
                    return redirect('/dashboard')
                else:
                    messages.error(request, 'The password field and confirm password field are not Identical ')
                    return redirect('/registeration')
    else:
        return render(request, 'registration_login.html')

def login(request):
    if request.method == "POST":
        if request.POST['check'] == 'login':
            any_errors = Users.objects.basic_validator_login(request.POST)
            if len(any_errors) > 0:
                for key, value in any_errors.items():
                    messages.error(request, value)
                return redirect('/login')
            else:
                user_name = request.POST["log_userName"]
                password = request.POST["login_pass"]
                try:
                    user = Users.objects.get(user_name= user_name)
                    if bcrypt.checkpw(password.encode(), user.password.encode()):
                        request.session["user_id"] = user.id
                        messages.success(request, "You are logged in!")
                        return redirect('/dashboard')
                    else:
                        messages.error(request, "User password does not match your record, try again!")
                        return redirect('/login')
                except Users.DoesNotExist:
                    messages.error(request, "User not found")
                    return redirect('/login')
    else:
        return render(request, 'registration_login.html')

def logout(request):
    request.session.clear()
    messages.success(request, "You are logged out!")
    return redirect("/")


def dashboardPage(request):
    if "user_id" not in request.session:
        messages.error(request, "Plese log_in first")
        return redirect("/")
    else:
        # Fetch items that user create
        user_logged_in= Users.objects.get(id=request.session["user_id"])
        userItems = Items.objects.filter(user=user_logged_in)
        # Fetch items that user has favirutes
        userFav= user_logged_in.fav_items.all()

        # For second table, other users' Wishlist
        otherusers= Users.objects.exclude(id=request.session["user_id"])
        otherItems= Items.objects.exclude(user= user_logged_in)
        context = {
            'user': user_logged_in,
            'user_items': userItems,
            'user_Fav': userFav,
            'other_users': otherusers,
            'other_Items': otherItems
        }

        return render(request, 'dashboard.html', context)


def add_to_list(request, product_id):
    the_item= Items.objects.get(id= product_id)
    the_user= Users.objects.get(id=request.session["user_id"])
    # Add the item to the user's fav list -> added it to manyTomany
    the_user.fav_items.add(the_item)
    the_user.save()
    request.session['product_id']= product_id
    messages.success(request, 'The item has been added successfully to WishList :)')
    return redirect('/dashboard')


def wish_items_create(request):
    if "user_id" not in request.session:
        messages.error(request, "Plese log_in first")
        return redirect("/")
    else:
        user_logged_in = Users.objects.get(id=request.session["user_id"])
        if request.method == 'POST':
            any_errors = Users.objects.basic_validator_productName(request.POST)
            if len(any_errors) > 0:
                for key, value in any_errors.items():
                    messages.error(request, value)
                return redirect('/wish_items/create')
            else:
                product_name= request.POST["product"]
                product_to_add= Items.objects.create(product_name= product_name, user= user_logged_in)
                messages.success(request, "The product has been added successfully")
                return redirect('/dashboard')
        else:
            return render(request, 'create_item.html')


def deleteItem(request, product_id):
    product_to_delete= Items.objects.get(id= product_id)
    product_to_delete.delete()
    messages.success(request, "The product has been Deleted successfully")
    return redirect('/dashboard')

def removeItem(request, product_id):
    the_item= Items.objects.get(id= product_id)
    the_user= Users.objects.get(id=request.session["user_id"])
    # remove the item from the user's fav list -> remove the connection in manyTomany
    the_user.fav_items.remove(the_item)
    messages.success(request, 'The item has been removed from WishList :)')
    return redirect('/dashboard')


def display_item_users(request, product_id):
    item= Items.objects.get(id= product_id)
    context = {
        'item': item,
        'users': item.fav_users.all()
    }
    return render(request, 'display_item.html', context)
