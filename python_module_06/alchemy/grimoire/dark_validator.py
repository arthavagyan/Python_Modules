from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    ingredients_list = ingredients.split(", ")
    for ingredient in ingredients_list:
        if ingredient.lower() in dark_spell_allowed_ingredients():
            return "VALID"
    return "INVALID"
