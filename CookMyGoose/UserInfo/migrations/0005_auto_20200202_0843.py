# Generated by Django 2.2.7 on 2020-02-02 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0004_auto_20200202_0216'),
    ]

    operations = [
        migrations.DeleteModel(
            name='home',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
    ]
