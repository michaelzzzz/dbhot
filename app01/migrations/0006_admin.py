# Generated by Django 3.2.2 on 2022-10-02 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_prettynum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
            ],
        ),
    ]
