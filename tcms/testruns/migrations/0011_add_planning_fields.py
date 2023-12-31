# Generated by Django 3.1.6 on 2021-02-15 13:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testruns", "0010_rename_related_names"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicaltestrun",
            name="planned_start",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="historicaltestrun",
            name="planned_stop",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="testrun",
            name="planned_start",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="testrun",
            name="planned_stop",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
