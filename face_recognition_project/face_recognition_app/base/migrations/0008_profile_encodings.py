# Generated by Django 4.0.6 on 2022-08-07 14:28

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_profile_delete_accounts_remove_orderitem_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='encodings',
            field=picklefield.fields.PickledObjectField(blank=True, editable=False, null=True),
        ),
    ]
