# Generated by Django 4.2.11 on 2024-05-03 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_remove_purchaseorder_id_remove_vendor_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='issue_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
