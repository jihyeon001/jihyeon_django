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



def search_shop(request):
    import os
    import sys
    import urllib.request
    from urllib.request import urlopen
    import json

    # 2 : .wrap_estimation > .num 
    # 2 제조사, 브랜드 : span.inner
    # 2 브랜드 : 

    # 1 : .gpa_view .gpa 

    if request.method == 'POST':

        filepath = "myresume/config_secret/debug"
        secret_debug = json.loads(open(filepath+'.json').read()) # id와 pw는 json파일

        client_id = secret_debug['NAVER']['CLIENT_ID']
        client_secret = secret_debug['NAVER']['CLIENT_SECRET']

        insert_text = request.POST.get('q')   # 검색 폼 데이터 인스턴스 지정
        encText = urllib.parse.quote("{}".format(insert_text)) # 폼에 입력된 data를 api에 매핑
        url = "https://openapi.naver.com/v1/search/shop?query=" + encText

        naver_request = urllib.request.Request(url)
        naver_request.add_header("X-Naver-Client-Id",client_id)
        naver_request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(naver_request)
        rescode = response.getcode()
       
        if(rescode==200):
            response_body = response.read()
            dic_data = json.loads(response_body.decode('utf-8'))
            list_item = dic_data.get('items')  # items는 리스트, 히스트 요소는 딕

            items = []            
            for i in range(len(list_item)):
                item_data = list_item[i]
                if item_data['productType'] == '1' and item_data['maker'] != ''  :
                    items.append(item_data)
                else:
                    continue
            
            context = {
                'items': items
             }
            return render(request, 'myresume/search.html', context=context)
        else:
            print("Error Code:" + rescode)
    
    else:
        return render(request, 'myresume/search.html')  



    # 이미지 왼쪽, 평점 순
    # 제조사명
    # 브랜드 명
    # 제품명
    # 최저가, 평점


