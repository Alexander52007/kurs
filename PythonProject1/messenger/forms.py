from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_."
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Ваш пароль не должен быть слишком похож на другую вашу личную информацию."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Введите тот же пароль, что и выше, для подтверждения."
    )

    class Meta:
        model = User
        fields = ("username",)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'position', 'department', 'photo',
            'medical_specialization', 'experience_years', 'bio'
        ]
        labels = {
            'full_name': 'ФИО',
            'position': 'Должность',
            'department': 'Отделение',
            'photo': 'Фотография профиля',
            'medical_specialization': 'Медицинская специализация',
            'experience_years': 'Стаж (лет)',
            'bio': 'О себе',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'medical_specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
