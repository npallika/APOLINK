# Generated by Django 4.1.7 on 2023-03-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0012_alter_productsdisplayed_for_sell_rent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent',
            field=models.CharField(blank=True, choices=[('Selling', 'For Selling'), ('Renting', 'For Renting'), ('Selling or Renting', 'For Selling or Renting')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
    ]
