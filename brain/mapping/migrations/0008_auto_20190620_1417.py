# Generated by Django 2.2.2 on 2019-06-20 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("mapping", "0007_auto_20190620_1323")]

    operations = [
        migrations.CreateModel(
            name="Dependency",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
        ),
        migrations.AddField(
            model_name="dependency",
            name="item1",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supports",
                to="mapping.Item",
            ),
        ),
        migrations.AddField(
            model_name="dependency",
            name="item2",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="depends_on",
                to="mapping.Item",
            ),
        ),
        migrations.AddField(
            model_name="dependency",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dependencies",
                to="mapping.Workspace",
            ),
        ),
    ]
