from django import forms
from django.contrib.auth.models import User, Group

class UserForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Rol")
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Eliminar help_text de todos los campos
        for field_name, field in self.fields.items():
            field.help_text = ''
        
        if self.instance.pk:
            self.fields['password'].required = False
            # Set initial group
            groups = self.instance.groups.all()
            if groups:
                self.fields['group'].initial = groups[0].pk
        else:
            self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            # Update group
            user.groups.clear()
            user.groups.add(self.cleaned_data['group'])
        return user
