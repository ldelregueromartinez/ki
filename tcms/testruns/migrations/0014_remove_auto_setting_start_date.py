# Generated by Django 3.1.6 on 2021-04-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testruns", "0013_remove_product_version"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicaltestrun",
            name="start_date",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="testrun",
            name="start_date",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
