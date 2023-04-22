# Generated by Django 4.2 on 2023-04-22 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('company', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('stocks', models.IntegerField()),
                ('category', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('status', models.CharField(default='Active', max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]