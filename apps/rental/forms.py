from django import forms

from .models import NewAdvtLocation, NewAdvtInformation, NewAdvtLastStep, AdvtReservation, NewAdvtImages

class AdCreateFormStep1(forms.ModelForm):
    class Meta:
        model=NewAdvtLocation
        fields=('country', 'region', 'city', 'street',)
        widgets = {
            'country':forms.TextInput(attrs={'class': 'form-control ','placeholder': 'Введите страну' }),
            'city':forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Введите название города'}),
            'region':forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Введите субьект РФ'}),
            'street':forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Введите улицу и номер дома'}),
            # 'street':forms.DateInput(
            #             format=('%Y-%m-%d'),
            #             attrs={'class': 'form-control', 
            #             'placeholder': 'Select a date',
            #             'type': 'date'
            # }),
        }

        labels = {
            'country': "Страна",
            'region': 'Регион',
            'city': 'Город',
            'street': 'Улица и Номер Дома',
        }

class AdCreateFormStep2(forms.ModelForm):
    class Meta:
        model=NewAdvtInformation
        fields='__all__'
        # widgets = {
        #     'country':forms.TextInput(attrs={'class': 'form-control ','placeholder': 'Введите страну' }),
        #     'city':forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Введите название города'}),
        #     'region':forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Введите субьект РФ'}),
        #     'street':forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Введите улицу и номер дома'}),
        #     # 'street':forms.DateInput(
        #     #             format=('%Y-%m-%d'),
        #     #             attrs={'class': 'form-control', 
        #     #             'placeholder': 'Select a date',
        #     #             'type': 'date'
        #     # }),
        # }

        labels = {
            'floor': "",
            'number_of_rooms': "",
            'balcony': 'Балкон',
            'loggia': 'Лоджия',
            'air_conditioner': 'Кондиционер',
            'dishwasher': 'Посудомоечная машина',
            'fridge': 'Холодильник',
            'water_heater': 'Водонагреватель',
            'stove': 'Плита',
            'tv': 'Телевизор',
            'microwave': 'Микроволновка',
            'hair_dryer': 'Фен',
            'washing_machine': 'Стиральная машина',
            'iron': 'Утюг',
            'wi_fi': 'Wi-Fi',
            'cabel_TV': 'Телевидение',
            'bed_sheets': 'Постельное белье',
            'towels': 'Полотенца',
            'hygiene_products': 'Средства гигиены',
            'max_people': '',
            'floors_at_house': '',
            'parking': '',
            'childs': '',
            'smoking': '',
            'pets': '',
            'events': '',
            'accounting_documents': '',
            'monthly_rent': '',
            'square_feet': '',


        }


class AdCreateFormStep3(forms.ModelForm):
    class Meta:
        model=NewAdvtLastStep
        fields='__all__'
        widgets = {
            'video':forms.TextInput(attrs={'class': 'form-control ','placeholder': 'Ссылка на видео' }),
            'description':forms.Textarea(attrs={'class': 'form-control ', 'placeholder': 'Расскажите, что есть в квартире и рядом с домом, опишите правила заселения и выезда. Пожалуйста, не указывайте ограничения для арендаторов. Например, по их полу или национальности.'}),
            'price':forms.NumberInput(attrs={'class': 'form-control ', 'placeholder': 'Введите цену в рублях'}),
            'deposit':forms.NumberInput(attrs={'class': 'form-control ', 'placeholder': 'Введите цену в рублях'}),
            'rep_photo':forms.FileInput(attrs={'class': 'form-control ', 'placeholder': 'Введите цену в рублях', "accept":"image/*"}),
            
        #     # 'street':forms.DateInput(
        #     #             format=('%Y-%m-%d'),
        #     #             attrs={'class': 'form-control', 
        #     #             'placeholder': 'Select a date',
        #     #             'type': 'date'
        #     # }),
        }

        labels = {
            "rep_photo": '',
            "video": '',
            "description": '',
            "price": '',
            "deposit": '',

        }

class AdCreateAdditionalImages(forms.ModelForm):
    class Meta:
        model=NewAdvtImages
        fields=('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

        labels = {
            "image": 'Дополнительные изображения',


        }
class NewReservation(forms.ModelForm):
    class Meta:
        model=AdvtReservation
        fields=('start_date', 'end_date',)

        widgets = {
            'video':forms.TextInput(attrs={'class': 'form-control ','placeholder': 'Ссылка на видео' }),
            
            'start_date':forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={'class': 'form-control', 
                        'placeholder': 'Select a date',
                        'type': 'date', 'style': 'height:50px;'
            }),
            'end_date':forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={'class': 'form-control', 
                        'placeholder': 'Select a date',
                        'type': 'date', 'style': 'height:50px;',
            }),
        }

        labels = {
            "start_date": '',
            "end_date": '',


        }