import joblib
import numpy as np

from parts.simple import recipeClass


# load the model from disk
waffleness_pca = joblib.load('data/waffleness.model')


def get_waffleness(R: recipeClass, model=waffleness_pca):

    selected_ingredients = ('flour', 'water', 'baking', 'butter',
                            'egg', 'milk', 'oil', 'salt', 'sugar', 'vanilla')
    n_selected_ingredients = len(selected_ingredients)

    def _name_mapping(name: str):
        for i in selected_ingredients:
            if i in name.lower():
                return i
        return "unselected"

    ingredients = R.flour + R.dry + R.wet + R.mix + R.toppings

    features = np.zeros(n_selected_ingredients, dtype=np.float)

    for ingr in ingredients:

        _name = _name_mapping(ingr.name)
        _amount = ingr.amount
        if _name == 'egg':
            _amount /= 250

        if _name != "unselected":
            idx = selected_ingredients.index(_name)
            features[idx] += _amount

    features /= features[0]

    X = np.expand_dims(features, axis=0)
    score = model.score(X)

    return score


def waffleness_estimator(R: recipeClass, threshold=10):
    score = get_waffleness(R)
    return True if score > threshold else False
