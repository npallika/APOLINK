# Generated by Django 4.1.7 on 2023-04-24 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0012_alter_productsdisplayed_for_sell_rent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent',
            field=models.CharField(blank=True, choices=[('Selling', 'For Selling'), ('Selling or Renting', 'For Selling or Renting'), ('Renting', 'For Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent_el',
            field=models.CharField(blank=True, choices=[('Selling', 'For Selling'), ('Selling or Renting', 'For Selling or Renting'), ('Renting', 'For Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent_en',
            field=models.CharField(blank=True, choices=[('Selling', 'For Selling'), ('Selling or Renting', 'For Selling or Renting'), ('Renting', 'For Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
    ]
