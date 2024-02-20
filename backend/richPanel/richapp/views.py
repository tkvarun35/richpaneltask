from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpResponseNotAllowed
import json
from django.contrib.auth.models import User
from richapp.checkFunc import userExist,authenticateUser,loginUser,logoutUser,giveAdminPermission,deleteUser,is_in_24hr,custom_serializer
from richapp.response import *
from django.contrib.auth.decorators import permission_required
from .models import *
import json, requests



# Create your views here.

def signin(request):
    if(request.method=='POST'):
        data=json.load(request)
        if not authenticateUser(data,returnType="boolean"):
            return JsonResponse(INVALID_USER,status=401)
        loginUser(request,data)
        # print('logged in')
        return JsonResponse(LOGIN_RESPONSE,status=200)
    return JsonResponse(INVALID_METHOD,status=405)

def createUser(request):
    if(request.method=='POST'):
        data=json.load(request)
        if not userExist(email=data['email']):
            user = User.objects.create_user(username=data["email"], password=data['password'])
            # if(data['usertype'])=='admin':
            #     giveAdminPermission(user)
        else:
            return JsonResponse(USER_EXISTS)
        return JsonResponse(USER_CREATED)
    return JsonResponse(INVALID_METHOD)

def logout(request):
    if(request.method=='POST'):
        logoutUser(request)
        return JsonResponse(LOGGED_OUT)
    return JsonResponse(INVALID_METHOD)

@permission_required('auth.delete_permission')
def delete(request):
    if(request.method=='DELETE'):
        data=json.load(request)
        deleteUser(data)
        return JsonResponse(USER_DELETED)
    return JsonResponse(INVALID_METHOD)

def syncuser(request):
    if(request.method=='POST'):
        data=json.load(request)
        u=request.user.id
        if(request.user.is_authenticated):
            user_id=User.objects.get(id=u)
            if(appuser.objects.filter(userid=user_id).exists()):
                appuser.objects.filter(userid=user_id).update(fbuserid=data['userid'],accesstoken=data['accesstoken'])
            else:
                user=appuser.objects.create(userid=user_id,fbuserid=data['userid'],accesstoken=data['accesstoken'])
            return JsonResponse(SUCCESS,status=200)
    else:
        return JsonResponse(INVALID_METHOD,status=401)
    
def getaccess(request):
    if(request.method=='GET'):
        u=request.user.id
        if(request.user.is_authenticated):
            user_id=User.objects.get(id=u)
            if(appuser.objects.filter(userid=user_id).exists()):
                query=list(appuser.objects.filter(userid=user_id).values())[0]
                # # print()
                x = requests.get('https://graph.facebook.com/v13.0/'+query['fbuserid']+'/accounts?'+'access_token='+query['accesstoken'])
                # print(json.loads(x.text))
                return JsonResponse(json.loads(x.text),status=200,safe=False)
            else:
                JsonResponse(USER_NOT_EXIST,status=401)
    return JsonResponse(INVALID_USER,status=401)


def addpage(request):
    if(request.method=='POST'):
        data=json.load(request)
        data=json.loads(data)
        # # print(data)
        u=request.user.id
        if(request.user.is_authenticated):
            if(data['request_for']=='getData'):
                user_id=User.objects.get(id=u)
                if(page.objects.filter(userid=user_id,pageid=data['id']).exists()):
                    page.objects.filter(userid=user_id,pageid=data['id']).update(pageaccesstoken=data['access_token'],pagename=data['name'])
                else:
                    pageDetails=page.objects.create(userid=user_id,pageid=data['id'],pageaccesstoken=data['access_token'],pagename=data['name'])
                query=list(page.objects.filter(userid=user_id,pageid=data['id']).values())[0]
                # # print(query)
                getConversations(query,pageid=data['id'],pat=data['access_token'])
            elif(data['request_for']=='refreshData'):
                user_id=User.objects.get(id=u)
                if(page.objects.filter(userid=user_id,pageid=data['id']).exists()):
                    page.objects.filter(userid=user_id,pageid=data['id']).update(pageaccesstoken=data['accesstoken'],pagename=data['name'])
                else:
                    pageDetails=page.objects.create(userid=user_id,pageid=data['id'],pageaccesstoken=data['accesstoken'],pagename=data['name'])
                query=list(page.objects.filter(userid=user_id,pageid=data['id']).values())[0]
                # # print(query)
                getConversations(query,pageid=data['id'],pat=data['accesstoken'])
            return JsonResponse(SUCCESS,status=200)
    else:
        return JsonResponse(INVALID_METHOD,status=401)
    

