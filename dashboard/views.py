from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Profile, User, UserRolePermissions
from core.models import Category, Video, Article
from django.db.models import Sum
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# @login_required
def dashboard(request):
    
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogin')
    
    users = User.objects.all()
    videos = Video.objects.all()
    articles = Article.objects.all()
    # all_views = Video.objects.aggregate(Sum('views'))['view_sum'] or 0
    total_users = User.objects.count()
    total_videos = Video.objects.count()
    total_articles = Article.objects.count()

    context = {
        'users': users,
        'total_users': total_users,
         'videos': videos,
         'articles': articles,
        'total_videos': total_videos,
        "total_articles":total_articles,
        # 'all_views': all_views
     }
    return render(request, "admin/dashboard.html", context)

def addVideo(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        video_file = request.FILES['video_file']
        categories = request.POST.getlist('categories')  # For multiple selected categories
        poster_image = request.FILES['poster_image']
        author_id = request.POST.get('author') 

        if author_id is None:
            # Handle case where author is not provided
            return render(request, "admin/video/add-video.html", {'error_message': 'Author is required', 'users': User.objects.all()})
        
        # Create the video object without assigning categories yet
        video = Video.objects.create(title=title, description=description, video_file=video_file, poster_image=poster_image, author_id=author_id)
        
        # Add selected categories to the video
        video.categories.add(*categories)

        return redirect('dashboard') 
    
    else:
        # Fetch all categories from the database
        categories = Category.objects.all()
        users = User.objects.all()
        return render(request, "admin/video/add-video.html", {'categories': categories,"users":users})

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'admin/video/video_detail.html', {'video': video})

def video_list(request):
    videos = Video.objects.all()
    context = {
         'videos': videos,
     }
    return render(request, "admin/video/video-list.html", context)

def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(name=category_name)
            return redirect('categorylist')
    return render(request,"admin/video/add-category.html")

def categorylist(request):
    categories=Category.objects.all()
    return render(request, "admin/video/categorylist.html",{"categories":categories})

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # Add your logic for editing the category
    return render(request, 'admin/video/edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # Add your logic for deleting the category
    category.delete()
    return redirect('categorylist')


def addArticle(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        poster_image = request.FILES['poster_image']
        categories = request.POST.getlist('categories')
        author_id = request.POST['author']

        article = Article.objects.create(
            title=title,
            description=description,
            poster_image=poster_image,
            author_id=author_id
        )
        article.categories.add(*categories)

        return redirect('article_list')
    
    else:
        categories = Category.objects.all()
        users = User.objects.all()
        return render(request, "admin/Articles/add-article.html", {'categories': categories, "users": users})

def articleList(request):
    articles=Article.objects.all()  
    return render(request, "admin/Articles/articles-list.html", {'articles': articles})

def community_list(request):
    return render(request,"admin/community/community_list.html")

def addcommunity(request):
    return render(request,"admin/community/add-community.html")

def add_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name', '')
        telephone = request.POST.get('telephone', '')
        role = request.POST.get('role')
        first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

        
        # Create a new user instance using CustomUser model and manager
        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        user.full_name = full_name
        user.telephone = telephone

        # Assign role based on the selected role in the form
        if role == 'institution_admin':
            user.is_staff = True
            user.role = 'institution_admin'
        elif role == 'system_admin':
            user.is_staff = True
            user.is_superuser = True
            user.role = 'system_admin'
        else:
            user.role = 'user'

        user.save()
        # Assign permissions based on user role
        UserRolePermissions.assign_permissions(user)

        return redirect('user_list')  # Redirect to a page displaying the list of users

    return render(request, 'admin/user/add_user.html')

def user_list(request):
    return render(request,"admin/community/community_list.html")

@login_required
def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'admin/user/view_profile.html', {'profile': profile})



def adminlogin(request):
    if request.user.is_authenticated:
        # If user is already authenticated, redirect them to another page
        return redirect('dashboard') 
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            # Redirect to a success page, or wherever you want
            return redirect('dashboard')
        else:
            # Display an error message if authentication fails
            messages.error(request, 'Invalid email or password.')
            return redirect('adminlogin')

    return render(request, "admin/auth/login.html")

def forgot_password(request):
    return render(request, 'admin/auth/forgot_password.html')