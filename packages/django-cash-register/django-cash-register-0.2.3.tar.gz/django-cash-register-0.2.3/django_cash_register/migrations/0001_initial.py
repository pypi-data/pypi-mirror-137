from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cash_register.fields
import django_cash_register.models
import django_cash_register.validators


def create_actions(apps, schema_editor):
    action_tuple = ('Product addition', 'Product change', 'Product removal', 'Write-off of product', 'Product returns',
                    'Sale of products')
    action_model = apps.get_model('django_cash_register', 'ActionType',)

    for action in action_tuple:
        action_model.objects.create(name=action)


def create_currencies(apps, schema_editor):
    currency_tuple = ('₽', '$', '€')
    currency_model = apps.get_model('django_cash_register', 'Currency')

    for currency in currency_tuple:
        if currency != '₽':
            currency_model.objects.create(value=currency, float_right=False)
        else:
            currency_model.objects.create(value=currency, float_right=True)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'type',
                'verbose_name_plural': 'Actions',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=3, verbose_name='Currency')),
                ('float_right', models.BooleanField(default=False, verbose_name='Fload right')),
                ('active', django_cash_register.fields.UniqueBooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'currency',
                'verbose_name_plural': 'Currencies',
            },
            bases=(models.Model, django_cash_register.models.LastUpdateCartList),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('barcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='Barcode')),
                ('qrcode', models.CharField(blank=True, max_length=500, null=True, verbose_name='QR-code')),
                ('product_count', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Count')),
                ('weight', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Weight')),
                ('purchase_price', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Purchase price')),
                ('price', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Price')),
                ('promotion_price', models.FloatField(blank=True, null=True, validators=[django_cash_register.validators.positive_number], verbose_name='Promotional price')),
                ('promotion_product', models.BooleanField(default=False, verbose_name='Promotional product')),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/images/', verbose_name='Image')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_cash_register.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model, django_cash_register.models.AddProductHistory, django_cash_register.models.LastUpdateCartList),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'unit',
                'verbose_name_plural': 'Units',
            },
        ),
        migrations.CreateModel(
            name='ProductHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('barcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='Barcode')),
                ('qrcode', models.CharField(blank=True, max_length=500, null=True, verbose_name='QR-code')),
                ('product_count', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Count')),
                ('weight', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Weight')),
                ('purchase_price', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Purchase price')),
                ('price', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Price')),
                ('promotion_price', models.FloatField(blank=True, null=True, validators=[django_cash_register.validators.positive_number], verbose_name='Promotional price')),
                ('promotion_product', models.BooleanField(default=False, verbose_name='Promotional product')),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/images/', verbose_name='Image')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('action_date', models.DateTimeField(auto_now=True, verbose_name='Date')),
                ('exists', models.BooleanField(verbose_name='Available')),
                ('action', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='django_cash_register.actiontype', verbose_name='Action')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='django_cash_register.category', verbose_name='Category')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_cash_register.product', verbose_name='Product')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_cash_register.unit', verbose_name='Unit')),
            ],
            options={
                'verbose_name': 'history',
                'verbose_name_plural': 'History',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_cash_register.unit', verbose_name='Unit'),
        ),
        migrations.CreateModel(
            name='CartList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Last update')),
                ('user', models.ForeignKey(limit_choices_to={'is_active': True, 'is_staff': True}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Cashier')),
            ],
            options={
                'verbose_name': 'cart action',
                'verbose_name_plural': 'Cart list',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_count', models.FloatField(validators=[django_cash_register.validators.positive_number], verbose_name='Count')),
                ('cart_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_cash_register.cartlist', verbose_name='Cart number')),
                ('product', models.ForeignKey(limit_choices_to={'active': True}, on_delete=django.db.models.deletion.PROTECT, to='django_cash_register.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'Open carts',
            },
            bases=(models.Model, django_cash_register.models.AddProductHistory),
        ),
        migrations.RunPython(create_actions),
        migrations.RunPython(create_currencies),
    ]
