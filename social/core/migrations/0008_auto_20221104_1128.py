# Generated by Django 3.2.11 on 2022-11-04 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20221104_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dweet',
            name='Img',
            field=models.ImageField(upload_to='dweet_img'),
        ),
        migrations.AlterField(
            model_name='likedweet',
            name='dweetid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.dweet'),
        ),
    ]
