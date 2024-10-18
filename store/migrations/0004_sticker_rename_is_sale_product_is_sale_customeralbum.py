# Generated by Django 5.1.2 on 2024-10-17 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_is_sale_product_sale_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='stickers/')),
                ('page_number', models.IntegerField()),
                ('position_on_page', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='product',
            old_name='is_Sale',
            new_name='is_sale',
        ),
        migrations.CreateModel(
            name='CustomerAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collected', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.sticker')),
            ],
        ),
    ]
