# Generated by Django 3.0.2 on 2020-02-02 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='American',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Asian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='BBQnGrill',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Chinese',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Diabetic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='European',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Gluten_Free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Indian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Italian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Kosher',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Lactose_Intolerant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Mexican',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='QuicknEazy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='SlowCooker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Southern',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Thai',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Vegan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Vegetarian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='allergies',
            field=models.CharField(blank=True, default='Please insert all allergies seperated by commas!', max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default=0, editable=False, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
    ]
