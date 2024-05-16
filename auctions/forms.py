from django import forms
from .models import Listing, Comment

class CreateListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
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

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs.update({
                'class': 'form-control', 
                'placeholder': f"{field_name.capitalize()}"
                })
        
    class Meta:
        model = Comment
        fields = ('comment', )
