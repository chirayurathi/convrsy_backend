# Generated by Django 4.2 on 2023-05-05 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convrsy_app', '0002_company_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='color',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]