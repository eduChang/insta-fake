from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm, ImageForm, CommentForm
from .models import Post, Comment, Hashtag
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
def list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'posts/list.html',{'posts':posts,'comment_form':comment_form})
    
@login_required    
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
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            
            # 해쉬태그 기능 추가
            content = post_form.cleaned_data.get('content')
            content_words = content.split()
            for word in content_words:
                if word[0] == "#":
                    tag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(tag[0])
            # 해쉬태그 끝
            
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

@login_required        
def update(request,id):
    post = get_object_or_404(Post, id=id)
    if post.user == request.user:
        if request.method == "POST":
            post_form = PostForm(request.POST, instance=post)
            if post_form.is_valid():
                post_form.save()
                
                post.hashtags.clear()
                content = post_form.cleaned_data.get('content')
                content_words = content.split()
                for word in content_words:
                    if word[0] == "#":
                        tag = Hashtag.objects.get_or_create(content=word)
                        post.hashtags.add(tag[0])
                
                return redirect("posts:list")
        else:
            post_form = PostForm(instance=post)
        return render(request, 'posts/form.html',{'post_form':post_form})
    else:
        return redirect('posts:list')

@login_required
def delete(request,id):
    post = Post.objects.get(id=id)
    if post.user == request.user:
        post.delete()
    return redirect("posts:list")

@login_required
@require_POST
def comment_create(request, post_id):
    # if request.method == 'POST':
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post = Post.objects.get(id=post_id)
        comment_form.save()
        return redirect("posts:list")

@login_required
def comment_delete(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
    return redirect('posts:list')
    
@login_required        
def like(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    
    # 사용자가 좋아요를 눌렀다면
    if user in post.likes.all():
        post.likes.remove(user)
        is_like = False
    # 사용자가 좋아요를 누르지 않았다면
    else:
        post.likes.add(user)
        is_like = True
    
    return JsonResponse({"is_like":is_like, "like_count":post.likes.count()})
    # return redirect('posts:list')
    # 과거의 코드
    # user = request.user
    # post = Post.objects.get(id=id)
    
    # likes = post.like_set.all()
    # check = 0
    # for like in likes:
    #     if user == like.user:
    #         check = 1
    #         like_post = like
            
    # if check == 1:
    #     like_post.delete()
    # else:
    #     like = Like(user=user, post=post)
    #     like.save()
            
    # return redirect('posts:list')
    
def hashtag(request,id):
    hashtag = Hashtag.objects.get(id=id)
    posts = hashtag.post_set.all()
    comment_form = CommentForm()
    
    return render(request, 'posts/list.html', {"posts":posts, "comment_form":comment_form, "hashtag":hashtag})
    
    
    
    
    
    
    