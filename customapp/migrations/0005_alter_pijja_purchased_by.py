# Generated by Django 5.1.3 on 2024-11-09 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customapp', '0004_alter_pijja_last_modified_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pijja',
            name='purchased_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='customapp.dumdumuser'),
        ),
    ]