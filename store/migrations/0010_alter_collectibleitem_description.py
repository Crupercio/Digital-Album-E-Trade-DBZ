# Generated by Django 5.1.2 on 2024-10-18 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_collectibleitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectibleitem',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
