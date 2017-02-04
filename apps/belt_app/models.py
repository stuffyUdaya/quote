from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re
import bcrypt

# Create your models here.
# email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex  = re.compile(r'^[a-zA-Z]*$')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def userValidator(self,name,alias,email,password,confpassword,dateofbirth):
        errors = []
        flag= False
        if not email_regex.match(email):
            errors.append("Email was invalid")
            flag = True
        if len(email)<2:
            errors.append("Email must contain more than 2 characters")
            flag = True
        if len(name)<2:
            errors.append(" Name should contain atleast two characters")
            flag = True
        if not name_regex.match(name):
            errors.append(" Name was invalid")
            flag = True
        if len(alias)<2:
            errors.append("alias should contain atleast two characters")
            flag = True

        if password!=confpassword:
            errors.append("Passwords must match")
            flag = True
        if len(password)<5:
            errors.append("Password should contain atleast five characters")
            flag = True
        if not flag:
            pwhash = bcrypt.hashpw(str(password).encode(),bcrypt.gensalt())
            if User.objects.create(name=name, alias=alias, email=email, hashedpassword=pwhash, dateofbirth=dateofbirth):
                print "Reg Success"
                user = User.objects.last()
                return(flag,user)
            else:
                print "Reg Failed"
                return(flag,errors)
        return(flag, errors)
    def loginValidator(self, postData):
        try:

                 user= User.objects.get(email=postData['email'])
                 print "user", user
                 password = postData['password'].encode()
                 hashed = user.hashedpassword.encode()
                 if bcrypt.hashpw(password, hashed) == hashed :
                     return (True, user)
                 else:
                     return(False, "Login Credentials are invalid")

        except:
                     return(False, "Login Credentials are invalid " )

class QuoteManager(models.Manager):
    def quoteValidator(self,qname,message,postee_id):
        errors = []
        flag= False

        if len(qname)<4:
            errors.append("Quoted by must contain more than 3 characters")
            flag = True
        if len(message)<11:
            errors.append(" message should contain morethan 10 characters")
            flag = True
        if not flag:
            if Quote.objects.create(qname=qname, message=message, postee_id= postee_id ):
                print "Quote Success"
                quote = Quote.objects.last()
                return(flag,quote)
            else:
                print "Reg Failed"
                return(flag,errors)
        return(flag, errors)



class User(models.Model):
    name = models.CharField(max_length= 50)
    alias = models.CharField(max_length= 50)
    email = models.CharField(max_length=100)
    hashedpassword = models.CharField(max_length= 255)
    dateofbirth = models.CharField(max_length= 50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
class Quote(models.Model):
    qname = models.CharField(max_length= 50)
    message = models.TextField(max_length = 500)
    postee = models.ForeignKey('User', models.DO_NOTHING, related_name="postee")
    objects = QuoteManager()

class Fav(models.Model):
    user =  models.ForeignKey('User', models.DO_NOTHING, related_name="user")

    quote = models.ForeignKey('Quote', models.DO_NOTHING, related_name="quote")
