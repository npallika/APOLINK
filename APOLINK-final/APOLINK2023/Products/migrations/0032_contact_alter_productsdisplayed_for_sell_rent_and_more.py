# Generated by Django 4.1.7 on 2023-04-28 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0031_alter_productsdisplayed_for_sell_rent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
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
