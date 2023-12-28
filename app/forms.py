from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок')
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание')
    blank_choice = (('N', 'Никто'),)
    categoryType = forms.ChoiceField(choices=Post.CATEGORY_CHOICES, label='Категория')

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'categoryType'
        ]


class CommentForm(forms.ModelForm):
    commentText = forms.CharField(widget=forms.Textarea, label="")

    class Meta:
        model = Comment
        fields = [
            'commentText',
        ]

