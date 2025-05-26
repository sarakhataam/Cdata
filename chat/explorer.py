def explore_data(data):
    exploration = {
        "shape": data.shape,
        "columns": data.columns.tolist(),
        "data_types": data.dtypes.astype(str).to_dict(),
        "null_counts": data.isnull().sum().to_dict(),
        "describe_all": data.describe().to_dict(),
        "head": data.head(5).to_dict(orient="records")
    }
    return exploration
