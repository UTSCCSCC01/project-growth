# Generated by Django 3.2.4 on 2021-07-01 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0032_alter_photo_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company_page.company'),
        ),
    ]
