# Generated by Django 4.1.7 on 2023-04-13 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_alter_firstlevelcategories_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firstlevelcategories',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
        ),
    ]
