# Generated by Django 3.0.3 on 2020-06-05 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0014_order_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='successful',
            field=models.BooleanField(default=False),
        ),
    ]