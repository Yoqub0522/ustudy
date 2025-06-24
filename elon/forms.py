from django import forms
from .models import Ad, AdImage, Message


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category', 'location', 'is_active']


class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ['ad', 'image']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'ad', 'content']
