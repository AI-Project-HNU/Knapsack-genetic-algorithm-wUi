"""
utils.py - Utility / Helper Functions
Author Role: Data & Validation Specialist
CS212 Artificial Intelligence - Question #19
"""

import random
import json
import os


def validate_items(items):
    if not items:
        return False,"No items provided. Please add at least one item."
    names_seen =set()
    for i, item in enumerate(items):
      if not item.get("name", "").strip():
        return False, f"Item #{i+1} has an empty name."
      if item["name"] in names_seen:
         return False, f"Duplicate item name: '{item['name']}'. Names must be unique."
      names_seen.add(item["name"])

      try:
         w=float(item["weight"])
         v=float(item["value"])
      except(ValueError, TypeError):
         return False, f"Item '{item['name']}' has non-numeric weight or value."
      if w<=0:
       return False, f"Item '{item['name']}' must have weight > 0."
      if v<=0:
         return False, f"Item '{item['name']}' must have value > 0."
      
      return True, ""
    


def validate_capacity(capacity_str):
   try:
      capacity= float(capacity_str)
      if capacity <=0:
         return False, None, "capacity must be positive"
      return True, capacity, ""
   except(ValueError,TypeError):
      return False, None ,"capacity must be a valid number"
   


def validate_ga_params(params):
   try:
      pop_size=int(params.get("population_size",100))
      generations=int(params.get("generations",200))
      mut_rate=float(params.get("mutation_rate", 0.01))
      cross_rate=float(params.get("crossover_rate", 0.8))
   except(ValueError,TypeError):
      return False, {}, "GA parameters must be numeric"
   
   if not (10<= pop_size<=1000):
      return False,{}, "population size must be between 10 and 1000"
   if not (10<= generations<=2000):
      return False,{}, "generations must be between 10 and 2000"
   if not (0.001<= mut_rate<= 0.5):
      return False,{}, "mutation rate must be between 0.001 and 0.5"
   if not (0.1<= cross_rate<=1.0):
      return False,{}, "crossover rate must be between 0.1 and 1.0"
   

   return True, {
        "population_size": pop_size,
        "generations": generations,
        "mutation_rate": mut_rate,
        "crossover_rate": cross_rate,
    }, ""

ITEM_NAMES = [
    "Laptop", "Camera", "Headphones", "Watch", "Tablet",
    "Phone", "Keyboard", "Mouse", "Monitor", "Speaker",
    "Book", "Notebook", "Pen", "Flashlight", "Compass",
    "Rope", "Knife", "Map", "Water Bottle", "Food Pack",
    "Gold Bar", "Diamond", "Ruby", "Emerald", "Sapphire",
    "Painting", "Sculpture", "Vase", "Coin", "Medal",
    "Jacket", "Boots", "Gloves", "Hat", "Backpack",
    "First Aid Kit", "Radio", "Battery", "Canteen", "Tent",
]
   
   
def generate_random_items(n=10, weight_range=(1,20), value_range=(5,100)):
   n=min(n,len(ITEM_NAMES))
   chosen_names=random.sample(ITEM_NAMES,n)
   items=[]
   for name in chosen_names:
      items.append({
         "name": name,
         "weight": round(random.uniform(*weight_range),1),
         "value": round(random.uniform(*value_range),1)
      })
   return items

