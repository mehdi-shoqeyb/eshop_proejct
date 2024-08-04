# Generated by Django 4.2.4 on 2024-07-30 00:27

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
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(max_length=32, unique=True, verbose_name='آیدی چت')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('support_user', models.ManyToManyField(limit_choices_to={'is_superuser': True}, related_name='support_users', to=settings.AUTH_USER_MODEL, verbose_name='پشتیبانی')),
                ('user', models.OneToOneField(limit_choices_to={'is_superuser': False}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('athor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_module.chatroom')),
            ],
        ),
    ]