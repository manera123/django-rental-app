from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .models import User
from django.http import HttpResponseRedirect
from .forms import UserCreationForm, ProfileForm
from .utils import send_account_email_confirmation
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.rental.models import NewAdvt, UserFavoriteAdvt, AdvtReservation, DocumentsCheckRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
)
# Create your views here.


class SignupView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    redirect_authenticated_user = False

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a register page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = form.save()
        user.is_active = False
        user.save()
        send_account_email_confirmation(self.request, user)
        return valid

    def get_success_url(self):
        return '/'


@login_required
def profile_details(request):
    user = request.user
    hosted_rooms = NewAdvt.objects.filter(host_id=user.id, is_archived=False)
    hosted_rooms_acrhived = NewAdvt.objects.filter(host_id=user.id, is_archived=True)
    context = {
        "user": user,
        "rooms": hosted_rooms,
        "rooms_archived": hosted_rooms_acrhived,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_details_archived(request):
    user = request.user
    hosted_rooms = NewAdvt.objects.filter(host_id=user.id, is_archived=False)
    hosted_rooms_acrhived = NewAdvt.objects.filter(host_id=user.id, is_archived=True)
    context = {
        "user": user,
        "rooms": hosted_rooms,
        "rooms_archived": hosted_rooms_acrhived,
    }
    return render(request, 'accounts/profile_archived.html', context)

@login_required
def profile_details_user_reservations(request):
    user = request.user
    reservations = AdvtReservation.objects.filter(renter=user).order_by('time_stamp')
    context = {
        "user": user,
        "reservations": reservations,
    }
    return render(request, 'accounts/profile_reservation.html', context)

@login_required
def profile_details_user_reservations_ended(request):
    user = request.user
    reservations = AdvtReservation.objects.filter(renter=user).order_by('time_stamp')
    context = {
        "user": user,
        "reservations": reservations,
    }
    return render(request, 'accounts/profile_reservation_ended.html', context)

@login_required
def profile_reservation_requests(request):
    reservations = AdvtReservation.objects.all().order_by('time_stamp')
    context = {
        "reservations": reservations,
    }
    return render(request, 'accounts/reservation_requests/index.html', context)


@login_required
def profile_reservation_requests_progress(request):
    reservations = AdvtReservation.objects.filter(status="На рассмотрении").order_by('time_stamp')
    context = {
        "reservations": reservations,
    }
    return render(request, 'accounts/reservation_requests/reservation_requests_in_progress.html', context)

@login_required
def profile_reservation_requests_accepted(request):
    reservations = AdvtReservation.objects.filter(status="Принят").order_by('time_stamp')
    context = {
        "reservations": reservations,
    }
    return render(request, 'accounts/reservation_requests/reservation_requests_accepted.html', context)


@login_required
def profile_reservation_requests_canceled(request):
    reservations = AdvtReservation.objects.filter(status="Отклонён").order_by('time_stamp')
    context = {
        "reservations": reservations,
    }
    return render(request, 'accounts/reservation_requests/reservation_requests_canceled.html', context)

@login_required
def profile_reservation_requests_ended(request):
    reservations = AdvtReservation.objects.filter(status="Завершён").order_by('time_stamp')
    context = {
        "reservations": reservations,
    }
    return render(request, 'accounts/reservation_requests/reservation_requests_ended.html', context)

@login_required
def profile_details_favorites(request):
    user = request.user
    rooms = UserFavoriteAdvt.objects.filter(user=user)
    context = {
        "user": user,
        "rooms": rooms,

    }
    return render(request, 'accounts/profile_favorites.html', context)

@login_required
def manager_control_panel(request):
    advts = NewAdvt.objects.filter(is_documents_checked=False)
    context = {
        "advts": advts,
    }
    return render(request, 'accounts/manager_control_panel/index.html', context)

@login_required
def manager_control_panel_advts_approved(request):
    advts = NewAdvt.objects.filter(is_documents_checked=True)
    context = {
        "advts": advts,
    }
    return render(request, 'accounts/manager_control_panel/panel_advts_approved.html', context)

@login_required
def manager_control_panel_document_check_requests(request):
    requests = DocumentsCheckRequest.objects.all()
    context = {
        "requests": requests,

    }
    return render(request, 'accounts/manager_control_panel/panel_documents_check.html', context)

@login_required
def manager_control_panel_documents_approved(request):
    requests = DocumentsCheckRequest.objects.filter(is_processed=True).order_by('time_stamp')
    context = {
        "requests": requests,

    }
    return render(request, 'accounts/manager_control_panel/panel_documents_approved.html', context)

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "accounts/profile.html"

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "accounts/profile_edit.html"

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)


class PasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset/password_reset.html"
    email_template_name = 'accounts/email_messages/password_reset_email.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset/password_reset_form.html"
    success_url = reverse_lazy('accounts:password_reset_complete')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Спасибо за подтверждение Email. Теперь вы можете войти.')
        return redirect('accounts:index')
    else:
        messages.error(request, 'Срок действия ссылки истёк')
        return redirect('accounts:index')

