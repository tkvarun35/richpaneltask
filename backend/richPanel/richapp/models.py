from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class appuser(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    fbuserid=models.CharField(max_length=1000)
    accesstoken=models.CharField(max_length=2000)
    

    class Meta:
        db_table = "user"

class page(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    pageid=models.CharField(max_length=100)
    pageaccesstoken=models.CharField(max_length=1000)
    pagename=models.CharField(max_length=100)
    
    class Meta:
        db_table = "page"

class conversations(models.Model):
    pageid=models.ForeignKey(page,on_delete=models.CASCADE,related_name='conv_rel')
    conversation_id=models.CharField(max_length=100)
    updated_time=models.DateTimeField(null=True)
    status=models.CharField(default='ACTIVE')
    
    class Meta:
        db_table = "conversations"

class message(models.Model):
    conversation=models.ForeignKey(conversations,on_delete=models.CASCADE,related_name='messages_rel')
    message_id=models.CharField(max_length=100)
    created_time=models.DateTimeField(null=True)
    status=models.CharField(default='ACTIVE')
    
    class Meta:
        db_table = "message"

class customer(models.Model):
    username=models.CharField(max_length=100)
    user_id=models.CharField(max_length=1000,primary_key=True)

    class Meta:
        db_table = "customer"

class message_details(models.Model):
    messageid=models.ForeignKey(message,on_delete=models.CASCADE)
    message_content=models.CharField(max_length=5000)
    userid=models.ForeignKey(customer,on_delete=models.CASCADE,default="",related_name='message_details_rel')
    created_time=models.DateTimeField(null=True)
    status=models.CharField(default='ACTIVE')

    
    
    class Meta:
        db_table = "message_details"

class replies(models.Model):
    conversation=models.ForeignKey(conversations,on_delete=models.CASCADE)
    message_content=models.CharField(max_length=5000)
    created_time=models.DateTimeField(default=datetime.now, blank=True)
    status=models.CharField(default='ACTIVE')
    
    
    
    class Meta:
        db_table = "replies"




