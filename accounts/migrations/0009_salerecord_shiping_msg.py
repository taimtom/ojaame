# Generated by Django 2.2.6 on 2020-11-24 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20201029_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='salerecord',
            name='shiping_msg',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
