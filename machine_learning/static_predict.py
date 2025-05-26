import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, mean_squared_error, r2_score,
                             accuracy_score, silhouette_score)
from sklearn.linear_model import LogisticRegression, LinearRegression, ElasticNet
from sklearn.ensemble import (RandomForestClassifier, RandomForestRegressor,
                              GradientBoostingClassifier, GradientBoostingRegressor,
                              AdaBoostClassifier, AdaBoostRegressor, ExtraTreesClassifier)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.cluster import KMeans, DBSCAN
import skfuzzy as fuzz

def static_ml(data, target_column, problem_type, model_name, split_ratio=0.2):
    if problem_type in ['Classification', 'Regression']:
        if target_column == "no target":
            raise ValueError(f"{problem_type} requires a target column.")

        X = data.drop(columns=[target_column])
        y = data[target_column]

    elif problem_type == 'Clustering':
        if target_column != "no target":
            X = data.drop(columns=[target_column])
        else:
            X = data.copy()

    else:
        raise ValueError("Unsupported problem type. Choose from 'Classification', 'Regression', or 'Clustering'.")

    X = X.select_dtypes(include=np.number)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = None
    metrics = {}

    if problem_type == 'Classification':
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=split_ratio, random_state=42)

        if model_name == 'LogisticRegression':
            model = LogisticRegression()
        elif model_name == 'RandomForestClassifier':
            model = RandomForestClassifier()
        elif model_name == 'DecisionTreeClassifier':
            model = DecisionTreeClassifier()
        elif model_name == 'SVC':
            model = SVC()
        elif model_name == 'KNeighborsClassifier':
            model = KNeighborsClassifier()
        elif model_name == 'GradientBoostingClassifier':
            model = GradientBoostingClassifier()
        elif model_name == 'AdaBoostClassifier':
            model = AdaBoostClassifier()
        elif model_name == 'ExtraTreesClassifier':
            model = ExtraTreesClassifier()
        else:
            raise ValueError("Unsupported Classification model.")

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        report = classification_report(y_test, y_pred, output_dict=True)
        metrics['classification_report'] = report

    elif problem_type == 'Regression':
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=split_ratio, random_state=42)

        if model_name == 'LinearRegression':
            model = LinearRegression()
        elif model_name == 'RandomForestRegressor':
            model = RandomForestRegressor()
        elif model_name == 'DecisionTreeRegressor':
            model = DecisionTreeRegressor()
        elif model_name == 'SVR':
            model = SVR()
        elif model_name == 'KNeighborsRegressor':
            model = KNeighborsRegressor()
        elif model_name == 'ElasticNet':
            model = ElasticNet()
        elif model_name == 'GradientBoostingRegressor':
            model = GradientBoostingRegressor()
        elif model_name == 'AdaBoostRegressor':
            model = AdaBoostRegressor()
        else:
            raise ValueError("Unsupported Regression model.")

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        acc = accuracy_score(np.round(y_test), np.round(y_pred))  # approximate accuracy

        metrics['mean_squared_error'] = mse
        metrics['r2_score'] = r2
        metrics['approximate_accuracy'] = acc

    elif problem_type == 'Clustering':
        if model_name == 'KMeans':
            model = KMeans(n_clusters=3, random_state=42)
            model.fit(X_scaled)
            labels = model.labels_
        elif model_name == 'DBSCAN':
            model = DBSCAN(eps=0.5, min_samples=5)
            model.fit(X_scaled)
            labels = model.labels_
        elif model_name == 'CMeans':
            cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
                X_scaled.T, c=3, m=2, error=0.005, maxiter=1000, init=None)
            labels = np.argmax(u, axis=0)
            model = {'centers': cntr, 'membership': u}
        else:
            raise ValueError("Unsupported Clustering model.")

        score = silhouette_score(X_scaled, labels)
        metrics['silhouette_score'] = score

    return model, metrics
