from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.core.exceptions import ValidationError
from .models import CustomUser, UserProfile, Address

class CustomUserCreateForm(UserCreationForm):
    phone = PhoneNumberField(label='Telefone', required=True)
    avatar = forms.ImageField(label='Avatar', required=False)
    country = forms.ChoiceField(
        label='País', choices=[(country.code, country.name) for country in CountryField().countries],
        widget=CountrySelectWidget()
    )
    street = forms.CharField(label='Rua', max_length=255, required=True)
    city = forms.CharField(label='Cidade', max_length=50, required=True)
    state = forms.CharField(label='Estado', max_length=50, required=True)
    postal_code = forms.CharField(label='Código Postal', max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'avatar', 'country', 'street', 'city', 'state', 'postal_code')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso. Por favor, escolha outro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este endereço de e-mail já está em uso. Por favor, escolha outro.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        
        if commit:
            user.save()
            # Criando o perfil do usuário
            profile = UserProfile(user=user, avatar=self.cleaned_data['avatar'], country=self.cleaned_data['country'])
            profile.save()
            # Criando o endereço do usuário
            address = Address(
                user_profile=profile,
                street=self.cleaned_data['street'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                country=self.cleaned_data['country'],
                postal_code=self.cleaned_data['postal_code']
            )
            address.save()
        return user

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone')
