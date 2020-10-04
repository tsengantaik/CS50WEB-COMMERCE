# Generated by Django 3.1.1 on 2020-09-26 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200926_2022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categorylist',
            old_name='categoryname',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='auctionlist',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.categorylist'),
        ),
    ]
