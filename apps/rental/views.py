from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from apps.accounts.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
)

from .models import *

from .forms import AdCreateFormStep1, AdCreateFormStep2, AdCreateFormStep3, NewReservation, AdCreateAdditionalImages
# Create your views here.


def index(request):
    rooms = NewAdvt.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, 'rental/index.html', context)

def ad_details(request, id):
    user = request.user
    ad = get_object_or_404(NewAdvt, id=id)
    fav = UserFavoriteAdvt.objects.filter(user=user,advt=ad)

    if request.method == 'POST':
        form = NewReservation(request.POST)
        if form.is_valid():
            reservation = AdvtReservation()
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            reservation.start_date = start_date
            reservation.end_date = end_date
            reservation.advt = ad
            reservation.renter = user
            reservation.save()
            messages.success(request, 'Запрос на заселении был отправлен!')
            return redirect('accounts:profile_reservations') 
        else:
            messages.error(request, 'Произошла ошибка при отправке запроса на заселение!')
            return redirect('rental:advt', ad.id)
    else:
        form = NewReservation() 
        
    context = {
        "ad": ad,
        "user": user,
        "fav": fav,
        "form": form,
    }
    return render(request, 'rental/room_details.html', context)

@login_required
def advt_reservation_cancel(request, id):
    reservation = AdvtReservation.objects.get(id=id)
    reservation.status = "Отменён"
    reservation.save()
    messages.success(request, 'Запрос был успешно отменен!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def advt_reservation_cancel_by_host(request, id):
    reservation = AdvtReservation.objects.get(id=id)
    reservation.status = "Отклонён"
    reservation.save()
    messages.success(request, 'Запрос был успешно отклонён!')
    return redirect('accounts:profile_reservation_requests_canceled') 

@login_required
def advt_reservation_accept(request, id):
    reservation = AdvtReservation.objects.get(id=id)
    reservation.status = "Принят"
    reservation.save()
    messages.success(request, 'Запрос был успешно принят!')
    return redirect('accounts:profile_reservation_requests_accepted') 

@login_required
def send_documents_for_check(request):
    user = request.user
    check = DocumentsCheckRequest()
    check.requester = user
    check.save()
    messages.success(request, 'Был отправлен запрос на подтверждение личности, с вами свяжется наш менеджер')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

@login_required
def approved_documents(request, id):
    user = User.objects.get(id=id)
    user.approved = True
    user.save()
    check = DocumentsCheckRequest.objects.get(requester=user)
    check.is_processed = True
    check.save()
    messages.success(request, 'Личность была успешна подтверждена')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

@login_required
def approved_advt(request, id):
    advt = NewAdvt.objects.get(id=id)
    advt.is_documents_checked = True
    advt.save()
    messages.success(request, 'Объявление было проверено, теперь оно видно всем!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

@login_required
def advt_reservation_end(request, id):
    reservation = AdvtReservation.objects.get(id=id)
    reservation.status = "Завершён"
    reservation.save()
    messages.success(request, 'Сделка была успешно завершена!')
    return redirect('accounts:profile_reservation_requests_ended') 

@login_required
def advt_add_step_1(request):
    
    if request.method == 'POST':
        form = AdCreateFormStep1(request.POST)
        if form.is_valid():
            new_advt = NewAdvt()
            new_advt.host = request.user
            new_advt.save()
            new_advt_location = NewAdvtLocation()

            country = request.POST.get('country')
            region = request.POST.get('region')
            city = request.POST.get('city')
            street = request.POST.get('street')

            new_advt_location.advt = new_advt
            new_advt_location.country = country
            new_advt_location.region = region
            new_advt_location.city = city
            new_advt_location.street = street
            new_advt_location.save()
            messages.success(request, 'Операция выполнена успешно!')
            return redirect('rental:advt_add_step_2', new_advt.id) 
        else:
            messages.error(request, 'Произошла ошибка при выполнении операции!')
            return redirect('rental:advt_add_step_1') 
    else:
        form = AdCreateFormStep1()
    context = {
        "form": form,
    }
    return render(request, 'rental/advt/advt_add_step_1.html', context)


@login_required
def advt_add_step_2(request, id):
    try:
        new_advt = NewAdvt.objects.get(id=id)
        if request.method == 'POST':
            form = AdCreateFormStep2(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Операция выполнена успешно!')
                    return redirect('rental:advt_add_step_3', new_advt.id) 
                except Exception as e:
                    return HttpResponse(f'Error: {str(e)}')
            else:
                messages.error(request, 'Произошла ошибка при выполнении операции!')
                return redirect('rental:advt_add_step_2', new_advt.id) 
        else:
            form = AdCreateFormStep2()

        context = {
            "new_advt": new_advt,
            "form": form,
        }

        return render(request, 'rental/advt/advt_add_step_2.html', context)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
    
@login_required
def advt_add_step_3(request, id):
    new_advt = NewAdvt.objects.get(id=id)
    if request.method == 'POST':
        form = AdCreateFormStep3(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                new_advt.is_completed = True
                messages.success(request, 'Объявление было успешно создано, ожидайте проверки модератором!')
                return redirect('accounts:profile') 
            except Exception as e:
                return HttpResponse(f'Error: {str(e)}')
        else:
            messages.error(request, 'Произошла ошибка при создании нового объявления!')
            return redirect('rental:advt_add_step_3', new_advt.id) 
    else:
        form = AdCreateFormStep3()

    context = {
        "new_advt": new_advt,
        "form": form,
    }

    return render(request, 'rental/advt/advt_add_step_3.html', context)


@login_required
def advt_edit_step_1(request, id):
    try:
        new_advt = NewAdvt.objects.get(id=id)
        if request.method == 'POST':
            form = AdCreateFormStep1(request.POST, instance=new_advt.new_advt_location.first())
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Информация обновлена!')
                    return redirect('rental:advt_edit_step_1', new_advt.id) 
                except Exception as e:
                    return HttpResponse(f'Error: {str(e)}')
            else:
                messages.error(request, 'Произошла ошибка при обновлении информации!')
                return redirect('rental:advt_edit_step_1', new_advt.id) 
        else:
            form = AdCreateFormStep1(instance=new_advt.new_advt_location.first())

        context = {
            "new_advt": new_advt,
            "form": form,
        }

        return render(request, 'rental/advt/advt_edit_step_1.html', context)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
    

@login_required
def advt_edit_step_2(request, id):
    try:
        new_advt = NewAdvt.objects.get(id=id)
        if request.method == 'POST':
            form = AdCreateFormStep2(request.POST, instance=new_advt.new_advt_information.first())
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Информация обновлена!')
                    return redirect('rental:advt_edit_step_2', new_advt.id) 
                except Exception as e:
                    return HttpResponse(f'Error: {str(e)}')
            else:
                messages.error(request, 'Произошла ошибка при обновлении информации!')
                return redirect('rental:advt_edit_step_2', new_advt.id) 
        else:
            form = AdCreateFormStep2(instance=new_advt.new_advt_information.first())

        context = {
            "new_advt": new_advt,
            "form": form,
        }

        return render(request, 'rental/advt/advt_edit_step_2.html', context)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
    

@login_required
def advt_edit_step_3(request, id):
    try:
        new_advt = NewAdvt.objects.get(id=id)
        if request.method == 'POST':
            form = AdCreateFormStep3(request.POST, request.FILES, instance=new_advt.new_advt_last_step.first())
            if form.is_valid():
                try:
                    form.save()
                    new_advt.is_completed = True
                    messages.success(request, 'Информация обновлена!')
                    return redirect('accounts:profile') 
                except Exception as e:
                    return HttpResponse(f'Error: {str(e)}')
            else:
                messages.error(request, 'Произошла ошибка при обновлении информации!')
                return redirect('rental:advt_edit_step_3', new_advt.id) 
        else:
            form = AdCreateFormStep3(instance=new_advt.new_advt_last_step.first())
        context = {
            "new_advt": new_advt,
            "form": form,
        }

        return render(request, 'rental/advt/advt_edit_step_3.html', context)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
    

@login_required
def advt_add_images(request, id):
    try:
        new_advt = NewAdvt.objects.get(id=id)
        if request.method == 'POST':
            form = AdCreateAdditionalImages(request.POST, request.FILES)
            if form.is_valid():
                try:
                    if request.FILES:
                        for f in request.FILES.getlist('image'):
                           NewAdvtImages.objects.create(advt=new_advt,image=f)
                    messages.success(request, 'Изображения были добавлены!')
                    return redirect('accounts:profile') 
                except Exception as e:
                    return HttpResponse(f'Error: {str(e)}')
            else:
                messages.error(request, 'Произошла ошибка при обновлении информации!')
                return redirect('rental:advt_add_images', new_advt.id) 
        else:
            form = AdCreateAdditionalImages()

        context = {
            "new_advt": new_advt,
            "form": form,
        }

        return render(request, 'rental/advt/advt_add_images.html', context)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
    

@login_required
def advt_to_or_from_archive(request, id):
    try:
        new_advt = NewAdvt.objects.get(id=id)
        if new_advt.is_archived:
            new_advt.is_archived = False
            new_advt.save()
            messages.success(request, 'Теперь объявление видно всем')
        else:
            new_advt.is_archived = True
            new_advt.save()
            messages.success(request, 'Объявление скрыто')
        return redirect('accounts:profile')
    except:
        messages.error(request, 'Произошла ошибка при выполнении операции')
        return redirect('accounts:profile')
    

@login_required
def advt_to_favorite(request, id):
    try:
        advt = NewAdvt.objects.get(id=id)
        user = request.user
        obj = UserFavoriteAdvt(user=user, advt=advt)
        obj.save()
        messages.success(request, 'Обьявление добавлено в избранное')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.error(request, 'Произошла ошибка при выполнении операции')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required
def advt_from_favorite(request, id):
    try:
        advt = NewAdvt.objects.get(id=id)
        user = request.user
        obj = UserFavoriteAdvt.objects.filter(user=user, advt=advt)
        obj.delete()
        messages.success(request, 'Обьявление убрано из избранного')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.error(request, 'Произошла ошибка при выполнении операции')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

@login_required
def advt_delete(request, id):
    try:
        advt = NewAdvt.objects.get(id=id)
        advt.delete()
        messages.success(request, 'Обьявление было успешно удалено')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.error(request, 'Произошла ошибка при выполнении операции')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))