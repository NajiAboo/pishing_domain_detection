import os
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster  import KMeans
from kneed import KneeLocator
from src.util.common import save_json, save_model
from src.config.configuration import DataIngestionConfig, DataPreprcessingConfig

class DataPreprocessing:
    def __init__(self,data_ingestion_config: DataIngestionConfig,
                    data_preprocessing_config: DataPreprcessingConfig
                 ) -> None:
        self.data_ingestion_config = data_ingestion_config
        self.data_preprocessing_config = data_preprocessing_config
        print(f"type {type(self.data_preprocessing_config.cluster_number_path)}")
    
    def __get_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_ingestion_config.local_data_file)
        return df
    
    def __split_dependent_independent(self, df: pd.DataFrame) -> tuple([pd.DataFrame, pd.Series]):
        X = df.iloc[:,:-1]
        y = df.iloc[:,-1]
        return X,y
    
    def __calculate_wcss(self, data:pd.DataFrame, max_cluster:int):
        wcss = []
        for cluster_index in range(1, max_cluster):
            kmeans = KMeans(n_clusters=cluster_index, init="k-means++", random_state=42)
            kmeans.fit(data)
            wcss.append(kmeans.inertia_)
        return wcss
    
    def __save_elbow_plot(self, wcss:list, max_cluster:int) -> None:
        plt.plot(range(1,max_cluster),wcss)
        plt.title("The Elbow Method")
        plt.xlabel("Number of Clusters")
        plt.ylabel("WCSS")
        plt.savefig(self.data_preprocessing_config.elbow_file_path)
        
    def __get_k(self, wcss:list, max_cluster:int) -> int:
        number_cluster = KneeLocator(range(1, max_cluster), wcss, curve="convex", direction="decreasing")
        return number_cluster.knee
    
    def __save_k(self, number_cluster:int) -> None:
        data = dict([("number_cluster", str(number_cluster) )])
        save_json(self.data_preprocessing_config.cluster_number_path, data)
    
    
    def __get_cluster_of_each_data(self, X: pd.DataFrame, number_cluster: int) -> tuple([pd.DataFrame,KMeans]) :
        kmean = KMeans(n_clusters=number_cluster, init="k-means++", random_state=42)
        y_mean = kmean.fit_predict(X)
        X["cluster"] = y_mean
        return X, kmean
    
    def __save_model(self, kmeans: KMeans):
       save_model(kmeans, self.data_preprocessing_config.cluster_model_path)
       pass
        
    def __divide_and_save_cluster(self,X: pd.DataFrame, y: pd.Series, number_cluster: int) -> None:
        X_modified, kmean = self.__get_cluster_of_each_data(X, number_cluster=number_cluster)
        X_modified["label"] = y
        X_modified.to_csv(self.data_preprocessing_config.clustered_data)      
        self.__save_model(kmeans=kmean)
        
        
    
    def start_data_preprocessing(self):
        # Fetch data 
        df = self.__get_data()
        
        # Split into dependent and independent
        X,y = self.__split_dependent_independent(df=df)
        wcss = self.__calculate_wcss(X, 11)
        self.__save_elbow_plot(wcss=wcss, max_cluster=11)
        
        # Find the K 
        cluster_count = self.__get_k(wcss=wcss, max_cluster=11)
        print(f"Number of cluster {cluster_count}")
       
        self.__save_k(number_cluster=cluster_count)
        self.__divide_and_save_cluster(X=X, y=y,number_cluster=cluster_count)