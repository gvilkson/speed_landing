from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser precisa ter is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('SuperUser precisa ter is_staff=True')
        
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Adicione campos adicionais aqui, como um campo de perfil
    # A opção blank=True permite que este campo seja deixado em branco ao criar um usuário
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, blank=True)
    email = models.EmailField('E-mail', max_length=254, unique=True)
    phone = PhoneNumberField('Telefone', blank=False, unique=True)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    # Configuração de authenticação.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    # Aqui, o relacionamento OneToOne é estabelecido
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email
    
    objects = CustomUserManager()


class UserProfile(models.Model):
    # Aqui você pode adicionar todos os campos que você precisa para o perfil do usuário
    # Por exemplo, você pode incluir um campo bio e um campo de imagem de perfil
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField('Avatar', upload_to='avatars/', null=True, blank=True, height_field=None, width_field=None, max_length=100)
    country = CountryField(default='BR')

    class Meta:
        verbose_name = "Perfil do usuário"
        verbose_name_plural = "Perfis dos usuários"
        ordering = ["user__username"]

    def __str__(self):
        return self.user.username
    
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/static/assets/images/avatars/avatar-2.png"
    
class Address(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = CountryField()
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return self.user_profile.user.get_full_name()
    
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        ordering = ["user_profile__user__username"]

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.profile is not None:  # Check if instance.profile is None before saving
        instance.profile.save()

# Adicione os signals para criar ou salvar o UserProfile quando um CustomUser for criado/salvo
post_save.connect(create_user_profile, sender=CustomUser)
post_save.connect(save_user_profile, sender=CustomUser)
