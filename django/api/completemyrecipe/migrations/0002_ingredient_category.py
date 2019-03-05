# Generated by Django 2.1.7 on 2019-03-04 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('completemyrecipe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='category',
            field=models.CharField(choices=[('P', 'Protein'), ('G', 'Grain'), ('F', 'Fruit'), ('V', 'Vegetable')], default=('U', 'Unknown'), max_length=1),
        ),
    ]