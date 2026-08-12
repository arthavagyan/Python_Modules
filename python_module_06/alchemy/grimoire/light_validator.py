def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients
    ingredients_list = ingredients.split(", ")
    for ingredient in ingredients_list:
        if ingredient.lower() in light_spell_allowed_ingredients():
            return "VALID"
    return "INVALID"
