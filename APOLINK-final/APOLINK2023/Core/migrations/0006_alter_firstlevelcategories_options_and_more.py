# Generated by Django 4.1.7 on 2023-04-20 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_alter_firstlevelcategories_short_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='firstlevelcategories',
            options={'verbose_name': 'First Level Category', 'verbose_name_plural': 'First Level Categories'},
        ),
        migrations.AlterModelOptions(
            name='secondlevelcategories',
            options={'verbose_name': 'Second Level Category', 'verbose_name_plural': 'Second Level Categories'},
        ),
    ]
