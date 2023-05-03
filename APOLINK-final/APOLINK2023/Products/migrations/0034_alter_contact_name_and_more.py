# Generated by Django 4.1.7 on 2023-04-28 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0033_alter_contact_options_contact_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent',
            field=models.CharField(blank=True, choices=[('Renting', 'For Renting'), ('Selling or Renting', 'For Selling or Renting'), ('Selling', 'For Selling')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent_el',
            field=models.CharField(blank=True, choices=[('Renting', 'For Renting'), ('Selling or Renting', 'For Selling or Renting'), ('Selling', 'For Selling')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent_en',
            field=models.CharField(blank=True, choices=[('Renting', 'For Renting'), ('Selling or Renting', 'For Selling or Renting'), ('Selling', 'For Selling')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
    ]