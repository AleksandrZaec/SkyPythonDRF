# Generated by Django 5.0.6 on 2024-06-26 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_course_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
    ]
