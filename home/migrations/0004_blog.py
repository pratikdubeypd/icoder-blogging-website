# Generated by Django 3.1.1 on 2021-07-04 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210704_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(blank=True)),
            ],
        ),
    ]