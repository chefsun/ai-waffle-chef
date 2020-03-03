from parts.simple import generate_recipe, ingredientClass, recipeClass
from parts.classify import classify
from parts.w2vChef import ingredientIdeas, wordcheck
from parts.amount import get_amount
import gensim
import json
import sys
import random
import logging

def cook(inspiration, model, all_recipes):
    new_ingredients = []
    print("You want me to make a " + inspiration + " waffle?")
    # additional_keywd = random.choice(["butter","meal","bake", "ingredients", "flour"])
    flour_ideas = ingredientIdeas(model, [inspiration, "flour"], [])
    butter_ideas = ingredientIdeas(model, [inspiration, "butter"], [])
    sugar_ideas = ingredientIdeas(model, [inspiration, "sugar"], [])
    ingredient_ideas = ingredientIdeas(model, [inspiration, "ingredient"], [])
    meal_ideas = ingredientIdeas(model, [inspiration, "meal"], [])
    bake_ideas = ingredientIdeas(model, [inspiration, "bake"], [])
    spice_ideas = ingredientIdeas(model, [inspiration, "spice"], [])
    ideas = flour_ideas + butter_ideas + sugar_ideas + ingredient_ideas + meal_ideas + bake_ideas + spice_ideas
    ideas = set(ideas)
    # ideas = ingredientIdeas(model, [inspiration, additional_keywd], [])
    possibilities = []
    for idea in ideas:
        idea = idea[0].replace('_', ' ').lower()
        possibilities.append(idea)
        pieces = idea.split(" ", 1)
        if len(pieces) == 2:
            if pieces[0] not in possibilities:
                possibilities.append(pieces[0])
            if pieces[1] not in possibilities:
                possibilities.append(pieces[1])
        print(idea)
    possibilities = set(possibilities)
    print(possibilities)
    for possibility in possibilities:
        classed = classify(possibility)
        if not classed: 
            classed = classify(possibility + "s")
        if not classed:
            classed = classify(possibility[:-1])
        if classed:
            a = int(get_amount(possibility))
            if a > 0:
                print(classed)
                print(possibility)
                new_ingredient = ingredientClass()
                new_ingredient.define_me(possibility, a, classed)
                new_ingredients.append(new_ingredient)
        else:
            pass
            #print("no")
    return new_ingredients

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = gensim.models.KeyedVectors.load_word2vec_format('J:\ML\GoogleNews-vectors-negative300.bin', binary=True)
f = open('data/layer1.json', 'r')
all_recipies = f.read().splitlines()
f.close()

cups = 8
multiplier = cups / 2.3
while True:
    print("What kinds of waffle would you like to eat?")
    while True:
        inspiration = input(">> ")
        if inspiration.lower() == "no":
            print("OK, see you!")
            sys.exit()
        if wordcheck(model,inspiration):
            break
    recipe = recipeClass()
    initial_ingredients = generate_recipe()
    new_ingredients = cook(inspiration, model, all_recipies)
    print("")
    print(inspiration + " waffle recipe")
    print("---------------------------------------")
    for i in initial_ingredients:
        i.multiply(multiplier)
        recipe.add_ingredient(i)
    for i in new_ingredients:
        i.multiply(multiplier)
        recipe.add_ingredient(i)
    recipe.update_amounts()
    recipe.print_ingredients()
    print('')
    print(recipe.print_recipe())
    print("---------------------------------------")
    