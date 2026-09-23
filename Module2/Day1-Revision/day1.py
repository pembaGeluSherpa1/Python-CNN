# %%
import pandas as pd # for dataframe/scripts
import numpy as np # numerical computation
import matplotlib.pyplot as plt # visualization
import seaborn as sns # visualization

from sklearn.preprocessing import OneHotEncoder # preprocessing
from sklearn.model_selection import train_test_split # model training
from sklearn.metrics import mean_squared_error, r2_score # for evaluation (accuracy)

from sklearn.linear_model import LinearRegression 
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV # model selection

import joblib # to generate .pkl file
import warnings
warnings.filterwarnings(action = 'ignore')

from pathlib import Path

# %%
car_df = pd.read_csv("cardekho_dataset.csv")
car_df.head()

# %%
car_df.shape

# %%
car_df.info()

# %%
car_df['brand'].value_counts().head(10)

# %%
car_df['car_name'].value_counts().head(20)

# %%
ax = sns.countplot(data=car_df, x = "vehicle_age")
plt.xticks()
for b in ax.containers:
    ax.bar_label(b)
plt.show()

# %%
car_df[car_df["km_driven"] > 50000].count()

# %%
car_df.drop(columns = ["Unnamed: 0"], inplace=True )

# %%
car_df.head()

# %%
# 1500 km < gureko 10 < year

car_df.columns

# %%
car_df[(car_df["km_driven"]<1500) & (car_df["vehicle_age"]<10)].shape[0]

# %% [markdown]
# #### Data Cleaning

# %%
# remove unrealistic records

cleaned_car_df = car_df[(car_df["km_driven"]<500000) &
                        (car_df["vehicle_age"]<=15)]

# %%


# %%
cleaned_car_df.head()

# %%
# correct fuel type

cleaned_car_df["fuel_type"].unique()

# %%
cleaned_car_df["fuel_type"].replace(
    "Electric",
    "Hybrid",
    inplace=True
)

# %%
# transmission analysis 
cleaned_car_df["transmission_type"].value_counts()

# %%
sns.histplot(data=cleaned_car_df, 
             x="engine",
             bins = 50)
plt.show()

# %%
sns.histplot(data=cleaned_car_df, 
             x= "mileage",
             bins = 50)
plt.show()

# %%
cleaned_car_df["seats"].value_counts()

# %%
cleaned_car_df.loc[cleaned_car_df["car_name"] == "Nissan Kicks", "seats"] = 5

# %%
cleaned_car_df["seats"].value_counts()

# %%
# convert price to lakhs 

cleaned_car_df["selling_price_in_lakhs"] = (cleaned_car_df["selling_price"]/100000)

cleaned_car_df.drop(["selling_price"],
                    axis=1,
                    inplace=True)

# %%
cleaned_car_df.head()

# %%
# price distribution analysis in lakhs

sns.histplot(data=cleaned_car_df,
             x="selling_price_in_lakhs",
             bins = 50)
plt.show()

# %%
cleaned_car_df["vehicle_age"].value_counts()

# %%



