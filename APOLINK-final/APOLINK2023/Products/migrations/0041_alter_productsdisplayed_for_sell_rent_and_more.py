# Generated by Django 4.1.7 on 2023-05-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0040_alter_contact_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent',
            field=models.CharField(blank=True, choices=[('Selling or Renting', 'For Selling or Renting'), ('Selling', 'For Selling'), ('Renting', 'For Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent_el',
            field=models.CharField(blank=True, choices=[('Selling or Renting', 'For Selling or Renting'), ('Selling', 'For Selling'), ('Renting', 'For Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent_en',
            field=models.CharField(blank=True, choices=[('Selling or Renting', 'For Selling or Renting'), ('Selling', 'For Selling'), ('Renting', 'For Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
    ]
