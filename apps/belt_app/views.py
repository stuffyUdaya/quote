from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .models import User,Quote,Fav
from django.db.models import Count


def index(request):
    return render (request, 'belt_app/index.html')

def process(request):
    results = User.objects.userValidator(request.POST['name'],request.POST['alias'],request.POST['email'],request.POST['password'],request.POST['confpassword'],request.POST['dateofbirth'])
    if results[0]:
        for err in results[1]:
            print err
            messages.error(request,err)
    else:
        request.session ['loggedin'] = results[1].id
        return redirect('/success')
    return redirect('/')
def login(request):
        postData ={
        'email': request.POST['email'],
        'password': request.POST['password']
        }
        results = User.objects.loginValidator(postData)
        if results[0]:
            request.session['loggedin'] = results[1].id
            return redirect('/success')
        else:
            messages.error(request,results[1])
            return redirect('/')
def success(request):
    fav = Fav.objects.filter(user_id = request.session['loggedin'])
    quote_other = Quote.objects.all()
    for x in fav :
        print x.quote_id
        quote_other = quote_other.exclude(id = x.quote_id)
        print quote_other
    context = {
        'user': User.objects.get(id = request.session['loggedin']),
        # 'quote': Quote.objects.all(),
        'fav': Fav.objects.filter(user_id = request.session['loggedin']),
        'quote':quote_other
    }
    return render(request,'belt_app/success.html',context)

def addquote(request,id):
    postee_id = id
    # user = User.objects.get(id = id)
    results = Quote.objects.quoteValidator(request.POST['qname'], request.POST['message'],postee_id)
    if results[0]:
        for err in results[1]:
            print err
            messages.error(request,err)
            return redirect('/success')
    else:
        return redirect('/success')

    # context = {
    #     'add': Quote.objects.create(qname = request.POST['qname'], message = request.POST['message'], postee = user)
    # }

def fav(request,id,uid):

        favs = Fav.objects.create(user_id = uid, quote_id = id),

        return redirect('/success')
def view(request,id):
    context= {
        'view': Quote.objects.filter(postee_id = id)
    }
    return render(request,'belt_app/view.html', context)
def remove(request,id,uid):
    Fav.objects.get(user_id = uid, quote_id = id ).delete()
    return redirect('/success')
def logout(request):
    request.session.flush()
    return redirect('/')
