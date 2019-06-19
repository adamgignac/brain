# Generated by Django 2.2.2 on 2019-06-19 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='color',
            field=models.CharField(choices=[('white', 'White'), ('gray', 'Gray'), ('red', 'Red'), ('orange', 'Orange'), ('yellow', 'Yellow'), ('green', 'Green'), ('cyan', 'Cyan'), ('violet', 'Violet'), ('beige', 'Beige'), ('plum', 'Plum'), ('salmon', 'Salmon'), ('turquiose', 'Turquoise'), ('goldenrod', 'Goldenrod'), ('firebrick', 'Firebrick'), ('chocolate', 'Chocolate'), ('steelblue', 'Steel Blue'), ('springgreen', 'Spring Green')], default='white', max_length=15),
        ),
    ]