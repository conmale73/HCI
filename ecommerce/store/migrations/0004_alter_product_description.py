# Generated by Django 4.1.7 on 2023-02-24 05:22

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_alter_product_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Text"),
        ),
    ]
