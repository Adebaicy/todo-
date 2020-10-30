# -*- coding: utf-8 -*-
'''
from django import forms

class Todof(forms.Form):
    title=forms.CharField(max_length=100)
    memo=forms.CharField(widget=forms.Textarea)
    important=forms.BooleanField(required=False)
    
    
#class Todoform():
    
    '''
from django.forms import ModelForm
from todoapp.models import Todo

# Create the form class.
class Todoform(ModelForm):
    class Meta:
        model = Todo
        fields=['title', 'memo', 'important']