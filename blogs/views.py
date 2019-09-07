from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import PostForm
import json
from .models import Post
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchVector
from django.core.paginator import  Paginator,EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from users.models import Profile
from django.template.loader import render_to_string

from PIL import Image
# Create your views here.

def nl2br(string):
    return string.replace('\n','<br>')

def querying(request):
    query = request.GET.get('q')
    if query:
        print(query)
        return redirect('/blogs/?q={}'.format(query))

def simple_upload(request):
    query = request.GET.get('q')
    if query:
        print(query)
        return redirect('/blogs/?q={}'.format(query))

    if request.method=='POST' and request.FILES['myfile']:
        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        uploaded_file_url=fs.url(filename)
        return render(request, 'submissions/simple_upload.html', {
            'uploaded_file_url':uploaded_file_url
        })
    return render(request, 'submissions/base.html')

def page_view(request,id):
    query = request.GET.get('q')
    if query:
        print('QUERY',query)
        return redirect('/blogs/?q={}'.format(query))

    obj=get_object_or_404(Post,id=id)
    formatted_text="  ".join(obj.Content.split("\n"))
    print("this is printing {}".format(obj))

    if obj.Approved==True:
        context={
            'object':obj,
            'content':formatted_text}
        return render(request,'blogs/page.html',context)
    else:
        return redirect('/blogs/')

def blog_view(request):

    queryset_list=Post.objects.all().exclude(Approved=False)

    query = request.GET.get('q')
    print('I AM PRINTING',query)
    if query:
        print('I AM PRINTING', query)
        queryset_list=queryset_list.annotate(search=SearchVector('Title','Content')).filter(search=query)
    paginator_=Paginator(queryset_list,10)
    page_request_var='page'
    page=request.GET.get(page_request_var)
    print("STAGE 1")
    try:
        queryset=paginator_.page(page)
    except PageNotAnInteger:
        queryset = paginator_.page(1)
    except EmptyPage:
        queryset=paginator_.page(paginator_.num_pages)

    context={
        'blogs':queryset
    }

    return render(request,'blogs/blogs.html',context)

def form_upload(request):
    query = request.GET.get('q')
    if query:
        print(query)
        return redirect('/blogs/?q={}'.format(query))
    querying(request)






    return render(request, 'submissions/new-submissions.html', {'form':PostForm})

def main_page(request):
    query = request.GET.get('q')
    if query:
        print(query)
        return redirect('/blogs/?q={}'.format(query))



    #Variable Declaration
    Posts = Post.objects.all().filter(Approved=True).order_by('Created')[::-1]
    Featured = None
    Query = None

    print(Posts)


    #Check for Featured
    if len(Posts) > 0:
        Featured = Posts[0]




    #Check for Query
    print("Post Length: {0}".format(len(Posts)))
    if len(Posts) > 3:
        print("Greater than 3!")
        Query = Posts[1:4]

    elif len(Posts) == 0:
        print('empty')

    else:
        print("Less than 3!")
        Query = Posts[1::]


    print(Query)

    #Keys
    keys = {
        "Featured":Featured,
        "Query": Query,

    }





    return render(request, 'main/new_home.html', keys)

def about(request):
    query = request.GET.get('q')
    if query:
        print(query)
        return redirect('/blogs/?q={}'.format(query))
    querying(request)
    return render(request,'main/aboutv2.html',{})

def contact(request):
    query = request.GET.get('q')
    if query:
        print(query)
        return redirect('/blogs/?q={}'.format(query))
    return render(request,'main/contactv2.html',{})

def submit(request):

    if request.method == 'POST':
        print("SUBMIT HAS STARTED")

        if request.user.is_authenticated:
            Content=request.POST.get('Content')
            Description=request.POST.get("Description")
            Image_Data = request.FILES['Image'] #Because it's a dictionary value
            Title=request.POST.get("Title")
            Author=request.POST.get("Authors").split(',')

            #Author Selection Logic

            newAuthors = []
            for author in Author:
                for user in Profile.objects.all():
                    if str(user) == author:
                        print(user)
                        newAuthors.append(user)




            post = Post(Title=Title, Image=Image_Data, Content=Content, Description=Description)
            post.save()





            for profile in newAuthors:
                    print("New Authors",profile,profile.id)
                    post.Author.add(profile)
                    print("next")



            print(post.Author)
            print(type(Author),Author)
            print(Image_Data, type(Image_Data))


            post.save()
            return render(request, 'main/about.html', {})

        else:
            return JsonResponse({"Dummy":"ok"})




# Section Pertaining to Reviewing Articles

def authorized(request):
    if request.user.is_authenticated:
        return JsonResponse({"sign-up":False})

    else:
        return JsonResponse({"sign-up": True})

def review(request):
    if request.user.is_authenticated and request.user.is_staff:
        review_items=Post.objects.filter(Approved=False).filter(Rejected=False)

        context={
            'articles':review_items,

        }

        return render(request,'main/review.html',context)
    else:
        return HttpResponseForbidden()

def review_article(request,id):
    if request.user.is_staff:

        obj = get_object_or_404(Post, id=id)

        context={
                 'article':obj,
                 'form':PostForm(initial={"Content":obj.Content,"Description":obj.Description})
                 }



        return render(request,'review/review_blog.html',context)

    else:
        return HttpResponseForbidden()

def review_action(request):
    pass

def preview_article(request,id):
    if request.user.is_staff:
        obj = get_object_or_404(Post,id=id)

        context={
            'object':obj,

        }

        return render(request,'review/preview_blog.html',context)

    else:
        return HttpResponseForbidden()


def preview(request):
    if request.user.is_staff:
        html = render_to_string('review/preview.html')
        return HttpResponse(html)
    else:
        return HttpResponseForbidden

def edit(request):
    if request.user.is_staff:

        data = {
            'form': PostForm
        }
        html = render_to_string('review/edit.html',context = data )
        print(html)
        return HttpResponse(html)
    else:
        return HttpResponseForbidden

def approve(request):
    if request.user.is_staff:

        #Grab Variables
        Description = request.POST.get("Description")
        Content = request.POST.get("Content")
        Title = request.POST.get("Title")





        #Get Post ID
        PostID = request.POST.get('Url').split('/')[::-1][0]
        Blog = get_object_or_404(Post, id = int(PostID))

        #Set Values
        Blog.Description = Description
        Blog.Content = Content

        #Image
        try:
            Image = request.FILES['Image']
            Blog.Image = Image
        except:
            print('No Image')

        Blog.Title = Title
        Blog.Approved = True
        Blog.save()

        return HttpResponse('')

    else:
        return HttpResponseForbidden

def rejected(request):

    if request.user.is_staff:

        #PostID
        PostID = request.POST.get('Url').split('/')[::-1][0]
        Blog = get_object_or_404(Post, id=int(PostID))

        #Reject
        print(Blog,PostID)
        Blog.Rejected = True
        Blog.save()

        return HttpResponse("Completed")

    else:
        return HttpResponseForbidden

