# from src.cassandra.data import show_prediction_vs_actual_graph_with_error
# from src.cassandra.helper import helper_nevergrad
# from model.deepLearning import deepLearning
# from model.linear import linear
# from model.logLinear import logLinear
# from src.cassandra.model.modelEvaluation.evaluation import show_coefficients
# from model.ridge import ridge
#
#
# def selection_model(df, medias, organic, X, y, settings_models):
#     # funziona
#     if 'linear' in settings_models['model']:
#         result_linear, model_linear = linear(df, medias, organic, X, y, 'Linear', settings_models['linear_metric'])
#         show_prediction_vs_actual_graph_with_error(result_linear, y, result_linear['prediction'], 'ordine_data', 'revenue', 'Linear')
#         if settings_models['linear_coeffs'] == True:
#             show_coefficients(X.columns, model_linear, 'Linear', graph=True)
#
#     # chiedere feadback se funziona
#     elif 'logLinear' in settings_models['model']:
#         result_log_linear, model_log_linear = logLinear(df, medias, organic, X, y, 'Log Linear', settings_models['log_linear_metric'])
#         show_prediction_vs_actual_graph_with_error(result_log_linear, np.log(y), result_log_linear['prediction'], 'ordine_data',
#                                          'revenue', 'Log Linear')
#         if settings_models['log_linear_coeffs'] == True:
#             show_coefficients(X.columns, model_log_linear, 'Log Linear', graph=True)
#
#     # funziona
#     elif 'ridge' in settings_models['model']:
#         result_ridge, model_ridge = ridge(df, medias, organic, X, y, 'Ridge', settings_models['ridge_metric'])
#         show_prediction_vs_actual_graph_with_error(result_ridge, y, result_ridge['prediction'], 'ordine_data', 'revenue', 'Ridge',)
#         if settings_models['ridge_coeffs'] == True:
#             show_coefficients(X.columns, model_ridge, 'Ridge',graph=True)
#
#     # da capire e chiedere feadback se funziona
#     elif 'deepLearning' in settings_models['model']:
#         result_deep_learning, model_deep_learning = deepLearning(df, medias, organic, X, y, 'Deep Learning',
#                                                                  settings_models['deep_learning_metric'])
#         show_prediction_vs_actual_graph_with_error(result_deep_learning, y, result_deep_learning['prediction'], 'ordine_data',
#                                          'revenue', 'Deep Learning')
#         if settings_models['deep_learning_coeffs']:
#             show_coefficients(X.columns, model_deep_learning, 'Deep Learning', graph=True)
#
#     elif 'nevergrad' in settings_models['model']:
#         helper_nevergrad()
#
#     elif 'all' in settings_models['model']:
#     #LINEAR
#         result_linear, model_linear = linear(df, medias, organic, X, y, 'Linear', settings_models['linear_metric'])
#         show_prediction_vs_actual_graph_with_error(result_linear, y, result_linear['prediction'], 'ordine_data', 'revenue',
#                                          'Linear')
#         if settings_models['linear_coeffs'] == True:
#             show_coefficients(X.columns, model_linear, 'Linear', graph=True)
#
#     #LOG LINEAR
#         result_log_linear, model_log_linear = logLinear(df, medias, organic, X, y, 'Log Linear',
#                                                         settings_models['log_linear_metric'])
#         show_prediction_vs_actual_graph_with_error(result_log_linear, np.log(y), result_log_linear['prediction'],
#                                          'ordine_data',
#                                          'revenue', 'Log Linear')
#         if settings_models['log_linear_coeffs'] == True:
#             show_coefficients(X.columns, model_log_linear, 'Log Linear', graph=True)
#     #RIDGE
#         result_ridge, model_ridge = ridge(df, medias, organic, X, y, 'Ridge', settings_models['ridge_metric'])
#         show_prediction_vs_actual_graph_with_error(result_ridge, y, result_ridge['prediction'], 'ordine_data', 'revenue',
#                                          'Ridge', )
#         if settings_models['ridge_coeffs'] == True:
#             show_coefficients(X.columns, model_ridge, 'Ridge', graph=True)
#
#     #DEEP LEARNING
#         result_deep_learning, model_deep_learning = deepLearning(df, medias, organic, X, y, 'Deep Learning',
#                                                                  settings_models['deep_learning_metric'])
#         show_prediction_vs_actual_graph_with_error(result_deep_learning, y, result_deep_learning['prediction'], 'ordine_data',
#                                          'revenue', 'Deep Learning')
#         if settings_models['deep_learning_coeffs']:
#             show_coefficients(X.columns, model_deep_learning, 'Deep Learning', graph=True)
#
#     #NEVERGRAD
#         helper_nevergrad()
