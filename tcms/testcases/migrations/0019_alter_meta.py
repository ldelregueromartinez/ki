# Generated by Django 3.2.6 on 2021-08-26 15:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("testcases", "0018_add_testcase_duration_fields"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
    ]
