# from data.dataAnalysis import show_distribution_graph
#
# from model.modelSelection import selection_model
#
#
# def build(settings_csv, settings_variables, settings_models):
#     #DataProcessing
#
#     csvdata = create_dataset(settings_csv['pathcsv'], settings_csv['delimiter'], settings_csv['subset_columns'])
#
#     csvdata = create_data_variables(csvdata, settings_csv['data'])
#
#     #csvdata.drop(csvdata[(csvdata[settings_csv['target']] > 17000)].index, inplace=True) #droppate 12 righe
#     #csvdata.drop(csvdata[(csvdata[settings_csv['target']] < 3000)].index, inplace=True) #droppate 3 righe
#
#     df = csvdata
#
#     settings_variables['media_numeric'] = settings_variables['medias']
#
#     # Aggregate variables in Numerical and Categorical
#     settings_variables['numerical'] = settings_variables['media_numeric'] + settings_variables['general_numeric']
#     settings_variables['categorical'] = settings_variables['seasonal_categorical'] + settings_variables['general_categorical']
#
#     # Sum everything up in one array
#     settings_variables['all_features'] = settings_variables['categorical'] + settings_variables['numerical']
#
#     #correlation_pairplots(settings_variables['medias'], df, settings_csv['target'])
#
#     #iterative_pair_plotting(df, 5)
#
#     #print(df.corr())
#
#     show_distribution_graph(df, settings_csv['data'], settings_csv['target'], settings_variables['medias'])
#
#     # Define X as all variables except the output variable - Y is the output variable
#     X = df[settings_variables['all_features']]
#     y = df[settings_csv['target']]
#
#
#     selection_model(df, settings_variables['medias'], settings_variables['organic'], X, y, settings_models)
