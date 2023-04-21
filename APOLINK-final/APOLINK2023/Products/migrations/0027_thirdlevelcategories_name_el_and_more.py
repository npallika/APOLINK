# Generated by Django 4.1.7 on 2023-04-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0026_alter_productsdisplayed_for_sell_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='thirdlevelcategories',
            name='name_el',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='thirdlevelcategories',
            name='name_en',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='thirdlevelcategories',
            name='short_name_el',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='thirdlevelcategories',
            name='short_name_en',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent',
            field=models.CharField(blank=True, choices=[('Renting', 'For Renting'), ('Selling', 'For Selling'), ('Selling or Renting', 'For Selling or Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
    ]