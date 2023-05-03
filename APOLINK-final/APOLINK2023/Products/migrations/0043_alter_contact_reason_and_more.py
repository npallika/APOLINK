# Generated by Django 4.1.7 on 2023-05-03 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0042_alter_contact_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='reason',
            field=models.CharField(blank=True, choices=[('Reason3', 'Reason3'), ('Reason2', 'Reason2'), ('Reason1', 'Reason1')], max_length=40, null=True, verbose_name='Reason for your inquiry'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent',
            field=models.CharField(blank=True, choices=[('Selling or Renting', 'For Selling or Renting'), ('Renting', 'For Renting'), ('Selling', 'For Selling')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent_el',
            field=models.CharField(blank=True, choices=[('Selling or Renting', 'For Selling or Renting'), ('Renting', 'For Renting'), ('Selling', 'For Selling')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
        migrations.AlterField(
            model_name='productsdisplayed',
            name='for_sell_rent_en',
            field=models.CharField(blank=True, choices=[('Selling or Renting', 'For Selling or Renting'), ('Renting', 'For Renting'), ('Selling', 'For Selling')], max_length=40, null=True, verbose_name='For sell, rent or both'),
        ),
    ]