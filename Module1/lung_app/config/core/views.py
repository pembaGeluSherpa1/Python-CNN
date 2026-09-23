from django.shortcuts import render

from .forms import LungCancerForm

from .ml_service import predict_lung_cancer



def home(request):

   prediction = None

   form = LungCancerForm()


   if request.method == "POST":

       form = LungCancerForm(request.POST)


       if form.is_valid():

           cleaned_data = form.cleaned_data


           input_data = {

               "GENDER": int(cleaned_data["GENDER"]),

               "AGE": int(cleaned_data["AGE"]),

               "SMOKING": int(cleaned_data["SMOKING"]),

               "YELLOW_FINGERS": int(cleaned_data["YELLOW_FINGERS"]),

               "ANXIETY": int(cleaned_data["ANXIETY"]),

               "PEER_PRESSURE": int(cleaned_data["PEER_PRESSURE"]),

               "CHRONIC_DISEASE": int(cleaned_data["CHRONIC_DISEASE"]),

               "FATIGUE": int(cleaned_data["FATIGUE"]),

               "ALLERGY": int(cleaned_data["ALLERGY"]),

               "WHEEZING": int(cleaned_data["WHEEZING"]),

               "ALCOHOL_CONSUMING": int(cleaned_data["ALCOHOL_CONSUMING"]),

               "COUGHING": int(cleaned_data["COUGHING"]),

               "SHORTNESS_OF_BREATH": int(cleaned_data["SHORTNESS_OF_BREATH"]),

           }


           prediction = predict_lung_cancer(input_data)


   return render(request, "predictor/index.html", {

       "form": form,

       "prediction": prediction

   })