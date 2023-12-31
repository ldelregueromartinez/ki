# Generated by Django 3.2.8 on 2021-10-28 10:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testruns", "0015_alter_testexecution_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestExecutionProperty",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
                (
                    "execution",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        to="testruns.testexecution",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
