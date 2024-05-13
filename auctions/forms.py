from django import forms
from .models import Listing

class CreateListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        # Sets image field required to false
        self.fields['image'].required = False
        # Iterates over fields, removes field label and adds bootstrap html attributes 
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs.update({
                'class': 'form-control', 
                'placeholder': f"{field_name.capitalize()}"
                })

    class Meta:
        model = Listing
        fields = ('title', 'description', 'image', 'price', 'category')
