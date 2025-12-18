from fastapi import FastAPI
from feast import FeatureStore

app = FastAPI()

store = FeatureStore(repo_path="/repo")

@app.get("/health")
def health():
    """
    Endpoint de santé simple pour vérifier que l'API est en ligne.
    """
    return {"status": "ok"}


@app.get("/features/{user_id}")
def get_features(user_id: str):
    """
    Récupère un sous-ensemble de features Feast pour un utilisateur donné.
    """
    features = [
        "subs_profile_fv:months_active",
        "subs_profile_fv:monthly_fee",
        "subs_profile_fv:paperless_billing",
    ]

    feature_dict = store.get_online_features(
        features=features,
        entity_rows=[{"user_id": user_id}],
    ).to_dict()

    # Conversion du format Feast (liste par feature) vers un format simple
    simple_features = {
        name: values[0] for name, values in feature_dict.items()
    }

    return {
        "user_id": user_id,
        "features": simple_features,
    }
