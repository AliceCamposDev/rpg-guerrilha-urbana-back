import math


def clean_dataframe_for_json(df):
    """Limpa um DataFrame pandas para serialização JSON"""
    if df is None:
        return []

    records = df.to_dict(orient="records")

    def clean_nested(obj):
        if isinstance(obj, dict):
            return {k: clean_nested(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_nested(item) for item in obj]
        elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
            return None
        elif isinstance(obj, (int, str, bool)) or obj is None:
            return obj
        else:
            return str(obj)

    return [clean_nested(record) for record in records]
