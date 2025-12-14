import re

def _extract_number(text):
    nums = re.findall(r"\d+", text.replace(" ", ""))
    return int(nums[0]) if nums else None

def evaluate_offer_text(user_offer_text: str, scenario):
    """
    Donne un score 0-10 pour la qualité de l'offre utilisateur par rapport au prix affiché.
    (Plus l'offre est proche du prix affiché, meilleur le score.)
    """
    offer = _extract_number(user_offer_text)
    if offer is None:
        return {"score": 0, "raison": "Aucune offre chiffrée détectée."}

    prix = scenario.get("prix", 0)
    min_price = scenario.get("prix_min", 0)

    # Score basique
    if offer >= prix:
        score = 10
    elif offer <= min_price:
        score = 2
    else:
        # linéaire entre plancher->2 et prix->10
        score = int(2 + (offer - min_price) / max(1, (prix - min_price)) * 8)
        score = max(2, min(10, score))

    return {"score": score, "offer": offer, "prix": prix, "prix_min": min_price}