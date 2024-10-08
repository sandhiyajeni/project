# Generated by Django 5.0.6 on 2024-06-04 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='pimage',
            field=models.ImageField(default=0, upload_to='media/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='cat',
            field=models.IntegerField(choices=[(1, 'cloth'), (2, 'shoes'), (3, 'mobile')]),
        ),
    ]
