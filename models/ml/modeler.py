import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler


def get_and_prepare_data(link="https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/strokes.csv"):
    """
    Retrieve data from the `link`
    link: a web link to get data for model training
    default: https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/strokes.csv
    """
    df = pd.read_csv(link, sep=",", index_col="id")

    return df


def create_logistic_regression_model(
        link="https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/strokes.csv"):
    """
    Create a logistic regression model using data from a web link
    Parameters:
    link ==> a web link holding training data
    """

    data = get_and_prepare_data(link)
    X = data.drop(['stroke'], axis=1)
    y = data['stroke']
    categorical_columns = ['ever_married', 'Residence_type', 'hypertension', 'heart_disease', 'work_type',
                           'smoking_status', 'gender']
    numerical_columns = ['age', 'bmi', 'avg_glucose_level']
    numeric_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", RobustScaler())])

    # Pré-traitement
    preprocessor = ColumnTransformer(
        transformers=[('categories', OneHotEncoder(handle_unknown="ignore"), categorical_columns),
                      ('numerics', numeric_transformer, numerical_columns)])

    classifier = Pipeline(steps=[("preprocessor", preprocessor), (
        "classifier", LogisticRegression(solver="newton-cg", C=5.0, max_iter=100, tol=0.5, class_weight='balanced'))])

    # Séparation des jeux de données d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=422)

    # Entraînement et sauvegarde du modèle
    classifier.fit(X, y)
    dump(classifier, "./stroke_model_lr.joblib")


def create_random_forest_model(link="https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/strokes.csv"):
    """
    Create a random forest classifier using data from a web link
    Parameters:
    :link ==> a web link holding training data
    """
    data = get_and_prepare_data(link)
    X = data.drop(['stroke'], axis=1)
    y = data['stroke']

    categorical_columns = ['ever_married', 'Residence_type', 'hypertension', 'heart_disease', 'work_type',
                           'smoking_status', 'gender']
    numerical_columns = ['age', 'bmi', 'avg_glucose_level']
    numeric_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", RobustScaler())])

    preprocessor = ColumnTransformer(
        transformers=[('categories', OneHotEncoder(handle_unknown="ignore"), categorical_columns),
                      ('numerics', numeric_transformer, numerical_columns)])

    classifier = Pipeline(steps=[("preprocessor", preprocessor), (
        "classifier", RandomForestClassifier(criterion='gini', n_estimators=100, max_depth=5, random_state=33))])

    # Entraînement et sauvegarde du modèle
    classifier.fit(X, y)
    dump(classifier, "./stroke_model_rf.joblib")


# First execution: decomment to create a first version of the model
if __name__ == "__main__":
    create_logistic_regression_model()
    create_random_forest_model()
