import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import Ridge,Lasso ,RidgeCV,LassoCV , ElasticNet , ElasticNetCV,LinearRegression
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_profiling import ProfileReport
from custom_logger import CustomLogger

class LinearRegressionTask:
    log = CustomLogger.log()

    def __init__(self, df):
        """
        Intializing with dataframe
        """
        try:
            if isinstance(df, pd.core.frame.DataFrame):
                self.df = df
                self.log.info("pandas dataframe is initialized")
            else:
                self.log.error("Raising exception since pandas dataframe is not passed")
                raise Exception(f"You have not entered a pandas dataframe: {df}")
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def get_info(self):
        """
        Return DataFrame info()
        """
        self.log.info("Returning dataframe info()")
        return self.df.info()

    def get_desc(self):
        """
        Return DataFrame describe()
        """
        self.log.info("Returning dataframe describe()")
        return self.df.describe()

    def get_profile_report(self):
        """
        Return DataFrame profile report()
        """
        try:
            self.log.info("Returning dataframe profile report()")
            #prof = pandas_profiling.ProfileReport(df=df)
            #prof.to_file('pandas_profile_test.html')
            prof = ProfileReport(self.df)
            prof.to_file('pandas_profile_report.html')
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def handle_null(self):
        """
        This method will identify the columns with null values and
        fill with its mean value
        """
        try:
            null_columns = self.df.columns[self.df.isnull().any()]
            self.log.info(f"null values found in columns: {null_columns}")
            for col in null_columns:
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            self.log.info(f"null values filled with the mean in columns: {null_columns}")
            return null_columns
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def drop_column(self,*col):
        """
        This method will identify the columns with null values and
        fill with its mean value
        """
        try:
            self.df.drop(columns=[*col],inplace=True)
            self.log.info(f"Column: {col} dropped from the dataframe")
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def normalize_data(self, X):
        """
        This method will return the standard normal distribution of the features
        """
        try:
            scaler = StandardScaler()
            arr = scaler.fit_transform(X)
            self.log.info(f"Returning standard scaler of columns: {X.columns}")
            return arr
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def get_vif(self, arr, X):
        """
        This method will return the vif/multicolinearity values for all the features
        """
        try:
            vif_df = pd.DataFrame()
            vif_df['vif'] = [variance_inflation_factor(arr, i) for i in range(arr.shape[1])]
            vif_df['feature'] = X.columns
            self.log.info(f"Returning vif/multicolinearity values of columns: {X.columns}")
            return vif_df
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def get_train_test_split(self, arr, y, test_size= 0.2, random_state = 345):
        """
        This method will return the x_train,x_test,y_train,y_test values
        """
        try:
            x_train,x_test,y_train,y_test = train_test_split(arr, y, test_size= test_size,
                                                             random_state = random_state)
            self.log.info("Returning x_train,x_test,y_train,y_test values")
            return x_train,x_test,y_train,y_test
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def get_x(self, cols):
        """
        Return Independent Variables
        """
        try:
            if isinstance(cols, (list,pd.core.indexes.base.Index)):
                self.log.info(f"Returning dataframe with Independent Variables : {cols}")
                return self.df[cols]
            else:
                self.log.error(f"Raising exception since list object is not passed: {cols}")
                raise Exception(f"You have not entered list in independent variables: {cols}")
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def get_y(self, y):
        """
        Return dependent Variables
        """
        try:
            if isinstance(y, str) and y in self.df.columns:
                self.log.info(f"Returning dependent Variable data: {y}")
                return self.df[y]
            else:
                self.log.error(f"Raising exception since valid y column is not passed: {y}")
                raise Exception(f"You have not entered valid y column: {y}")
        except Exception as e:
            print(e)
            self.log.exception(str(e))


    def type_map(self, s):
        """
        Mapping integer values to categorical column
        """
        if s == 'L':
            return 0
        if s == 'M':
            return 1
        if s == 'H':
            return 2
        return -1

    def format_cat_column(self, col):
        """
        Format Categorical column, append to dataframe &
        Return column name
        """
        try:
            if isinstance(col, str) and col in self.df.columns:
                new_col = col + "_new"
                self.df[new_col] = self.df[col].apply(lambda x: self.type_map(x))
                self.log.info(f"Returning New Column: {new_col}")
                return new_col
            else:
                self.log.error(f"Raising exception since valid col column is not passed: {col}")
                raise Exception(f"You have not entered valid col column: {col}")
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def build_linear_regression_model(self, X, y):
        """
        This method will build a linear regression model
        """
        try:
            self.log.info("Building linear regression model")
            linear = LinearRegression()
            linear.fit(X, y)
            return linear
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def build_lasso_model(self, X, y, cv = 5, max_iter=1000000, alphas = None):
        """
        This method will build a lasso model
        """
        try:
            self.log.info("Building lasso linear regression model")
            lassocv = LassoCV(alphas=alphas, cv=cv, max_iter=max_iter, normalize=True)
            lassocv.fit(X, y)
            lasso = Lasso(alpha=lassocv.alpha_)
            lasso.fit(X, y)
            return lasso, lassocv
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def build_ridge_model(self, X, y, cv = 5, alphas=None):
        """
        This method will build a ridge model
        """
        try:
            self.log.info("Building lasso linear regression model")
            ridgecv = RidgeCV(alphas=alphas, cv=cv, normalize=True)
            ridgecv.fit(X, y)
            ridge = Ridge(alpha=ridgecv.alpha_)
            ridge.fit(X, y)
            return ridge, ridgecv
        except Exception as e:
            print(e)
            self.log.exception(str(e))


    def build_elasticnet_model(self, X, y, cv = 5, max_iter=1000000, alphas=None ):
        """
        This method will build a elasticnet model
        """
        try:
            self.log.info("Building elastic net linear regression model")
            elasticcv = ElasticNetCV(alphas=alphas, cv=cv, max_iter=max_iter, normalize=True)
            elasticcv.fit(X, y)
            elastic = ElasticNet(alpha=elasticcv.alpha_ , l1_ratio=elasticcv.l1_ratio_)
            elastic.fit(X, y)
            return elastic, elasticcv
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def save_model(self, model, file_name):
        """
        This method will save the model
        """
        try:
            self.log.info(f"Saving linear regression model: {model} to {file_name} file.")
            pickle.dump(model, open(file_name, 'wb'))
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def model_predict(self, model, test):
        """
        This method will predict the result of the model
        """
        try:
            if isinstance(test, (list,np.ndarray)):
                self.log.info("Predicting result for passed test values")
                return model.predict([test])
            else:
                self.log.error(f"Raising exception since valid test data is not passed: {test}")
                raise Exception(f"You have not entered valid test data: {test}")
        except Exception as e:
            print(e)
            self.log.exception(str(e))

    def get_score(self, model, X, y):
        """
        This method will give the model accuracy
        """
        try:
            return model.score(X, y)
        except Exception as e:
            print(e)
            self.log.exception(str(e))