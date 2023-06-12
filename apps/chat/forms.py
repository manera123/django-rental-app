from django import forms
from .models import MessageFeatures


class ImageMessageForm(forms.Form):
	image = forms.ImageField(label='')


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model=MessageFeatures
        fields=('text',)
        widgets = {
            'text':forms.Textarea(attrs={'class': 'form-control w-100', 'style': 'max-height:350px; height:100px;' ,'placeholder': 'Введите сообщение'}),

            # 'street':forms.DateInput(
            #             format=('%Y-%m-%d'),
            #             attrs={'class': 'form-control', 
            #             'placeholder': 'Select a date',
            #             'type': 'date'
            # }),
        }

        labels = {
            'text': "",

        }