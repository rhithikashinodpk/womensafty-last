# Generated by Django 4.2.4 on 2024-04-02 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_guardianname_complaint_guardian_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('approved', 'approved')], default='pending', max_length=200),
        ),
    ]
