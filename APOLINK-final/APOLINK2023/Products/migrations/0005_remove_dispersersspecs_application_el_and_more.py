# Generated by Django 4.1.7 on 2023-04-21 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_alter_productsdisplayed_for_sell_rent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispersersspecs',
            name='application_el',
        ),
        migrations.RemoveField(
            model_name='dispersersspecs',
            name='application_en',
        ),
        migrations.RemoveField(
            model_name='palletizerspecs',
            name='application_el',
        ),
        migrations.RemoveField(
            model_name='palletizerspecs',
            name='application_en',
        ),
        migrations.RemoveField(
            model_name='productsdisplayed',
            name='manufacturer_el',
        ),
        migrations.RemoveField(
            model_name='productsdisplayed',
            name='manufacturer_en',
        ),
        migrations.RemoveField(
            model_name='productsdisplayed',
            name='model_el',
        ),
        migrations.RemoveField(
            model_name='productsdisplayed',
            name='model_en',
        ),
        migrations.RemoveField(
            model_name='productsdisplayed',
            name='product_name_el',
        ),
        migrations.RemoveField(
            model_name='productsdisplayed',
            name='product_name_en',
        ),
        migrations.RemoveField(
            model_name='productsdisplayed',
            name='product_short_description_el',
        ),
        migrations.RemoveField(
            model_name='productsdisplayed',
            name='product_short_description_en',
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent',
            field=models.CharField(blank=True, choices=[('Selling', 'For Selling'), ('Selling or Renting', 'For Selling or Renting'), ('Renting', 'For Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='manufacturer'),
        ),
    ]
