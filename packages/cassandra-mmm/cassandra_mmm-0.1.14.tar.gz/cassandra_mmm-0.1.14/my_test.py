#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from cassandra.data.dataProcessing.clean_and_format import create_data_columns
from cassandra.data.dataAnalysis.correlation import show_saturation_curves, show_relationship_between_variables
from cassandra.data.dataAnalysis.plot import show_target_vs_media_spent_graph, show_prediction_vs_actual_graph
from cassandra.data.dataProcessing.clean_and_format import create_dataset
from cassandra.model.deepLearning import deepLearning
from cassandra.model.linear import linear
from cassandra.model.logLinear import logLinear
from cassandra.model.ridge import ridge
from cassandra.data.featureSelection.ols import ols
from cassandra.data.trasformations.trasformations import saturation, adstock
from cassandra.model.modelEvaluation.evaluation import show_coefficients
from cassandra.model.modelEvaluation.evaluation import show_nrmse, show_mape
import pandas as pd
import nevergrad as ng
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# In[256]:


csv_data = create_dataset('D:/workspace_cassandra/mmm/spedire/dataset-spedire-07-01-22.csv',
                          subset_columns=['ordine_data', 'revenue', 'transazioni', 'google_search_spent',
                                          'google_performance_max_spent', 'google_display_spent',
                                          'fb_retargeting_spent', 'fb_prospecting_spent', 'bing_spent', 'bing_organico',
                                          'google_organico', 'referral', 'email_sessioni', 'cambio_eur_dollaro',
                                          'ios_14', 'Offerte'])
csv_data = create_data_columns(csv_data, 'ordine_data')

csv_data.drop(csv_data[(csv_data['revenue'] > 17000)].index, inplace=True)  # droppate 12 righe
csv_data.drop(csv_data[(csv_data['revenue'] < 3000)].index, inplace=True)  # droppate 3 righe

df = csv_data
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 10)
pd.set_option("display.max_columns", 10)
df

# In[257]:


medias = [col for col in df.columns if 'spent' in col]
# medias.remove("google_discovery_spent")

show_saturation_curves(medias, df, 'revenue')

# In[258]:


# show_relationship_between_variables(df, 5)


# In[259]:


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
df.corr()

# In[260]:


show_target_vs_media_spent_graph(df, 'ordine_data', 'revenue', medias)

# In[261]:


