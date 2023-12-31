# Generated by Django 2.2.5 on 2019-09-03 20:30

from django.conf import settings
from django.db import migrations, models

import tcms.core.models.base


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("management", "0005_order_by_name"),
        ("testruns", "0006_rename_test_case_run_to_test_execution"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bug",
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
                ("summary", models.CharField(db_index=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("status", models.BooleanField(db_index=True, default=True)),
                (
                    "assignee",
                    models.ForeignKey(
                        null=True,
                        blank=True,
                        on_delete=models.deletion.CASCADE,
                        related_name="assigned_bugs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "build",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="management.Build"
                    ),
                ),
                (
                    "executions",
                    models.ManyToManyField(
                        related_name="bugs", to="testruns.TestExecution"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="management.Product"
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="repoted_bugs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(related_name="bugs", to="management.Tag"),
                ),
                (
                    "version",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="management.Version"
                    ),
                ),
            ],
            bases=(models.Model, tcms.core.models.base.UrlMixin),
        ),
    ]
