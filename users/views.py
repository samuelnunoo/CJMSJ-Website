from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.http import Http404
from django.core.mail import send_mail
from DjangoWebSite import settings
from .models import Profile
from blogs.views import querying
from django.shortcuts import render, redirect,get_object_or_404
from blogs.models import Post
from .forms import ProfileForm
from django.http import JsonResponse
from .models import Account




User=get_user_model()
# Create your views here.


def activate(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and account_activation_token.check_token(user,token):

        user.is_active = True
        user.save()

        login(request,user)

        #So they can Update Their Profile
        return redirect('/users/profile/')
    else:
        return render(request, 'account/account_activation_invalid.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            try:

                user_ = form.save(commit=False)
                user_.is_active = False

                # User.objects.create(**form.cleaned_data)
                user_.save()

                current_site = get_current_site(request)

                subject = 'Activate your CJMSJ.org Account'
                message = render_to_string('account/account_activation_email.html',
                                           {
                                               'user': user_,
                                               'domain': current_site.domain,
                                               'uid': urlsafe_base64_encode(force_bytes(user_.pk)),
                                               'token': account_activation_token.make_token(user_),

                                           })
                host = settings.EMAIL_HOST_USER
                send_mail(subject, message=message, from_email=host, recipient_list=[user_.email])
                print("first one:", host, user_.email)
                return redirect('users:account_activation_sent')
            except Exception as e:
                print(e)
                return redirect('users:invalid')

        else:

            return redirect('users:invalid')

    else:
        form = SignUpForm()
        return render(request, 'account/signup.html/', {"form": form})



def email(request):

    email = request.GET.get('email')
    try:
        get_object_or_404(Account, email=email)
        data = {'Result':False}
        return JsonResponse(data)

    except:
        print("Not Found")
        data = {'Result':True}
        return JsonResponse(data)






def team(request):
    query = request.GET.get('q')
    if query:
        print(query)
        return redirect('/blogs/?q={}'.format(query))
    obj=Profile.objects.all().filter(staff=True)

    context={
        'team':obj,
    }

    return render(request, 'main/team.html', context)

def account_activation_sent(request):
    querying(request)
    return render(request, 'account/account_activation_sent.html')

def invalid(request):
    return render(request,'account/account_activation_invalid.html')

def user_status(request):
    return {'user':request.user}

def profile(request,id):
    query = request.GET.get('q')
    if query:
        print('QUERY',query)
        return redirect('/blogs/?q={}'.format(query))


    profile=get_object_or_404(Profile,id=id)
    print(profile)
    posts=Post.objects.filter(Author=profile).filter(Approved=True)

    print(profile,posts)

    if profile:
        context={
            'Author':profile,
            'Articles':posts}
        return render(request,'main/profile.html',context)
    else:
        return redirect('')

def user_profile(request):
    if request.method == 'GET':
        print('1')
        if request.user.is_authenticated:
            print('2')
            user=get_object_or_404(Profile,user=request.user)
            form=ProfileForm(initial={'first_name':user.first_name,'last_name':user.last_name,'bio':user.bio})


            context = {
                #'user':user,
                "form":form,
                'image':user.image.url,
                'name':user.name,
            }


            return render(request,'registration/user_profile.html',context)

    else:
        return redirect('/')

def update_profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = get_object_or_404(Profile, user=request.user)
            first_Name = request.POST.get('first_name')
            last_Name = request.POST.get('last_name')
            biography = request.POST.get('bio')
            print("Trying")

            try:
                Image_Data = request.FILES['Image']
                print(Image_Data)
                user.image = Image_Data
            except:
                print('no image')





            user.first_name = first_Name
            user.last_name = last_Name
            user.bio = biography
            user.complete = True
            user.save()
            return render(request, 'main/about.html', {})

        else:
            return JsonResponse({"Dummy": "ok"})








