from django.core import exceptions
from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, password_validation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

UserModel = get_user_model()

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from recipes.models import Recipe, RecipeCategory
from ingredients.models import Ingredient


def validate_password_strength(value):
    """Validates that a password is as least 7 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 7

    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters '
                                'long.').format(min_length))

    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must contain at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must contain at least 1 letter.'))


@login_required
def favourite_recipe_list(request):
    new = Recipe.objects.filter(favourites=request.user)
    return render(request,
                  'account/favourite_recipes.html',
                  {'new': new})


@login_required
def favourite_recipe_add(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.favourites.filter(id=request.user.id).exists():
        recipe.favourites.remove(request.user)
    else:
        recipe.favourites.add(request.user)
    # return HttpResponseRedirect(reverse('recipes:recipe_detail', args=[str(id)]))

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
# @login_required
# def add_to_cart(request, id):
#     recipe = get_object_or_404(Recipe, id=id)
#     user = get_object_or_404(User, id=request.user.id)
#     # if Cart.objects.all().filter(id=request.user.id).exists():
#     #     cart = Cart(recipe=recipe, user=user)
#     #     cart.delete()
#     # else:
#     if not Cart.objects.all().filter(recipe=recipe).exists():
#         cart = Cart(recipe=recipe, user=user)
#         cart.save()
#     else:
#         print("exists")
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])



@login_required
def favourite_ingredient_list(request):
    new = Ingredient.objects.filter(favourites=request.user)
    return render(request,
                  'account/favourite_ingredients.html',
                  {'new': new})


@login_required
def favourite_ingredient_add(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    if ingredient.favourites.filter(id=request.user.id).exists():
        ingredient.favourites.remove(request.user)
    else:
        ingredient.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def cart_list(request):
    cart = Recipe.objects.filter(cart=request.user)
    return render(request,
                  'account/cart.html',
                  {'cart': cart})


@login_required
def add_to_cart(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.cart.filter(id=request.user.id).exists():
        recipe.cart.remove(request.user)
    else:
        recipe.cart.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('ingredients/ingredient/list.html')
                    # return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'GET':
        return render(request, 'account/register.html')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # try:
            #     password_validation.validate_password(user_form.cleaned_data['password'])
            # except exceptions.ValidationError as e:
            #     raise forms.ValidationError('Invalid value')
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': default_token_generator.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

            # return render(request,
            #               'account/register_done.html',
            #               {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        Profile.objects.create(user=user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


class CategoryDetailView(DetailView):
    model = RecipeCategory
    context_object_name = 'category'
    # paginate_by = 2
    template_name = 'base.html'