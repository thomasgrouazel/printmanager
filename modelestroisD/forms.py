from django import forms
from .models import Modele, Variante, Version, Tag
import os

def get_image_choices():
    MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media/images')
    choices = [(f"images/{img}", img) for img in os.listdir(MEDIA_ROOT) if os.path.isfile(os.path.join(MEDIA_ROOT, img))]
    choices.insert(0, ('', '-------'))
    return choices

class ModeleForm(forms.ModelForm):
    existing_image = forms.ChoiceField(choices=get_image_choices(), required=False, label="Choisir une image existante")

    class Meta:
        model = Modele
        fields = ["name", "image", "description", "tags", "existing_image"]

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        existing_image = cleaned_data.get('existing_image')

        if not image and not existing_image:
            raise forms.ValidationError("Vous devez soit télécharger une nouvelle image soit choisir une image existante.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        existing_image = self.cleaned_data.get('existing_image')
        if existing_image:
            instance.image = existing_image
        if commit:
            instance.save()
        return instance


class VarianteForm(forms.ModelForm):
    class Meta: 
        model = Variante
        fields = ["name", "description", "image"]

class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ["name", "description", "image", "file"]

# class addVersionForm(forms.ModelForm):
#     class Meta:
#         model = Version
#         fields = ["name", "description", "image", "file"]
