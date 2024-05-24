from django import forms
from .models import Listing, Comment, Bid, Category

class CreateListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = f"{field_name.capitalize()}"
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"{field_name.capitalize()}"
                })
    
        self.fields['description'].widget = forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 5,
            })

    class Meta:
        model = Listing
        fields = ('title', 'description', 'image', 'price', 'category')

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add Comment',
                'rows': 5,
            })
        self.fields['comment'].label = ''
        
    class Meta:
        model = Comment
        fields = ('comment', )

class BidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs.update({
                'class': 'form-control', 
                'placeholder': f"{field_name.capitalize()}"
                })

    class Meta:
        model = Bid
        fields = ('bid', ) 
