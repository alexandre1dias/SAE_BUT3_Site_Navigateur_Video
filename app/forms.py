# forms.py
from django import forms

class CreateVideoForm(forms.Form):
    url = forms.CharField(label="Lien de la vidéo", max_length=255)
    
class AddAnswerForm(forms.Form):
    question = forms.ModelChoiceField(queryset=None, label="Question", required=True)  # queryset sera défini dans la vue
    artist = forms.ModelChoiceField(queryset=None, label="Artiste", required=True)    # queryset sera défini dans la vue
    timecode = forms.IntegerField(label="Timecode", required=True)
    content = forms.CharField(label="Réponse", widget=forms.Textarea, required=True)
    