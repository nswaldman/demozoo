# Generated by Django 3.1.13 on 2021-07-11 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_entry_phase_phasestaffmember'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phasestaffmember',
            options={'ordering': ['role']},
        ),
    ]