# Generated by Django 4.0.3 on 2022-05-26 15:44

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
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drive_name', models.CharField(max_length=100)),
                ('last_date', models.DateField()),
                ('role', models.CharField(max_length=100)),
                ('req', models.CharField(max_length=400)),
                ('ctc', models.CharField(max_length=20)),
                ('passouts', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=200)),
                ('stu_applied', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SaveExcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel', models.FileField(upload_to='excel/')),
            ],
        ),
        migrations.CreateModel(
            name='PM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=30)),
                ('mobile', models.CharField(max_length=10)),
                ('department', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
