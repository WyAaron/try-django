# Generated by Django 4.1.7 on 2023-03-23 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CVSMS', '0010_delete_storagenodemetadata_alter_files_filename_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storagenodeinfo',
            name='maxSize',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='files',
            name='SID',
            field=models.CharField(choices=[('NONE', 'NONE'), ('PARITY', 'PARITY'), ('1', '1'), ('0', '0')], default='NONE', max_length=256, null=True),
        ),
    ]