organic = ['bing_organico', 'google_organico', 'referral', 'email_sessioni', 'cambio_eur_dollaro', 'ios_14', 'Offerte',
           'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'month', 'year']

seasonal_categorical = ['month', 'year', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

media_numeric = medias

general_categorical = ['ios_14', 'Offerte']

general_numeric = ['bing_organico', 'google_organico', 'referral', 'email_sessioni', 'cambio_eur_dollaro']

# Aggregate variables in Numerical and Categorical
numerical = media_numeric + general_numeric
categorical = seasonal_categorical + general_categorical

# Sum everything up in one array
all_features = categorical + numerical

df.fillna(0, inplace=True)

X = df[all_features]
y = df['revenue']

result_ols, model_ols = ols(X, y)

# In[262]:


result_linear, model_linear = linear(df, medias, organic, X, y, 'revenue', 'Linear', ['accuracy', 'nrmse', 'mape'])

# In[263]:


# result_loglinear, model_loglinear = logLinear(df, medias, organic, X, y, 'revenue', 'LogLinear', ['accuracy', 'nrmse', 'mape'])


# In[264]:


# result_ridge, model_ridge = ridge(df, medias, organic, X, y, 'revenue', 'Ridge', metric = ['accuracy', 'nrmse', 'mape'])


# In[265]:


# result_deep, model_deep = deepLearning(df, X, y, 'revenue', 'DeepLearning', ['accuracy', 'nrmse', 'mape'])


# In[266]:


new_X = {}


def build_model(google_search_spent_theta, google_search_spent_beta,
                google_performance_max_spent_theta, google_performance_max_spent_beta,
                google_display_spent_theta, google_display_spent_beta,
                fb_retargeting_spent_theta, fb_retargeting_spent_beta,
                fb_prospecting_spent_theta, fb_prospecting_spent_beta,
                bing_spent_theta, bing_spent_beta,
                bing_organico_theta, bing_organico_beta,
                google_organico_theta, google_organico_beta,
                referral_theta, referral_beta,
                email_sessioni_theta, email_sessioni_beta,
                cambio_eur_dollaro_theta, cambio_eur_dollaro_beta,
                month_theta, month_beta,
                year_theta, year_beta,
                mon_theta, mon_beta,
                tue_theta, tue_beta,
                wed_theta, wed_beta,
                thu_theta, thu_beta,
                fri_theta, fri_beta,
                sat_theta, sat_beta,
                sun_theta, sun_beta,
                ios_14_theta, ios_14_beta,
                Offerte_theta, Offerte_beta):
    # ' Transform all media variables and set them in the new Dictionary
    # ' Adstock first and Saturation second
    new_X["google_search_spent"] = saturation(adstock(df["google_search_spent"], google_search_spent_theta),
                                              google_search_spent_beta)
    new_X["google_performance_max_spent"] = saturation(
        adstock(df["google_performance_max_spent"], google_performance_max_spent_theta),
        google_performance_max_spent_beta)
    new_X["google_display_spent"] = saturation(adstock(df["google_display_spent"], google_display_spent_theta),
                                               google_display_spent_beta)
    new_X["fb_retargeting_spent"] = saturation(adstock(df["fb_retargeting_spent"], fb_retargeting_spent_theta),
                                               fb_retargeting_spent_beta)
    new_X["fb_prospecting_spent"] = saturation(adstock(df["fb_prospecting_spent"], fb_prospecting_spent_theta),
                                               fb_prospecting_spent_beta)
    new_X["bing_spent"] = saturation(adstock(df["bing_spent"], bing_spent_theta), bing_spent_beta)
    new_X["bing_organico"] = saturation(adstock(df["bing_organico"], bing_organico_theta), bing_organico_beta)
    new_X["google_organico"] = saturation(adstock(df["google_organico"], google_organico_theta), google_organico_beta)
    new_X["referral"] = saturation(adstock(df["referral"], referral_theta), referral_beta)
    new_X["email_sessioni"] = saturation(adstock(df["email_sessioni"], email_sessioni_theta), email_sessioni_beta)
    new_X["cambio_eur_dollaro"] = saturation(adstock(df["cambio_eur_dollaro"], cambio_eur_dollaro_theta),
                                             cambio_eur_dollaro_beta)
    new_X["month"] = saturation(adstock(df["month"], month_theta), month_beta)
    new_X["year"] = saturation(adstock(df["year"], year_theta), year_beta)
    new_X["mon"] = saturation(adstock(df["mon"], mon_theta), mon_beta)
    new_X["tue"] = saturation(adstock(df["tue"], tue_theta), tue_beta)
    new_X["wed"] = saturation(adstock(df["wed"], wed_theta), wed_beta)
    new_X["thu"] = saturation(adstock(df["thu"], thu_theta), thu_beta)
    new_X["fri"] = saturation(adstock(df["fri"], fri_theta), fri_beta)
    new_X["sat"] = saturation(adstock(df["sat"], sat_theta), sat_beta)
    new_X["sun"] = saturation(adstock(df["sun"], sun_theta), sun_beta)
    new_X["ios_14"] = saturation(adstock(df["ios_14"], ios_14_theta), ios_14_beta)
    new_X["Offerte"] = saturation(adstock(df["Offerte"], Offerte_theta), Offerte_beta)

    # ' Cast Dictionary to DataFrame and append the output column
    new_df = pd.DataFrame.from_dict(new_X)
    new_df = new_df.join(df['revenue'])
    # print(new_df)

    # ' Train test split data
    X = new_df[all_features]
    y = new_df['revenue']

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = LinearRegression()
    model.fit(X_train, y_train)

    result = df
    # print(result)
    result['prediction'] = model.predict(X)

    nrmse_val = show_nrmse(result['revenue'], result['prediction'])
    mape_val = show_mape(result['revenue'], result['prediction'])
    accuracy = model.score(X_test, y_test)

    # print(nrmse_val, mape_val, accuracy)
    return mape_val


# In[267]:


# ' Define the list of hyperparameters to optimize
# ' List must be the same as the ones in the function's definition, same order recommended too
instrum = ng.p.Instrumentation(
    google_search_spent_theta=ng.p.Scalar(lower=0, upper=1),
    google_search_spent_beta=ng.p.Scalar(lower=0, upper=1),

    google_performance_max_spent_theta=ng.p.Scalar(lower=0, upper=1),
    google_performance_max_spent_beta=ng.p.Scalar(lower=0, upper=1),

    google_display_spent_theta=ng.p.Scalar(lower=0, upper=1),
    google_display_spent_beta=ng.p.Scalar(lower=0, upper=1),

    fb_retargeting_spent_theta=ng.p.Scalar(lower=0, upper=1),
    fb_retargeting_spent_beta=ng.p.Scalar(lower=0, upper=1),

    fb_prospecting_spent_theta=ng.p.Scalar(lower=0, upper=1),
    fb_prospecting_spent_beta=ng.p.Scalar(lower=0, upper=1),

    bing_spent_theta=ng.p.Scalar(lower=0, upper=1),
    bing_spent_beta=ng.p.Scalar(lower=0, upper=1),

    bing_organico_theta=ng.p.Scalar(lower=0, upper=1),
    bing_organico_beta=ng.p.Scalar(lower=0, upper=1),

    google_organico_theta=ng.p.Scalar(lower=0, upper=1),
    google_organico_beta=ng.p.Scalar(lower=0, upper=1),

    referral_theta=ng.p.Scalar(lower=0, upper=1),
    referral_beta=ng.p.Scalar(lower=0, upper=1),

    email_sessioni_theta=ng.p.Scalar(lower=0, upper=1),
    email_sessioni_beta=ng.p.Scalar(lower=0, upper=1),

    cambio_eur_dollaro_theta=ng.p.Scalar(lower=0, upper=1),
    cambio_eur_dollaro_beta=ng.p.Scalar(lower=0, upper=1),

    month_theta=ng.p.Scalar(lower=0, upper=1),
    month_beta=ng.p.Scalar(lower=0, upper=1),

    year_theta=ng.p.Scalar(lower=0, upper=1),
    year_beta=ng.p.Scalar(lower=0, upper=1),

    mon_theta=ng.p.Scalar(lower=0, upper=1),
    mon_beta=ng.p.Scalar(lower=0, upper=1),

    tue_theta=ng.p.Scalar(lower=0, upper=1),
    tue_beta=ng.p.Scalar(lower=0, upper=1),

    wed_theta=ng.p.Scalar(lower=0, upper=1),
    wed_beta=ng.p.Scalar(lower=0, upper=1),

    thu_theta=ng.p.Scalar(lower=0, upper=1),
    thu_beta=ng.p.Scalar(lower=0, upper=1),

    fri_theta=ng.p.Scalar(lower=0, upper=1),
    fri_beta=ng.p.Scalar(lower=0, upper=1),

    sat_theta=ng.p.Scalar(lower=0, upper=1),
    sat_beta=ng.p.Scalar(lower=0, upper=1),

    sun_theta=ng.p.Scalar(lower=0, upper=1),
    sun_beta=ng.p.Scalar(lower=0, upper=1),

    ios_14_theta=ng.p.Scalar(lower=0, upper=1),
    ios_14_beta=ng.p.Scalar(lower=0, upper=1),

    Offerte_theta=ng.p.Scalar(lower=0, upper=1),
    Offerte_beta=ng.p.Scalar(lower=0, upper=1)
)

# print(instrum)
# ' Define an Optimizer (use NGOpt as default) and set budget as number of trials (recommended 2500+)
optimizer = ng.optimizers.NGOpt(parametrization=instrum, budget=2500)
# print(optimizer)

# ' Pass the function to minimize
# ' Nevergrad will automatically map Hyperparams
recommendation = optimizer.minimize(build_model)

# ' Results of the optimization are inside the following variable
recommendation.value

# build_model(**recommendation.value[1])
# ' Use the following code to directly use the optimized hyperparams to build you model


# In[268]:


new_X = {}


def build_model(google_search_spent_theta, google_search_spent_beta,
                google_performance_max_spent_theta, google_performance_max_spent_beta,
                google_display_spent_theta, google_display_spent_beta,
                fb_retargeting_spent_theta, fb_retargeting_spent_beta,
                fb_prospecting_spent_theta, fb_prospecting_spent_beta,
                bing_spent_theta, bing_spent_beta,
                bing_organico_theta, bing_organico_beta,
                google_organico_theta, google_organico_beta,
                referral_theta, referral_beta,
                email_sessioni_theta, email_sessioni_beta,
                cambio_eur_dollaro_theta, cambio_eur_dollaro_beta,
                month_theta, month_beta,
                year_theta, year_beta,
                mon_theta, mon_beta,
                tue_theta, tue_beta,
                wed_theta, wed_beta,
                thu_theta, thu_beta,
                fri_theta, fri_beta,
                sat_theta, sat_beta,
                sun_theta, sun_beta,
                ios_14_theta, ios_14_beta,
                Offerte_theta, Offerte_beta):
    # ' Transform all media variables and set them in the new Dictionary
    # ' Adstock first and Saturation second
    new_X["google_search_spent"] = saturation(adstock(df["google_search_spent"], google_search_spent_theta),
                                              google_search_spent_beta)
    new_X["google_performance_max_spent"] = saturation(
        adstock(df["google_performance_max_spent"], google_performance_max_spent_theta),
        google_performance_max_spent_beta)
    new_X["google_display_spent"] = saturation(adstock(df["google_display_spent"], google_display_spent_theta),
                                               google_display_spent_beta)
    new_X["fb_retargeting_spent"] = saturation(adstock(df["fb_retargeting_spent"], fb_retargeting_spent_theta),
                                               fb_retargeting_spent_beta)
    new_X["fb_prospecting_spent"] = saturation(adstock(df["fb_prospecting_spent"], fb_prospecting_spent_theta),
                                               fb_prospecting_spent_beta)
    new_X["bing_spent"] = saturation(adstock(df["bing_spent"], bing_spent_theta), bing_spent_beta)
    new_X["bing_organico"] = saturation(adstock(df["bing_organico"], bing_organico_theta), bing_organico_beta)
    new_X["google_organico"] = saturation(adstock(df["google_organico"], google_organico_theta), google_organico_beta)
    new_X["referral"] = saturation(adstock(df["referral"], referral_theta), referral_beta)
    new_X["email_sessioni"] = saturation(adstock(df["email_sessioni"], email_sessioni_theta), email_sessioni_beta)
    new_X["cambio_eur_dollaro"] = saturation(adstock(df["cambio_eur_dollaro"], cambio_eur_dollaro_theta),
                                             cambio_eur_dollaro_beta)
    new_X["month"] = saturation(adstock(df["month"], month_theta), month_beta)
    new_X["year"] = saturation(adstock(df["year"], year_theta), year_beta)
    new_X["mon"] = saturation(adstock(df["mon"], mon_theta), mon_beta)
    new_X["tue"] = saturation(adstock(df["tue"], tue_theta), tue_beta)
    new_X["wed"] = saturation(adstock(df["wed"], wed_theta), wed_beta)
    new_X["thu"] = saturation(adstock(df["thu"], thu_theta), thu_beta)
    new_X["fri"] = saturation(adstock(df["fri"], fri_theta), fri_beta)
    new_X["sat"] = saturation(adstock(df["sat"], sat_theta), sat_beta)
    new_X["sun"] = saturation(adstock(df["sun"], sun_theta), sun_beta)
    new_X["ios_14"] = saturation(adstock(df["ios_14"], ios_14_theta), ios_14_beta)
    new_X["Offerte"] = saturation(adstock(df["Offerte"], Offerte_theta), Offerte_beta)

    # ' Cast Dictionary to DataFrame and append the output column
    new_df = pd.DataFrame.from_dict(new_X)
    new_df = new_df.join(df['revenue'])

    # ' Train test split data
    X = new_df[all_features]
    y = new_df['revenue']

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = LinearRegression()
    model.fit(X_train, y_train)

    result = df
    result['prediction'] = model.predict(X)

    nrmse_val = show_nrmse(result['revenue'], result['prediction'])
    mape_val = show_mape(result['revenue'], result['prediction'])
    accuracy = model.score(X_test, y_test)

    print(nrmse_val, mape_val, accuracy)
    return mape_val, model, result


# In[269]:


mape_val, model, result = build_model(**recommendation.value[1])
print(mape_val)

# In[271]:


show_prediction_vs_actual_graph(result, 'ordine_data', 'revenue', 'prediction')

# In[278]:


show_coefficients(all_features, model, 'Nevergrad')

# In[ ]:




