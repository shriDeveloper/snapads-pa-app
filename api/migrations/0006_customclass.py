# Generated by Django 3.1.5 on 2021-02-04 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210124_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_token', models.CharField(blank=True, max_length=100, null=True)),
                ('custom_classes', models.TextField(blank=True, null=True)),
                ('custom_font', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
