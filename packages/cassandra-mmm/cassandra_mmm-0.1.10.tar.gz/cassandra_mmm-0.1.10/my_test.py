from data.dataProcessing.clean_and_format import create_data_columns
from src.cassandra.data.dataAnalysis.correlation import show_saturation_curves, show_relationship_between_variables
from src.cassandra.data.dataAnalysis.plot import show_target_vs_media_spent_graph
from src.cassandra.data.dataProcessing.clean_and_format import create_dataset
from src.cassandra.model.deepLearning import deepLearning
from src.cassandra.model.linear import linear
from src.cassandra.model.logLinear import logLinear
from src.cassandra.model.ridge import ridge

csv_data = create_dataset('D:/workspace_cassandra/mmm/spedire/dataset-spedire-07-01-22.csv')
csv_data = create_data_columns(csv_data, 'ordine_data')

csv_data.drop(csv_data[(csv_data['revenue'] > 17000)].index, inplace=True) #droppate 12 righe
csv_data.drop(csv_data[(csv_data['revenue'] < 3000)].index, inplace=True) #droppate 3 righe

df = csv_data

medias = [col for col in df.columns if 'spent' in col]

organic = ['bing_organico', 'google_organico', 'referral', 'email_sessioni', 'cambio_eur_dollaro', 'ios_14', 'Offerte', 'mon','tue','wed','thu','fri','sat','sun', 'month','year']

seasonal_categorical = ['month', 'year', 'mon','tue','wed','thu','fri','sat','sun']

media_numeric = medias

general_categorical= ['ios_14', 'Offerte']

general_numeric = ['bing_organico', 'google_organico', 'referral', 'email_sessioni', 'cambio_eur_dollaro']

# Aggregate variables in Numerical and Categorical
numerical = media_numeric + general_numeric
categorical = seasonal_categorical + general_categorical

# Sum everything up in one array
all_features = categorical + numerical

#show_saturation_curves(medias, df, 'revenue')

#show_relationship_between_variables(df, 5)

#print(df.corr())

#show_target_vs_media_spent_graph(df, 'ordine_data', 'revenue', medias)


# Define X as all variables except the output variable - Y is the output variable
X = df[all_features]
y = df['revenue']

result_linear, model_linear = linear(df, medias, organic, X, y, 'revenue', 'Linear', ['accuracy', 'nrmse', 'mape'])
result_loglinear, model_loglinear = logLinear(df, medias, organic, X, y, 'revenue', 'LogLinear', ['accuracy', 'nrmse', 'mape'])
result_ridge, model_ridge = ridge(df, medias, organic, X, y, 'revenue', 'Ridge', metric = ['accuracy', 'nrmse', 'mape'])
result_deep, model_deep = deepLearning(df, X, y, 'revenue', 'DeepLearning', ['accuracy', 'nrmse', 'mape'])

