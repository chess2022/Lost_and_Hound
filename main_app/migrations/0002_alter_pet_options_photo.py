# Generated by Django 4.0.6 on 2022-07-21 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pet',
            options={},
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField(max_length=500)),
                ('pet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.pet')),
            ],
        ),
    ]