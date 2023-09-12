from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Card, Subscription
from .forms import CreateUserForm, CardForm
from .decorators import unauthenticated_user


def home(request):
    last_5_cards = Card.objects.order_by('-created_at')[:5].select_related('user')
    user = request.user
    for card in last_5_cards:
        card.experiences_list = card.experiences.split(',')
        card.skills_list = card.skills.split(',')
    
    if user.is_authenticated:
        subscribed_cards = Subscription.objects.filter(subscriber=user).values_list('subscribed_card', flat=True)
    else:
        subscribed_cards = []

    context = {'last_5_cards': last_5_cards, 'subscribed_cards': subscribed_cards}
    return render(request, 'accounts/dashboard.html', context)

def error_404_view(request, exception):
    # Redirect to the 'home' URL when a 404 error occurs
    return redirect('home')


def subscribe_to_card(request, card_id):
    if request.user.is_authenticated:
        card = get_object_or_404(Card, pk=card_id)
        # Sprawdź, czy użytkownik już jest subskrybentem karty
        if not Subscription.objects.filter(subscriber=request.user, subscribed_card=card).exists():
            Subscription.objects.create(subscriber=request.user, subscribed_card=card)
    
def unsubscribe_from_card(request, card_id):
    if request.user.is_authenticated:
        card = get_object_or_404(Card, pk=card_id)
        subscription = Subscription.objects.filter(subscriber=request.user, subscribed_card=card)
        if subscription.exists():
            subscription.delete()

@login_required(login_url='login')
def user_subscriptions(request):
    if request.user.is_authenticated:
        subscribed_cards = Subscription.objects.filter(subscriber=request.user).values_list('subscribed_card', flat=True)
        subscribed_cards = list(subscribed_cards)  # Konwertuj QuerySet na listę
    else:
        subscribed_cards = []

    # Przygotuj listę kart z dodanymi listami experiences_list i skills_list
    cards_with_lists = []
    for card_id in subscribed_cards:
        card = Card.objects.get(pk=card_id)
        card.experiences_list = card.experiences.split(',')
        card.skills_list = card.skills.split(',')
        cards_with_lists.append(card)

    context = {
        'subscribed_cards': cards_with_lists,
    }

    return render(request, 'accounts/user_subscriptions.html', context)

            

@login_required(login_url='login')
def profilePage(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return redirect('home')

    is_superuser = user.is_superuser
    user_cards = Card.objects.filter(user_id=pk)

    for card in user_cards:
        card.experiences_list = card.experiences.split(',')
        card.skills_list = card.skills.split(',')

    context= {'user': user, 'is_superuser': is_superuser, 'user_cards': user_cards}
    return render(request, 'accounts/profile.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html',context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created')
            return redirect("login")  # Redirect to the login page after successful registration
    else:
        form = CreateUserForm()

    context = {'form':form}
    return render(request, 'accounts/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required
def create_subscription(request):
    if request.method == 'POST':
        subscribed_to_user_id = request.POST.get('subscribed_to')
        if subscribed_to_user_id:
            subscribed_to_user = User.objects.get(pk=subscribed_to_user_id)
            Subscription.objects.create(subscriber=request.user, subscribed_to=subscribed_to_user)
            return redirect('dashboard')  # Przekieruj na stronę dashboard lub inny odpowiedni adres
    users_to_subscribe = User.objects.exclude(pk=request.user.id)
    return render(request, 'accounts/create_subscription.html', {'users_to_subscribe': users_to_subscribe})


@login_required
def create_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user  # Przypisujemy obecnie zalogowanego użytkownika
            card.save()
            form.save_m2m()  # Zapisujemy pola ManyToMany
            return redirect('home')  # Stwórz odpowiednią stronę dla udanego utworzenia karty
    else:
        form = CardForm()

    return render(request, 'accounts/create_card.html', {'form': form})

@login_required
def confirm_delete_card_page(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)

    context = {'card': card}
    return render(request, 'accounts/confirm_delete.html', context)

@login_required
def delete_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)
    card.delete()
    return redirect('home')  # Przekierowanie po usunięciu karty