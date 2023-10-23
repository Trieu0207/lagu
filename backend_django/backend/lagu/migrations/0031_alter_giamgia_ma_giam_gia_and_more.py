# Generated by Django 4.2.5 on 2023-10-12 00:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lagu', '0030_rename_ma_dat_ban_dsdatban_ma_dat_ban_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giamgia',
            name='ma_giam_gia',
            field=models.CharField(blank=True, default='V2L00N', max_length=7, unique=True),
        ),
        migrations.AlterField(
            model_name='hoadoncoctien',
            name='ngay_thanh_toan',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 12, 7, 51, 57, 530597)),
        ),
    ]
