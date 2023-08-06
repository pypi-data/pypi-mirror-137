# To extract the values from a correlation matrix to 3 columns data frame. 


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import mean
from numpy import std

from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split,StratifiedKFold,GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, BaggingClassifier, AdaBoostClassifier
from imblearn.over_sampling import SMOTENC, SMOTE
from sklearn.metrics import f1_score, precision_score, recall_score, roc_curve, roc_auc_score, accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, RepeatedStratifiedKFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split,StratifiedKFold,GridSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import make_classification
from sklearn import preprocessing
from xgboost import XGBClassifier
import lightgbm


SEED = 2022

def all_model_statistics(data, outcome = "Attrition"):
    '''A dataset will be analyzed by several models
    and accuracy, recall, specificity, precision, f1 and AUC
    will be returned in a dataframe'''

    X = data.drop(outcome,axis = 1)
    y = np.ravel(data[[outcome]])

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    stratify=y)
    
    res_bayes = bayes_mod(X_train, y_train, X_test, y_test)
    res_log = log_mod(X_train, y_train, X_test, y_test)
    res_kn = kn_mod(X_train, y_train, X_test, y_test)
    # res_svc = svc_mod(X_train, y_train, X_test, y_test)
    res_randfo = ranfo_mod(X_train, y_train, X_test, y_test)
    res_gradbo = gradbo_mod(X_train, y_train, X_test, y_test)
    res_lightgb = lightgb_mod(X_train, y_train, X_test, y_test)
    res_xgb = xgb_mod(X_train, y_train, X_test, y_test)
    
    final_res = pd.DataFrame([res_bayes, res_log, res_kn, res_randfo,
                              res_gradbo, res_lightgb, res_xgb])
   
    final_res = final_res.rename(index={0: 'Naive Bayes', 1: "Log regression", 2: "KNeighbors",
                                        3: "RandomForestClassifier", 
                                        4: "GradientBoostingClassifier", 
                                        5: "Light Gradien Boosting", 6: "XGB"})
    print(final_res)
    return final_res


def print_return_statistics(modelo, X_train, y_train, X_test, y_test, namemodel):
    modelo.fit(X_train, y_train)
    y_pred_nb = modelo.predict(X_test)
    # Print results
    var_accuracty = accuracy_score(y_test, y_pred_nb)
    print('Accuracy score:',var_accuracty)
    var_recall = recall_score(y_test, y_pred_nb)
    print('Recall/Sensitivity:',var_recall)
    var_specificity = recall_score(y_test, y_pred_nb, pos_label= 0)
    print('Specificity:', var_specificity)
    var_precision = precision_score(y_test, y_pred_nb)
    print('Precision:', var_precision)
    var_f1 = f1_score(y_test, y_pred_nb)
    print('F1 score:', var_f1)
    var_roc = roc_auc_score(y_test, y_pred_nb)
    print('ROCAUC score:', var_roc)

    # return a dictionary
    mydict = {}
    # mydict[namemodel + "_acc"] = var_accuracty
    mydict["acc"] = var_accuracty
    mydict["recall"] = var_recall
    mydict["spec"] = var_specificity
    mydict["prec"] = var_precision
    mydict["f1"] = var_f1
    mydict["roc"] = var_roc

    if y_pred_nb.mean() != 0:
        confusion_matrix = pd.crosstab(y_test, y_pred_nb, rownames=['Actual'], colnames=['Predicted'])
        print (confusion_matrix)

        # calculate the fpr and tpr for all thresholds of the classification
        probs = modelo.predict_proba(X_test)
        preds = probs[:,1]
        fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
        roc_auc = metrics.auc(fpr, tpr)

        plt.title('Receiver Operating Characteristic')
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show()

    print(mydict)
    return mydict

def bayes_mod(X_train, y_train,X_test, y_test):
    model_name = "Naive Bayes Classifier"
    nbClassifier = MultinomialNB(alpha = 0.1, class_prior=None, fit_prior=True)
    nb_model = Pipeline(steps=[
        ('classifier', nbClassifier)
    ])
    print(" ------------------  NAIVE BAYES ------------------")

    res2 = print_return_statistics(nb_model, X_train, y_train, X_test, y_test, namemodel = "mod")
    return res2

def log_mod(X_train, y_train,X_test, y_test):
    lrc_model = Pipeline(steps = [("classifier", 
                                   LogisticRegression(solver="liblinear", random_state=0,
                                                                penalty="l1", C = 1, max_iter = 1000))])
                                                                                                                           
    print(" ------------------  LOGISTIC REGRESSION ------------------")

    res2 = print_return_statistics(lrc_model, X_train, y_train, X_test, y_test, namemodel = "mod")
    return res2

def kn_mod(X_train, y_train,X_test, y_test):
    knClassifier = KNeighborsClassifier(n_neighbors=2)

    kn_model = Pipeline(steps=[
        ('classifier', knClassifier)
    ])
    print(" ------------------  KNeighbors ------------------")

    res2 = print_return_statistics(kn_model, X_train, y_train, X_test, y_test, namemodel = "mod")
    return res2

def svc_mod(X_train, y_train,X_test, y_test):
    # kernel{‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’} or callable, default=’rbf’
    svcClassifier = SVC(gamma='auto', kernel = "rbf")

    svc_model = Pipeline(steps=[
        ('classifier', svcClassifier)
    ])
    print(" ------------------  SVC ------------------")

    res2 = print_return_statistics(svc_model, X_train, y_train, X_test, y_test, namemodel = "mod")
    return res2

