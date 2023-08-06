from django.db import models
from django.conf import settings

from .fields import UniqueBooleanField
from .functions import get_call_info
from .validators import positive_number



class LastUpdateCartList():
    def _last_update(self):
        carts = CartList.objects.all()

        for cart in carts:
            cart.save()


class AddProductHistory(LastUpdateCartList):
    def _check_changes(self):
        """Checks if the product has changed."""

        befor_change = dict(Product.objects.filter(pk=self.pk)[0].__dict__)
        after_change = dict(self.__dict__)
        del befor_change['_state']
        del after_change['_state']

        return befor_change != after_change
    
    def _choice_action_type(self, func_name):
        """Choice action type."""

        if func_name == 'save':
            exists = True

            if not self.pk:
                action_type = ActionType.objects.filter(name='Product addition').first()
            else:                
                if self._check_changes():              
                    action_type = ActionType.objects.filter(name='Product change').first()
                else:
                    return False, False

        elif func_name == 'delete':
            exists = False
            action_type = ActionType.objects.filter(name='Product removal').first()
        
        elif func_name == 'sell':
            exists = True
            action_type = ActionType.objects.filter(name='Sale of products').first()

        return action_type, exists

    def _create_history_object(self, action_type, exists):
        """Creates a history object."""

        if self.__class__.__name__ == 'Cart':
            product = self.product
        else:
            product = self
            
        ProductHistory.objects.create(
            product=product,
            action=action_type,
            name=product.name,
            barcode=product.barcode,
            qrcode=product.qrcode,
            category=product.category,
            product_count=product.product_count,
            unit=product.unit,
            weight=product.weight,
            purchase_price=product.purchase_price,
            price=product.price,
            promotion_price=product.promotion_price,
            image=product.image,
            active=product.active,
            exists=exists
        )
    
    def _add_history(self, call_info):
        """Adding history."""

        super_func = f'super({call_info[1]}, self).{call_info[-1]}()'

        if call_info[1] in ('Cart', 'Product'):
            action_type, exists = self._choice_action_type(call_info[-1])

            if call_info[1] == 'Product':
                if call_info[-1] == 'save':
                    if action_type:
                        exec(super_func)
                        self._create_history_object(action_type, exists)
                        self._last_update()

                if call_info[-1] == 'delete':
                    self._create_history_object(action_type, exists)
                    exec(super_func)
                    self._last_update()

            elif call_info[1] == 'Cart':
                if call_info[-1] == 'sell':
                    self._create_history_object(action_type, exists)
                    self._last_update()


class ActionType(models.Model):
    """Model of the types of actions performed with the product."""

    name = models.CharField(max_length=255, verbose_name='Name')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'type'
        verbose_name_plural = 'Actions'


class Category(models.Model):
    """Product category model."""

    name = models.CharField(max_length=255, verbose_name='Name')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'


class Unit(models.Model):
    """Unit model."""

    name = models.CharField(max_length=20, verbose_name='Name')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'unit'
        verbose_name_plural = 'Units'


class AbstractProduct(models.Model):
    """Abstract model for Product models."""

    name = models.CharField(max_length=255, verbose_name='Name')
    barcode = models.CharField(max_length=255, null=True, blank=True, verbose_name='Barcode')
    qrcode = models.CharField(max_length=500, null=True, blank=True, verbose_name='QR-code')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Category')
    product_count = models.FloatField(validators=[positive_number], verbose_name='Count')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='Unit')
    weight = models.FloatField(validators=[positive_number], verbose_name='Weight')
    purchase_price = models.FloatField(validators=[positive_number], verbose_name='Purchase price')
    price = models.FloatField(validators=[positive_number], verbose_name='Price')
    promotion_price = models.FloatField(validators=[positive_number], null=True, blank=True,
                                        verbose_name='Promotional price')
    promotion_product = models.BooleanField(default=False, verbose_name='Promotional product')
    image = models.ImageField(upload_to='static/images/', null=True, blank=True, verbose_name='Image')
    active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        abstract = True


