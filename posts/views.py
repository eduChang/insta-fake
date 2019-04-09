from django.shortcuts import render,redirect
from .forms import PostForm, ImageForm
from .models import Post

# Create your views here.
def list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html',{'posts':posts})
    
def create(request):
    # 1. get 방식으로 데이터를 입력할 form을 요청한다.
    # 4. 사용자가 데이터를 입력해서 post방식으로 요청한다.
    # 9. 사용자가 다시 적절한 데이터를 입력해서 post방식으로 요청한다.
    if request.method == "POST":
        # 5. post방식으로 저장요청을 받고, 데이터를 받아 PostForm에 넣어서 인스턴스화 한다.
        # 10. 5번과 같음
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST,request.FILES)
        # 6. 데이터 검증을 한다.
        # 11. 6번과 같음
        if post_form.is_valid():
            # 12. 적절한 데이터가 들어온다. 데이터를 저장하고 list페이지로 리다이렉트!!
            post = post_form.save()
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(request.POST, request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            
            return redirect("posts:list")
        else:
            # 7. 적절하지 않은 데이터가 들어온다.
            pass
            
    else:
        # 2. PostForm을 인스턴스화 시켜서 form에 저장한다.
        post_form = PostForm()
        image_form = ImageForm()
    # 3. form 을 담아서 create.html을 보내준다.
    # 8. 사용자가 입력한 데이터는 form에 담아진 상태로 다시 form을 담아서 create.html을 보내준다.
    return render(request, 'posts/form.html', {'post_form':post_form,"image_form":image_form})
        
def update(request,id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect("posts:list")
    else:
        post_form = PostForm(instance=post)
    return render(request, 'posts/form.html',{'post_form':post_form})
    
def delete(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect("posts:list")
        
        
        
        
        
        
        
        
        