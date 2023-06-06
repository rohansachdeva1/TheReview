from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    #final_score = forms.DecimalField(required=True, min_value=0, max_value=5, decimal_places=1)
    blurb = forms.CharField(required=True,
            widget=forms.widgets.Textarea(
                attrs={
                    "placeholder": "Enter your blurb",
                    "class":"form-control",
                }
            ),
            label="",
        )
    
    class Meta:
        model = Review
        exclude = ("user", "entity")