class Product(AbstractProduct, AddProductHistory, LastUpdateCartList):
    """The product model is inherited from the 'AbstractProduct' abstract model.
    When you perform actions on the model, you interact with the 'ProductHistory' model."""

    def save(self, sell=False, *args, **kwargs):
        """Redefined 'create'/'update' function. It then adds an entry to the 'ProductHistory' model."""
        if not sell:
            self._add_history(get_call_info(self))
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Redefined 'delete' function. It then adds an entry to the 'ProductHistory' model."""

        self._add_history(get_call_info(self))

    def __str__(self):
        return f'[{self.pk}] {self.name}'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'Products'


class CartList(models.Model):
    """Cart model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True, 'is_active': True},
                             on_delete=models.PROTECT, verbose_name='Cashier')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Last update')

    def __str__(self):
        full_name = self.user.get_full_name()

        if full_name:
            full_name = f' / {self.user.get_full_name()}'

        return f'[{self.pk}] {self.user}{full_name}'

    class Meta:
        verbose_name = 'cart action'
        verbose_name_plural = 'Cart list'


class Cart(models.Model, AddProductHistory):
    """Open cart model."""

    cart_number = models.ForeignKey(CartList, on_delete=models.CASCADE, verbose_name='Cart number')
    product = models.ForeignKey(Product, limit_choices_to={'active': True}, on_delete=models.PROTECT,
                                verbose_name='Product')
    product_count = models.FloatField(validators=[positive_number], verbose_name='Count')

    @staticmethod
    def _add_test_product():
        """Adding a test product to the cart."""

        cart_number = CartList.objects.first()
        product = Product.objects.last()
        product_count = 1
        Cart.objects.create(cart_number=cart_number, product=product, product_count=product_count)

    @staticmethod
    def sell_all(cart_number):
        """Sale of all products."""

        carts = Cart.objects.filter(cart_number=cart_number)
        for cart in carts:
            cart.sell()
    
    @staticmethod
    def delete_all(cart_number):
        """Delete all products."""

        Cart.objects.filter(cart_number=cart_number).delete()

    def product_count_plus(self, *args, **kwargs):
        """Adding +1 to product cart."""

        self.product_count += 1
        super().save(*args, **kwargs)
        self._last_update()

    def product_count_minus(self, *args, **kwargs):
        """Removing -1 from cart."""

        self.product_count -= 1
        super().save(*args, **kwargs)
        self._last_update()
        
    def sell(self, *args, **kwargs):
        """Sale of products."""

        self.product.product_count -= self.product_count
        self.product.save(True)
        self._add_history(get_call_info(self))
        super().delete(*args, **kwargs)
        self._last_update()

    def save(self, *args, **kwargs):
        """Redefined 'create'/'update' function. It then updates the 'last_last_update' in the 'CartList' model."""
        
        product = Cart.objects.filter(product__pk=self.product.pk).first()
        
        if product is None:
            super().save(*args, **kwargs)
            self._last_update()

    def delete(self,  *args, **kwargs):
        """Redefined 'delete' function. It then updates the 'last_last_update' in the 'CartList' model."""

        super().delete(*args, **kwargs)
        self._last_update()

    def __str__(self):
        return f'{self.product.price} / {self.product.name}'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'Open carts'


class ProductHistory(AbstractProduct):
    """Product history model."""

    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name='Product')
    action = models.ForeignKey(ActionType, null=True, on_delete=models.PROTECT, verbose_name='Action')
    action_date = models.DateTimeField(auto_now=True, verbose_name='Date')
    exists = models.BooleanField(verbose_name='Available')

    def __str__(self):
        if self.product is None:
            return f'{self.product}'
        else:
            return f'{self.product.name}'

    class Meta:
        verbose_name = 'history'
        verbose_name_plural = 'History'


class Currency(models.Model, LastUpdateCartList):
    """Currency model."""

    value = models.CharField(max_length=3, verbose_name='Currency')
    float_right = models.BooleanField(default=False, verbose_name='Fload right')
    active = UniqueBooleanField(default=True, verbose_name='Active')

    def save(self, *args, **kwargs):
        """Redefined 'create'/'update' function. It then updates the 'last_last_update' in the 'CartList' model."""

        super().save(*args, **kwargs)
        self._last_update()

    def delete(self, *args, **kwargs):
        """Redefined 'delete' function. It then updates the 'last_last_update' in the 'CartList' model."""

        super().delete(*args, **kwargs)
        self._last_update()

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'currency'
        verbose_name_plural = 'Currencies'
