from relevanceai.http_client import Client, Dataset, Clusterer


def test_dataset_api_kmeans_centroids_properties(
    test_client: Client, test_dataset_df: Dataset
):
    from sklearn.cluster import KMeans

    vector_field = "sample_1_vector_"
    alias = "test_alias"
    from relevanceai.clusterer import KMeansModel

    model = KMeansModel()

    clusterer: Clusterer = test_client.Clusterer(model=model, alias=alias)
    clusterer.fit(dataset=test_dataset_df, vector_fields=[vector_field])

    assert f"_cluster_.{vector_field}.{alias}" in test_dataset_df.schema

    centroids = clusterer.centroids
    assert len(centroids) > 0
