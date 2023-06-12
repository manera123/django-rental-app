
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from apps.accounts.models import User
from .models import Messages, MessageFeatures, Dialogue
from django.db.models import Q, Max, Count
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_safe, require_http_methods
from django.contrib.auth.decorators import login_required
from .crypto import encrypt
from .forms import ImageMessageForm, MessageCreateForm

from PIL import Image

# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_user_chat_logs(request):
    chat_logs_users = Messages.objects.filter(	Q(sender=request.user)|
                                                Q(receiver=request.user)
                                            ).exclude(
                                                messages=None
                                            )
    chat_logs = chat_logs_users.values('sender','receiver').annotate(
                                                        messages__id__max=Max('messages__id')
                                                    ).order_by('-messages__id__max')
    chat_logs_final = chat_logs
    for i in range(len(chat_logs)):
        sender = chat_logs[i]['sender']
        receiver = chat_logs[i]['receiver']
        for j in range(i+1,len(chat_logs)):
            if chat_logs[j]['sender'] == receiver and chat_logs[j]['receiver'] == sender:
                chat_logs_final = chat_logs_final.exclude(	sender=receiver, receiver=sender)
                break
    for i in chat_logs_final:
        sender = User.objects.get(id=i['sender'])
        if sender != request.user:
            unseen_count = Messages.objects.filter(	sender=sender,
                                                    receiver=request.user
                                            ).first().messages.filter(seen=False).count()
        else:
            unseen_count = 0
        i['unseen_count'] = unseen_count
    return chat_logs_final

@require_safe
@login_required
def index(request):
    chat_logs = get_user_chat_logs(request)

    context = {
        'chat_logs' : chat_logs,
    }
    return render(request, 'chat/index.html', context)



@require_safe
@login_required
def handle_unseen_messages(request):
	if request.is_ajax():
		id = request.GET.get('id')
		person = User.objects.get(id=id)
		m = Messages.objects.filter(sender=person, receiver=request.user).first()
		for i in m.messages.all():
			i.seen = True
			i.save()
		return JsonResponse({ 'message' : 'success' })


@require_safe
@login_required
def handle_message_liking(request):
	if request.is_ajax():
		id = request.GET.get('id')
		m = MessageFeatures.objects.get(id=id)
		m.liked = not m.liked
		m.save()
		return JsonResponse({ 'message' : 'success' })



@login_required
def view_messages(request, id):
    chat_logs = get_user_chat_logs(request)
    user = request.user
    other = User.objects.get(id=id)
    requested_chat1 = Messages.objects.filter(	sender=request.user,
                                                receiver=other
                                        ).first()

    requested_chat2 = Messages.objects.filter(	sender=other,
                                                receiver=request.user
                                            ).first()

    if requested_chat1 and requested_chat2:
        requested_chat1 = requested_chat1.messages.all().order_by('time_stamp')

        requested_chat2 = requested_chat2.messages.all().order_by('time_stamp')

        requested_chat = requested_chat1|requested_chat2
    elif requested_chat1:
        requested_chat = requested_chat1.messages.all().order_by('time_stamp')
    elif requested_chat2:
        requested_chat = requested_chat2.messages.all().order_by('time_stamp')
    else:
        requested_chat = MessageFeatures.objects.none()
    
    if request.method == 'POST':
        form = MessageCreateForm(request.POST)
        if form.is_valid():
            text = request.POST.get('text')
            print(text)
            Messages.add_message(request.user, other, text)
        
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Произошла ошибка при создании нового объявления!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = MessageCreateForm()

    context = {
        'chat_logs': chat_logs,
        'other' : other,
        'user' : user,
        'messages' : requested_chat,
        'id': id,
        'form': form,
    }
    return render(request, 'chat/chat.html', context)

@require_safe
@login_required
def view_typing_box(request):
    id = 2
    image_form = ImageMessageForm()
    return render(request, 'chat/typing_box.html', { 
                                                    'id' : id,
                                                    'image_form' : image_form, 
                                                }) 


@require_http_methods(['POST'])
@login_required
def send_message(request, id):
	if request.is_ajax():
		text = request.POST.get('text')
		if(len(text) > 63):
			inp = [text[i: i+63] for i in range(0, len(text), 63)]
			enc = ''.join([encrypt(s) for s in inp])
		else:
			enc = encrypt(text)
		person = User.objects.get(id=id)
		try:
			Messages.add_message(request.user, person, text=enc)
			response = 'Sent'
		except:
			response = 'Failed'
		return JsonResponse({'response' : response })


@require_http_methods(['POST'])
@login_required
def handle_image_messages(request, id):
	if request.is_ajax():
		image_form = ImageMessageForm(request.POST, request.FILES)
		if image_form.is_valid():
			person = User.objects.get(id=id)
			response = 'Sent'
			Messages.add_message(
						request.user, 
						person, 
						message_type='i', 
						image=image_form.cleaned_data['image']
					)
		else:
			response = 'Failed'
		return JsonResponse({'response' : response })