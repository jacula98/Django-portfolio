from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name='subscribed_cards', blank=True)

    WORK_TYPE_CHOICES = (
        ('Godzinowa', 'Godzinowa'),
        ('Zlecenie', 'Zlecenie'),
    )
    
    CARD_TYPE_CHOICES = (
        ('looking_for_job', 'Szukam pracy'),
        ('looking_for_worker', 'Szukam pracownika'),
    )

    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    work_type = models.CharField(max_length=20, choices=WORK_TYPE_CHOICES)
    needed_workers = models.PositiveIntegerField(null=True, blank=True)

    CURRENCY_CHOICES = (
        ('PLN', 'PLN'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        # Dodaj więcej opcji walut
    )
    job_name = models.CharField(max_length=100, blank=True, null=True, help_text="Tylko jeśli szukasz pracowników")
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    skills = models.TextField(help_text="Umiejętności (oddzielone przecinkami)")
    experiences = models.TextField(help_text="Doświadczenie (oddzielone przecinkami)")
    description = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Card - {self.id}"

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed_card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subscriber.username} subscribed to {self.subscribed_card.user.username}'s Card"


