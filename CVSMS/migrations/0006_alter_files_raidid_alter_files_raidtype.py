# Generated by Django 4.1.7 on 2023-03-20 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CVSMS', '0005_alter_files_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='RAIDid',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='files',
            name='RAIDtype',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
