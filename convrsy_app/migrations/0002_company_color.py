# Generated by Django 4.2 on 2023-05-04 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convrsy_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='color',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
