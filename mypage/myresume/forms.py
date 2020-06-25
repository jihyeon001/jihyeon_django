from django import forms
from .models import Stack, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CreateStack(forms.ModelForm):
    class Meta:
        model = Stack
 
        fields = ['title', 'author', 'body'] 

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '제목을 입력하세요.'}
            ),
            'author': forms.Select(
                attrs={'class': 'custom-select'},
            ),
            'body': forms.CharField(widget=CKEditorUploadingWidget()),
        }

class UpdateStack(forms.ModelForm):
    class Meta:
        model = Stack
        fields = ['title', 'author', 'body'] 

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'author': forms.Select(attrs={'class': 'custom-select'}),
            'body': forms.CharField(widget=CKEditorUploadingWidget()),
        }


class StackCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_textfield']
        widgets = {
            'comment_textfield': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40})
        }
