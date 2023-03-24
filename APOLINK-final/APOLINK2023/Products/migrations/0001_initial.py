# Generated by Django 4.1.6 on 2023-03-10 14:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ThirdLevelCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('short_name', models.CharField(blank=True, max_length=40, null=True)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='Core/Static/Photos/ThirdLevelCategories')),
                ('parent_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.secondlevelcategories')),
            ],
        ),
        migrations.CreateModel(
            name='ProductsDisplayed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_registered', models.DateField(default=django.utils.timezone.now)),
                ('date_updated', models.DateField(auto_now=True)),
                ('manufactured_date', models.DateField(null=True)),
                ('product_name', models.CharField(max_length=200)),
                ('product_short_description', models.TextField(blank=True, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True)),
                ('for_sell_rent', models.CharField(blank=True, choices=[('Selling or Renting', 'For Selling or Renting'), ('Selling', 'For Selling'), ('Renting', 'For Renting')], max_length=40, null=True, verbose_name='For sell, rent or both')),
                ('model', models.CharField(blank=True, max_length=200, null=True)),
                ('product_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Products.thirdlevelcategories')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product Displayed',
                'verbose_name_plural': 'Products Displayed',
            },
        ),
        migrations.CreateModel(
            name='ProductPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='upload/')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Products.productsdisplayed')),
            ],
        ),
        migrations.CreateModel(
            name='DispersersSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('batch', 'Batch'), ('continuous', 'Continuous')], max_length=25, null=True, verbose_name='Batch/Continuous')),
                ('power', models.FloatField(verbose_name='Motor Power in kW')),
                ('application', models.CharField(blank=True, max_length=80, null=True, verbose_name='Application')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Products.productsdisplayed')),
            ],
        ),
        migrations.CreateModel(
            name='CaseSealerSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('BtmDr', 'Bottom Driven'), ('SdDr', 'Side Driven'), ('T&BtmDr', 'Top & Bottom Driven')], max_length=25, null=True, verbose_name='Case Sealer Type')),
                ('min_box_size_cm', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)], verbose_name='Minimum Box Size (cm)')),
                ('max_box_size_cm', models.PositiveIntegerField(default=20, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Maximum Box Size (cm)')),
                ('boxes_per_min', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Maximum boxes per min')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Products.productsdisplayed')),
            ],
        ),
        migrations.CreateModel(
            name='CasePackerSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('top', 'Top Loader'), ('side', 'Side Loader'), ('P&PL', 'Pick and Place')], max_length=25, null=True, verbose_name='Case Packer Type')),
                ('boxes_per_min', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Maximum boxes per min')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Products.productsdisplayed')),
            ],
        ),
    ]
