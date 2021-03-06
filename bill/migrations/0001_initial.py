# Generated by Django 3.0.6 on 2020-05-25 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('bill_date', models.DateField()),
                ('bill_details', models.CharField(max_length=200)),
                ('is_paid', models.BooleanField(default=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_case', to='case.case')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_item', to='stock.items')),
            ],
        ),
    ]
