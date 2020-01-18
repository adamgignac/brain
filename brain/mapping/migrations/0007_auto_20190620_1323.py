# Generated by Django 2.2.2 on 2019-06-20 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("mapping", "0006_auto_20190620_1313")]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="slug",
            field=models.SlugField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="itemtype",
            name="slug",
            field=models.SlugField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="workspace",
            name="slug",
            field=models.SlugField(editable=False, unique=True),
        ),
    ]
