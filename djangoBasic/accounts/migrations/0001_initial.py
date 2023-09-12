# Generated by Django 4.2.3 on 2023-09-01 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribed_to', models.ManyToManyField(related_name='subscribers', to=settings.AUTH_USER_MODEL)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(choices=[('looking_for_job', 'Szukam pracy'), ('looking_for_worker', 'Szukam pracownika')], max_length=20)),
                ('work_type', models.CharField(choices=[('Godzinowa', 'Godzinowa'), ('Zlecenie', 'Zlecenie')], max_length=20)),
                ('needed_workers', models.PositiveIntegerField(blank=True, null=True)),
                ('job_name', models.CharField(blank=True, help_text='Tylko jeśli szukasz pracowników', max_length=100, null=True)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(choices=[('PLN', 'PLN'), ('USD', 'USD'), ('EUR', 'EUR')], max_length=3)),
                ('skills', models.TextField(help_text='Umiejętności (oddzielone przecinkami)')),
                ('experiences', models.TextField(help_text='Doświadczenie (oddzielone przecinkami)')),
                ('description', models.TextField(max_length=5000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]