# Generated by Django 2.0.3 on 2018-04-05 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sef_portal.Area'),
        ),
    ]