def getConversations(pagedata,pageid,pat):
        # # print(pagedata)
        x=requests.get("https://graph.facebook.com/v19.0/"+pageid+"/conversations?platform=MESSENGER&access_token="+pat)
        x=json.loads(x.text)
        for data in x['data']:
            que1=conversations.objects.filter(pageid=pagedata['id'],conversation_id=data['id'])
            if(que1.exists()):
                    if(is_in_24hr(data['updated_time'])):
                        que1.update(updated_time=data['updated_time'])
                        getMessages(list(que1.values())[0],pagedata)
                    else:
                        print("inactivated")
                        que1.update(status="INACTIVE")
                        continue

            elif(is_in_24hr(data['updated_time'])):
                conversations.objects.create(pageid=page.objects.get(id=pagedata['id']),conversation_id=data['id'],updated_time=data['updated_time'])
                getMessages(list(conversations.objects.filter(pageid=pagedata['id'],conversation_id=data['id']).values())[0],pagedata)
            else:
                continue
                        

def getMessages(convdata,pagedata):
    # # print(convdata)
    x=requests.get("https://graph.facebook.com/v19.0/"+convdata['conversation_id']+"?fields=messages&access_token="+pagedata['pageaccesstoken'])
    x=json.loads(x.text)
    # print(x)
    for messagedata in x['messages']['data']:
        # # print(messagedata)
        # # print()
        que1=message.objects.filter(message_id=messagedata['id'],conversation=convdata['id'])
        if(is_in_24hr(messagedata['created_time'])):
            if(not que1.exists()):
                print("kk")
                print(messagedata['id'])
                print(convdata['id'])
                message.objects.update_or_create(conversation=conversations.objects.get(id=convdata['id']),message_id=messagedata['id'],created_time=messagedata['created_time'])
                    # message.objects.filter(message_id=messagedata['id'])
            getMessageDetails(list(message.objects.filter(message_id=messagedata['id']).values())[0],pagedata,x['id'])
        else:
            que1.update(status="INACTIVE")
        # print(list(message.objects.filter(message_id=messagedata['id']).values()))
        # print(is_in_24hr(messagedata['created_time']))
        

        
def getMessageDetails(messagedata,pagedata,convID):
    x=requests.get("https://graph.facebook.com/v19.0/"+messagedata['message_id']+"?fields=id,created_time,from,to,message&access_token="+pagedata['pageaccesstoken'])
    messagedetails=json.loads(x.text)
    # # print(x)
    # print(messagedata['message_id'])
    # print(messagedata['message_id'])
    print(messagedata)
    que1=message_details.objects.filter(messageid__message_id=messagedata['message_id'],userid=messagedetails['from']['id'])
    # return
    # # print(messagedetails)
    if(is_in_24hr(messagedetails['created_time'])):
        if(not que1.exists()):
            # # print('hello')
            # # print(messagedetails['from']['id'])
            # # print(list(page.objects.filter(id=pagedata['id']).values())[0]['pageid'])
            pageid=list(page.objects.filter(id=pagedata['id']).values())[0]['pageid']
            if(messagedetails['from']['id']!=pageid and not customer.objects.filter(user_id=messagedetails['from']['id']).exists()):
                customer.objects.create(username=messagedetails['from']['name'],user_id=messagedetails['from']['id'])
            if(messagedetails['from']['id']!=pageid and not que1.exists()):
                message_details.objects.create(messageid=message.objects.get(message_id=messagedata['message_id']),message_content=messagedetails['message'],created_time=messagedetails['created_time'],userid=customer.objects.get(user_id=messagedetails['from']['id']))
                
    else:
        que1.update(status='INACTIVE')
    

