# Generated by Django 4.0.6 on 2022-07-21 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('DG', 'Dog'), ('CT', 'Cat'), ('OT', 'Other')], default='DG', max_length=2)),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('breed', models.CharField(max_length=100)),
                ('sex', models.CharField(choices=[('ML', 'Male'), ('FM', 'Female')], default='ML', max_length=2)),
                ('comments', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('LT', 'Lost'), ('FD', 'Found')], default='LT', max_length=2)),
            ],
        ),
    ]
