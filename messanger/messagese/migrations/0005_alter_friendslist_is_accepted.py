# Generated by Django 5.0.3 on 2024-05-10 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagese', '0004_friendslist_profile_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendslist',
            name='is_accepted',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