def getmessage(request):
    
    # return JsonResponse(list(conversations.objects.filter(pageid__pageid=239364779259215).values()),status=200,safe=False)
    if(request.method=='POST'):
        if(request.user.is_authenticated):
            pageid=json.load(request)
            conversation=conversations.objects.filter(pageid__pageid=pageid['pageid'],pageid__userid__id=request.user.id).order_by('-updated_time').exclude(status='INACTIVE').values()
            data={}
            data['conversations']=list(conversation)
            # # print(data)
            for i in data['conversations']:
                # # print(i['conversation_id'])
                i['message']=list(message_details.objects.filter(messageid__conversation__conversation_id=i['conversation_id'],status="ACTIVE").order_by('-created_time').values())[0]
                i['message']['user']=list(customer.objects.filter(user_id=i['message']['userid_id']).values())[0]
                pat=list(page.objects.filter(pageid=pageid['pageid']).values('pageaccesstoken'))[0]['pageaccesstoken']
                i['message']['user']['pat']=pat
            return JsonResponse(data,status=200,safe=False)
            # return JsonResponse(NO_DATA,status=204)
        else:
            return JsonResponse(INVALID_METHOD,status=401)
    else:
        return JsonResponse(INVALID_METHOD,status=401)
    

def getchat(request):
    if(request.method=='POST'):
        if(request.user.is_authenticated):
            chat=json.load(request)
            conversation=message_details.objects.filter(messageid__conversation__conversation_id=chat['conversation_id']).order_by('-created_time').exclude(status="INACTIVE").values('created_time','message_content')
            # data={}
            data=list(conversation)
            chatreply=replies.objects.filter(conversation__conversation_id=chat['conversation_id']).order_by('-created_time').exclude(status="INACTIVE").values('created_time','message_content','conversation')
            chatreply=list(chatreply)
            finalchat=chatreply+data
            # # print(finalchat)
            finalchat=json.loads(json.dumps(finalchat,default=custom_serializer))
            # # print(finalchat)
            for item in finalchat:
                item['created_time'] = datetime.fromisoformat(item['created_time'])
            
            sorted_data = sorted(finalchat, key=lambda x: x['created_time'], reverse=False)
            finaldata=json.loads(json.dumps(sorted_data, indent=4, default=custom_serializer))
            # print(finaldata)
            
            return JsonResponse(finaldata,status=200,safe=False)
        else:
            return JsonResponse(INVALID_METHOD,status=401)
    else:
        return JsonResponse(INVALID_METHOD,status=401)
    

def reply(request):
    if(request.method=='POST'):
        if(request.user.is_authenticated):
            chat=json.load(request)
            rec_id=list(customer.objects.filter(message_details_rel__messageid__conversation__conversation_id=chat['convID']).values())[0]
            reqdata={}
            reqdata['recipient']={}
            reqdata['recipient']['id']=rec_id['user_id']
            reqdata['messaging_type']='RESPONSE'
            reqdata['message']={}
            reqdata['message']['text']=chat['msg']
            # # print(reqdata)
            pagedata=list(page.objects.filter(conv_rel__conversation_id=chat['convID']).values())[0]
            # # print(pagedata)
            url="https://graph.facebook.com/v19.0/"+pagedata['pageid']+"/messages?access_token="+pagedata['pageaccesstoken']
            # # print(url)
            x=requests.post(url=url,json=reqdata)
            resp=json.loads(x.text)
            # # print(resp)
            reply=replies.objects.create(conversation=conversations.objects.get(conversation_id=chat['convID'],pageid__userid__id=request.user.id),message_content=chat['msg'])
            return JsonResponse(SUCCESS,status=200,safe=False)
        else:
            return JsonResponse(INVALID_METHOD,status=401)
    else:
        return JsonResponse(INVALID_METHOD,status=401)
    

def disconnect(request):
    if(request.method=='POST'):
        if(request.user.is_authenticated):
            user=request.user.id
            user=list(appuser.objects.filter(userid__id=user).values())[0]
            pat=user['accesstoken']
            fbid=user['fbuserid']
            x = requests.delete('https://graph.facebook.com/v19.0/'+fbid+'/permissions?access_token='+pat)
            resp=json.loads(x.text)
            # print(resp)
            if(resp.get('success')!=None):
                appuser.objects.filter(id=request.user.id).delete()
            else:
                return JsonResponse(NO_SUCCESS,status=422)
            return JsonResponse(resp,status=200,safe=False)
        else:
            return JsonResponse(INVALID_METHOD,status=401)
    else:
        return JsonResponse(INVALID_METHOD,status=401)
