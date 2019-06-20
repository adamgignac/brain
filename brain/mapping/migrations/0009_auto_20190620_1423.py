# Generated by Django 2.2.2 on 2019-06-20 14:23

from django.db import migrations, models
import django.db.models.deletion

def update_dependencies(apps, schema_editor):
    Item = apps.get_model('mapping', 'Item')
    Dependency = apps.get_model('mapping', 'Dependency')
    for item in Item.objects.all():
        for dep in item.dependencies.all():
            Dependency.objects.create(item1=item, item2=dep, workspace=item.workspace)


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0008_auto_20190620_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependency',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='mapping.Workspace'),
        ),
        migrations.RunPython(update_dependencies, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='item',
            name='dependencies',
            field=models.ManyToManyField(blank=True, to='mapping.Item'),
        ),
    ]