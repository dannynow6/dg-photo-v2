from django import forms
from .models import Photo
from PIL import Image


class PhotoForm(forms.ModelForm):
    """A form for entering new photo info"""

    TYPES_CHOICES = [
        ("LS", "Landscape"),
        ("SP", "Street"),
        ("MP", "Macro"),
        ("AP", "Astrophotography"),
        ("PT", "Portrait"),
        ("NP", "Night"),
        ("BW", "Black & White"),
        ("TP", "Travel"),
        ("AS", "Abstract"),
        ("EP", "Experimental"),
        ("FP", "Fashion"),
        ("LE", "Long Exposure"),
        ("AL", "Aerial"),
    ]

    FORMAT_CHOICES = [
        ("FF", "Full-Frame"),
        ("MF", "Medium-Format"),
        ("AC", "APS-C"),
        ("FT", "Micro Four Thirds"),
        ("OF", "One-Inch"),
    ]

    class Meta:
        model = Photo
        fields = [
            "type",
            "location_city",
            "location_country",
            "title",
            "camera_make",
            "camera_model",
            "format",
            "description",
            "year_taken",
            "lens_make",
            "lens_model",
            "focal_length",
            "picture",
        ]
        labels = {
            "type": "Type",
            "location_city": "City",
            "location_country": "Country",
            "title": "Title",
            "camera_make": "Camera Make",
            "camera_model": "Camera Model",
            "format": "Format",
            "description": "Description",
            "year_taken": "Year Taken",
            "lens_make": "Lens Make",
            "lens_model": "Lens Model",
            "focal_length": "Focal Length",
            "picture": "Picture",
        }
        choices = {
            "type": "TYPE_CHOICES",
            "format": "FORMAT_CHOICES",
        }
        widgets = {
            "type": forms.Select(attrs={"id": "type-choice"}),
            "location_city": forms.TextInput,
            "location_country": forms.TextInput,
            "title": forms.TextInput,
            "camera_make": forms.TextInput,
            "camera_model": forms.TextInput,
            "format": forms.Select(attrs={"id": "format-choice"}),
            "description": forms.TextInput,
            "year_taken": forms.DateInput,
            "lens_make": forms.TextInput,
            "lens_model": forms.TextInput,
            "focal_length": forms.TextInput,
            "picture": forms.ClearableFileInput,
        }
