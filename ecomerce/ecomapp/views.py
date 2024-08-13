from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import razorpay
from ecomapp.models import Order, Products,Cart
from django.db.models import Q
def index(request):
    a={}
    b=Products.objects.filter(is_active=True)
    a['products']=b#{{id:1,"name":"tshirt","price":500},{}}
    return render(request,'index.html',a)
def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)#lingesh-2items--(1*15000)+(2*1000)=150000+2000=170000
    sum=0
    for i in c:
        sum=sum+(i.qty*i.pid.price)
    a={}
    a['products']=c
    a['items']=len(c)
    a['total']=sum
    return render(request,'cart.html',a)

def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')
def user_login(request):
    a={}
    if request.method=="GET":
        return render(request,'login.html')
    else:
        u=request.POST['uname']
        p=request.POST['upass']
        if u=='' or p=='':
            a['err']="fields are empty"
            return render(request,'login.html',a)
        else:
            b=authenticate(username=u,password=p)
            print("credential",b)
            if b is not None:
                login(request,b)
                return redirect('/')
            else:
                a['err']="password and username are invalid"
                return render(request,'login.html',a)

def register(request):
    b={}
    if request.method=='POST':
        u=request.POST['uname']
        e=request.POST['uemail']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        if u=='' or e=='' or p=='' or cp=='':
            b['err']="the field are empty"
            return render(request,'register.html',b)
        elif p!=cp:
            b['err']="password didn't match"
            return render(request,'register.html',b)
        else:
            try:
                b['success']="Successfully resgister!!Please login"
                a=User.objects.create(username=u,email=e,password=p)
                a.set_password(p)
                a.save()
                return render(request,'register.html',b)
            except:
                b['err']="user already exist"
                return render(request,'register.html',b)
    else:
        return render(request,'register.html')
def user_logout(request):
    logout(request)
    return redirect('/')
def cat_filter(request,a):
    q1=Q(is_active=True)
    q2=Q(cat=a)
    p=Products.objects.filter(q1 & q2)
    b={}
    b['products']=p
    return render(request,"index.html",b)
def sort(request,a):
    if a=='0':
        col='price'
    else:
        col='-price'
    p=Products.objects.filter(is_active=True).order_by(col)
    b={}
    b['products']=p
    return render(request,'index.html',b)
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(is_active=True)
    q2=Q(price__gte=min)
    q3=Q(price__lte=max)
    p=Products.objects.filter(q1 & q2 & q3)
    b={}
    b['products']=p
    return render(request,'index.html',b)
def productsdetails(request,b):
    a={}
    p=Products.objects.filter(id=b)
    a['products']=p
    return render(request,'product_details.html',a)
def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        q1=Q(uid=userid)
        q2=Q(pid=pid)
        c=Cart.objects.filter(q1 & q2)
        p=Products.objects.filter(id=pid)
        a={}
        a['products']=p
        if c:
            a['msg']="products already exist"
            return render(request,'product_details.html',a)
        else:
            u=User.objects.filter(id=userid)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            a['success']="product added successfully"
            return render(request,'product_details.html',a)

    else:
        return redirect('/login')
def remove(request,a):
    c=Cart.objects.filter(id=a)
    c.delete()
    return redirect('/cart')
def cartqty(request,a,pid):
    userid=request.user.id
    q1=Q(uid=userid)
    q2=Q(pid=pid)
    c=Cart.objects.filter(q1 & q2)
    qty=c[0].qty
    if a== '0':
        qty=qty-1  
        c.update(qty=qty)
    else:
        qty=qty+1
        c.update(qty=qty)
    return redirect('/cart')
import random
def placeorder(request):
    if request.user.is_authenticated:
        a={}
        c=Cart.objects.filter(uid=request.user.id)
        oid=random.randrange(1000,9999)
        sum=0
        for i in c:
            o=Order.objects.create(oid=oid,pid=i.pid,uid=i.uid,qty=i.qty)
            o.save()
            i.delete()
        j=Order.objects.filter(uid=request.user.id)
        for k in j:
            sum=sum+(k.qty*k.pid.price)
        a['products']=j
        a['items']=len(j)
        a['total']=sum
        return render(request,'place_order.html',a)
    else:
        return redirect('/login')
def makepayment(request):
    userid=request.user.id
    o=Order.objects.filter(uid=userid)
    sum=0
    for i in o:
        sum=sum+(i.qty*i.pid.price)
    client = razorpay.Client(
    auth=("rzp_test_1OzOLTxIgmjE33", "Ato6PCAdn6ZM0STkEUqVLidb"))
    data = {
         "amount": sum, 
         "currency": "INR", 
         "receipt": str(o[0].oid) }
    payment = client.order.create(data=data)
    print(payment)
    a={}
    a['payment']=payment
    return render(request,"pay.html",a)
