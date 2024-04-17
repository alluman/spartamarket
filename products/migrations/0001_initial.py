# Generated by Django 4.2 on 2024-04-17 08:57

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
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('view', models.PositiveIntegerField(default=0)),
                ('price', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, default='static/images/user.png', upload_to='images/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('like_user', models.ManyToManyField(related_name='like_products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
