# Generated by Django 3.2 on 2021-08-23 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_options'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('open', 'Открытый'), ('in_progress', 'В обработке'), ('cancelled', 'Отмененный'), ('finished', 'Завершенный')], default='open', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_item', to='product.product'),
        ),
    ]
