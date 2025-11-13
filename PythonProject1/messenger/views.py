from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count, Case, When, IntegerField
from django.contrib.auth import login
from .models import Chat, Message, Profile
from .forms import ProfileForm, CustomUserCreationForm

@login_required
def chats(request):
    user_chats = Chat.objects.filter(participants=request.user).prefetch_related(
        'participants__profile',
        'messages'
    ).annotate(
        unread_count=Count(
            'messages',
            filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user)
        )
    ).order_by('-updated_at')

    chats_with_last_message_and_unread = []
    for chat in user_chats:
        last_message = chat.messages.last()
        other_participant = chat.participants.exclude(id=request.user.id).first()
        chats_with_last_message_and_unread.append({
            'chat': chat,
            'last_message': last_message,
            'other_participant': other_participant,
            'unread_count': chat.unread_count,
        })

    all_users = User.objects.exclude(id=request.user.id).select_related('profile')

    context = {
        'chats_with_last_message_and_unread': chats_with_last_message_and_unread,
        'all_users': all_users,
    }
    return render(request, 'messenger/chats.html', context)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    other_participant = chat.participants.exclude(id=request.user.id).first()
    chat.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)

    messages = chat.messages.all()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content
            )
            return redirect('chat_detail', chat_id=chat_id)

    context = {
        'chat': chat,
        'messages': messages,
        'other_participant': other_participant,
    }
    return render(request, 'messenger/chat_detail.html', context)

@login_required
def create_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    existing_chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()

    if existing_chat:
        return redirect('chat_detail', chat_id=existing_chat.id)

    chat = Chat.objects.create()
    chat.participants.add(request.user, other_user)

    return redirect('chat_detail', chat_id=chat.id)


def home(request):
    return render(request, 'messenger/home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chats')
    else:
        form = CustomUserCreationForm()
    return render(request, 'messenger/register.html', {'form': form})


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'messenger/profile.html', {'form': form, 'profile': profile})
