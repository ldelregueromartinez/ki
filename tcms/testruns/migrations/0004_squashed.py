# Generated by Django 2.1.2 on 2018-10-22 19:11

from django.conf import settings
from django.db import migrations, models

import tcms.core.models.base

CASE_RUN_STATUS_ID_COLUMN = "case_run_status_id"
if settings.DATABASES["default"]["ENGINE"].find("sqlite") > -1:
    CASE_RUN_STATUS_ID_COLUMN = ""


def forwards_add_initial_data(apps, schema_editor):
    test_case_run_status_model = apps.get_model("testruns", "TestCaseRunStatus")

    test_case_run_status_model.objects.bulk_create(
        [
            test_case_run_status_model(name="IDLE"),
            test_case_run_status_model(name="RUNNING"),
            test_case_run_status_model(name="PAUSED"),
            test_case_run_status_model(name="PASSED"),
            test_case_run_status_model(name="FAILED"),
            test_case_run_status_model(name="BLOCKED"),
            test_case_run_status_model(name="ERROR"),
            test_case_run_status_model(name="WAIVED"),
        ]
    )


def reverse_add_initial_data(apps, schema_editor):
    test_case_run_status_model = apps.get_model("testruns", "TestCaseRunStatus")
    status_names = [
        "IDLE",
        "RUNNING",
        "PAUSED",
        "PASSED",
        "FAILED",
        "BLOCKED",
        "ERROR",
        "WAIVED",
    ]
    test_case_run_status_model.objects.filter(name__in=status_names).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("management", "0003_squashed"),
        ("testcases", "0001_initial"),
        ("testplans", "0005_squashed"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TestCaseRun",
            fields=[
                ("case_run_id", models.AutoField(primary_key=True, serialize=False)),
                ("case_text_version", models.IntegerField()),
                ("running_date", models.DateTimeField(blank=True, null=True)),
                ("close_date", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("sortkey", models.IntegerField(blank=True, null=True)),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.CASCADE,
                        related_name="case_run_assignee",
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
                    "case",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="case_run",
                        to="testcases.TestCase",
                    ),
                ),
            ],
            bases=(models.Model, tcms.core.models.base.UrlMixin),
        ),
        migrations.CreateModel(
            name="TestCaseRunStatus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        db_column=CASE_RUN_STATUS_ID_COLUMN,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=60, unique=True)),
            ],
            bases=(models.Model, tcms.core.models.base.UrlMixin),
        ),
        migrations.CreateModel(
            name="TestRun",
            fields=[
                ("run_id", models.AutoField(primary_key=True, serialize=False)),
                ("start_date", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "stop_date",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("summary", models.TextField()),
                ("notes", models.TextField(blank=True)),
                (
                    "build",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="build_run",
                        to="management.Build",
                    ),
                ),
            ],
            bases=(models.Model, tcms.core.models.base.UrlMixin),
        ),
        migrations.CreateModel(
            name="TestRunCC",
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
                (
                    "run",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="cc_list",
                        to="testruns.TestRun",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_column="who",
                        on_delete=models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TestRunTag",
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
                (
                    "run",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="testruns.TestRun"
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="management.Tag"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="testrun",
            name="cc",
            field=models.ManyToManyField(
                through="testruns.TestRunCC", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="testrun",
            name="default_tester",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="default_tester",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="testrun",
            name="manager",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="manager",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="testrun",
            name="plan",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="run",
                to="testplans.TestPlan",
            ),
        ),
        migrations.AddField(
            model_name="testrun",
            name="product_version",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="version_run",
                to="management.Version",
            ),
        ),
        migrations.AddField(
            model_name="testrun",
            name="tag",
            field=models.ManyToManyField(
                related_name="run", through="testruns.TestRunTag", to="management.Tag"
            ),
        ),
        migrations.AddField(
            model_name="testcaserun",
            name="case_run_status",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to="testruns.TestCaseRunStatus"
            ),
        ),
        migrations.AddField(
            model_name="testcaserun",
            name="run",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="case_run",
                to="testruns.TestRun",
            ),
        ),
        migrations.AddField(
            model_name="testcaserun",
            name="tested_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="case_run_tester",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="testruncc",
            unique_together={("run", "user")},
        ),
        migrations.AlterUniqueTogether(
            name="testrun",
            unique_together={("run_id", "product_version")},
        ),
        migrations.AlterUniqueTogether(
            name="testcaserun",
            unique_together={("case", "run", "case_text_version")},
        ),
        migrations.RunPython(forwards_add_initial_data, reverse_add_initial_data),
        migrations.AlterField(
            model_name="testruntag",
            name="run",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="tags",
                to="testruns.TestRun",
            ),
        ),
        migrations.CreateModel(
            name="HistoricalTestCaseRun",
            fields=[
                ("case_run_id", models.IntegerField(blank=True, db_index=True)),
                ("case_text_version", models.IntegerField()),
                ("running_date", models.DateTimeField(blank=True, null=True)),
                ("close_date", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("sortkey", models.IntegerField(blank=True, null=True)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_change_reason", models.TextField(null=True)),
                ("history_date", models.DateTimeField()),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "build",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to="management.Build",
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to="testcases.TestCase",
                    ),
                ),
                (
                    "case_run_status",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to="testruns.TestCaseRunStatus",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "run",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to="testruns.TestRun",
                    ),
                ),
                (
                    "tested_by",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical test case run",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
        ),
        migrations.CreateModel(
            name="HistoricalTestRun",
            fields=[
                ("run_id", models.IntegerField(blank=True, db_index=True)),
                (
                    "start_date",
                    models.DateTimeField(blank=True, db_index=True, editable=False),
                ),
                (
                    "stop_date",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("summary", models.TextField()),
                ("notes", models.TextField(blank=True)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_change_reason", models.TextField(null=True)),
                ("history_date", models.DateTimeField()),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "build",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to="management.Build",
                    ),
                ),
                (
                    "default_tester",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "manager",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to="testplans.TestPlan",
                    ),
                ),
                (
                    "product_version",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=models.deletion.DO_NOTHING,
                        related_name="+",
                        to="management.Version",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical test run",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
        ),
    ]
