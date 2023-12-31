# Generated by Django 4.2.4 on 2023-09-09 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='start_time',
            field=models.BigIntegerField(default=1694295751.891318),
        ),
        migrations.AlterField(
            model_name='runner',
            name='longest_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.run'),
        ),
    ]
