# Generated by Django 3.1.7 on 2021-03-06 15:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("testruns", "0012_test_execusion_add_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicaltestrun",
            name="product_version",
        ),
        migrations.RemoveField(
            model_name="testrun",
            name="product_version",
        ),
    ]
