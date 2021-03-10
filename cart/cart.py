from decimal import Decimal
from django.conf import settings
from recipes.models import Recipe


# class Cart(object):
#     def __init__(self, request):
#         self.session = request.sessionn
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
#
#     def add(self, recipe):