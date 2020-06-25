from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Stack
from .forms import CreateStack, StackCommentForm, UpdateStack
from django.utils import timezone


def index(request):
    return render(request, 'myresume/index.html')
    
def main(request):
    return render(request, 'myresume/main.html')

def profile(request):
    return render(request, 'myresume/profile.html')

def stackMain(request):
    stacks = Stack.objects.all()
    return render(request, 'myresume/stackMain.html', {'stacks': stacks })


def detail(request, stack_id):
    stack = Stack.objects.all()
    stack_detail = get_object_or_404(Stack, pk=stack_id)
    comments = Comment.objects.filter(stack_id=stack_id) # filter == WHERE
    
    if request.method == 'POST':
        comment_form = StackCommentForm(request.POST) # form.py에 들어온 POST요청 인스턴스지정
        comment = Comment()

        if comment_form.is_valid():
            content = comment_form.cleaned_data['comment_textfield']  # 입력된 댓글 date 인스턴스지정
            comment.comment_textfield = content # Comment객체.댓글내용컬럼 = 댓글 data
            comment.stack_id = stack_detail.id # 해당 댓글의 외래키 = 해당 게시글 기본키
            comment.save()
            return redirect('detail', stack_id)
        else:
            return redirect('detail', stack_id)

    else:
        comment_form = StackCommentForm()
        context = {
            'stack_detail': stack_detail,
            'comments': comments,
            'stack': stack,
            'comment_form': comment_form,
        }
        return render(request, 'myresume/detail.html', context)


def createStack(request):
    if request.method == 'POST':
        form = CreateStack(request.POST)
 
        if form.is_valid():
            form.save()
            return redirect('stackMain') 
        else:
            return redirect('stackMain')
    else:
        form = CreateStack()
        return render(request, 'myresume/createStack.html', {'form': form}) 


def updateStack(request, stack_id):
    stack_detail = get_object_or_404(Stack, pk=stack_id)
    if request.method == 'POST':
        form = UpdateStack(request.POST, instance=stack_detail)
        if form.is_valid():
            udetail = form.save()
            #existing_data.delete()
            return redirect('/detail/' +str(udetail.id)) 
        else:
            return redirect('stackMain')
     
    else:
        form = UpdateStack(instance=stack_detail)
        return render(request, 'myresume/createStack.html', {'form': form})   


def deleteStack(request, stack_id):
    stack = Stack.objects.get(id=stack_id)
    stack.delete() # 삭제
    return redirect('stackMain') 