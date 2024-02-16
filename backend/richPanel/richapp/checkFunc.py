from django.contrib.auth.models import User,Permission
from django.contrib.auth import authenticate,login,logout
from richapp.response import *
from datetime import datetime, timedelta




def userExist(email):
    return User.objects.filter(email=email).exists()

def authenticateUser(data,returnType):
    user=authenticate(username=data['email'],password=data['password'])
    if returnType=='boolean':
        return user is not None
    if returnType=='user':
        return user
    return INVALID_RETURN_TYPE

def loginUser(request,data):
    user=authenticateUser(data,returnType="user")
    user=login(request,user)
    return user

def logoutUser(request):
    return logout(request)

def giveAdminPermission(user):
    delete_user=Permission.objects.get(codename="delete_permission")
    user.user_permissions.add(delete_user)
    user.save()

def deleteUser(data):
    user=User.objects.get(username=data['username'])
    user.delete()


def is_in_24hr(datetime_str):
    try:
        # Parse the datetime string
        input_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')
        
        # Get the current time
        current_time = datetime.now(input_datetime.tzinfo)
        
        # Calculate 24 hours from now
        last_24hr = current_time - timedelta(hours=24)
        
        # Check if the input datetime is before or after the next 24 hours
        if  last_24hr< input_datetime :
            return True
        else:
            return False
    except ValueError:
        return "Invalid datetime format"
    
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

