from django import forms

class LungCancerForm(forms.Form):
    GENDER = forms.ChoiceField(choices=[(1,"Male"),(0,"Female")])
    AGE = forms.IntegerField(min_value=1,max_value=120)
    SMOKING = forms.ChoiceField(choices=[(1,"Yes"),(0,"No")])
    YellowFingers = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    Anxiety = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    PeerPressure = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    ChronicDisease = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    Fatigue = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    Allergy = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    Wheezing = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    AlcoholConsuming = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    Coughing = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    ShortnessOfBreath = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    SwallowingDifficulty = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
    ChestPain = forms.ChoiceField(choices=[(1,"Yes"), (0,"No")])
