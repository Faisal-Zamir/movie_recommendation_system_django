import os
import joblib
from django.conf import settings
from django import forms

# Construct full path to the pkl file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # this points to forms.py folder
pkl_path = os.path.join(BASE_DIR, "ML_Files", "movie_data.pkl")  # adjust folder if needed

# Load movie data
final_df = joblib.load(pkl_path)

MOVIE_CHOICES = [(title, title) for title in final_df['title'].tolist()]


class MovieRecommendationForm(forms.Form):
    movie_title = forms.ChoiceField(
        choices=MOVIE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'movieTitle'
            }
        ),
        label=""
    )