def ranfo_mod(X_train, y_train,X_test, y_test):
    # kernel{‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’} or callable, default=’rbf’
    randforClassifier = RandomForestClassifier(n_estimators=590, random_state=0)

    randfor_model = Pipeline(steps=[
        ('classifier', randforClassifier)
    ])
    print(" ------------------  RandomForestClassifier ------------------")

    res2 = print_return_statistics(randfor_model, X_train, y_train, X_test, y_test, namemodel = "mod")
    return res2


def xgb_mod(X_train, y_train,X_test, y_test):
    gradboosClassifier = XGBClassifier(learning_rate=0.01,n_estimators=2000,
                                       use_label_encoder=False,random_state=420)

    gradboos_model = Pipeline(steps=[
        ('classifier', gradboosClassifier)
    ])
    print(" ------------------  XGBClassifier ------------------")

    res2 = print_return_statistics(gradboos_model, X_train, y_train, X_test, y_test, namemodel = "mod")
    return res2

def gradbo_mod(X_train, y_train,X_test, y_test):
    gradboosClassifier = GradientBoostingClassifier(n_estimators=100, learning_rate=0.01,
                                                max_depth=10, random_state=0)

    gradboos_model = Pipeline(steps=[
        ('classifier', gradboosClassifier)
    ])
    print(" ------------------  GradientBoostingClassifier ------------------")

    res2 = print_return_statistics(gradboos_model, X_train, y_train, X_test, y_test, namemodel = "mod")
    return res2


def lightgb_mod(X_train, y_train,X_test, y_test):
    gbligthClassifier = LGBMClassifier()

    gbligth_model = Pipeline(steps=[
        ('classifier', gbligthClassifier)
    ])
    print(" ------------------  LGBMClassifier ------------------")

    res2 = print_return_statistics(gbligth_model, X_train, y_train, X_test, y_test, namemodel = "mod")
    return res2

def compare_models(data, model, target):
    
    X_train = data.drop('Attrition', axis=1)
    y_train = data['Attrition']
    
    kont = 0
    # apply StratifiedK-Fold
    skf = StratifiedKFold(n_splits = 5, random_state = SEED, shuffle=True)
    score_train = []
    score_test = []
    score_val = []
    
    for train_index, val_index in skf.split(X_train,y_train):
        print("kont: ", kont)
        print("X_train.shape: ", X_train.shape)
        print("y_train.shape: ", y_train.shape)
        # print("train_index: ", train_index)
        
        # sampled,target = SMOTE().fit_resample(df[cols],df["Attrition"])
        # df6 = pd. concat([sampled[cols], target], axis=1) 
        
        oversample = SMOTE()
        
        # oversample = SMOTENC(categorical_features = cols_cat_idx, random_state=SEED)
        # print(type(train_index))
        # print(cols_cat_idx)
        
        X_train2, y_train2 = oversample.fit_resample(X_train.iloc[train_index], y_train.iloc[train_index])
                      
        # X_train = X_train.iloc[train_index]
        X_val = X_train.iloc[val_index]
        # y_train = y_train.iloc[train_index]
        y_val = y_train.iloc[val_index]
        
        X_train_scaled = X_train2
        X_val_scaled = X_val
        
        print(X_train_scaled.shape)
        print(y_train2.shape)
        print(X_val_scaled.shape)
        print(y_val.shape)
        

        # Apply model
        if str(type(model)) == "<class 'catboost.core.CatBoostClassifier'>":
            model.fit(X_train_scaled, y_train2, verbose=False)
        else:
            model.fit(X_train_scaled, y_train2)
            
        predictions_train = model.predict(X_train_scaled)
        predictions_val = model.predict(X_val_scaled)
        score_train.append(f1_score(y_train2, predictions_train))
        score_val.append(f1_score(y_val, predictions_val))

    avg_train = round(np.mean(score_train),3)
    avg_val = round(np.mean(score_val),3)
    std_train = round(np.std(score_train),2)
    std_val = round(np.std(score_val),2)
    
    print("std_val: ", std_val)
    kont = kont + 1
    return str(avg_train) + '+/-' + str(std_train),str(avg_val) + '+/-' + str(std_val)

def show_results_model(df, data, target, *args):
    """
    Receive an empty dataframe and the different models and call the function avg_score
    """
    
    print("Comienza")
    count = 0
    # for each model passed as argument
    for arg in args:
        # obtain the results provided by avg_score
        print("arg: ", arg)
        avg_train, avg_test = compare_models(data, arg, target)
        print("avg_train: ", avg_train)
        print("avg_test: ", avg_test)
        
        # store the results in the right row
        df.iloc[count] = avg_train, avg_test
        count+=1
    return df


def matrix_to_xy(df, columns=None, reset_index=False):
    import numpy as np
    
    bool_index = np.triu(np.ones(df.shape)).astype(bool)
    xy = (
        df.where(bool_index).stack().reset_index()
        if reset_index
        else df.where(bool_index).stack()
    )
    if reset_index:
        xy.columns = columns or ["row", "col", "val"]
    return xy


def xy_to_matrix(xy):
    import numpy as np
    import pandas as pd
    
    df = xy.pivot(*xy.columns).fillna(0)
    df_vals = df.to_numpy()
    df = pd.DataFrame(
        np.triu(df_vals, 1) + df_vals.T, index=df.index, columns=df.index
    )
    return df
