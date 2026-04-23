"""
knapsack_01.py - 0-1 Knapsack Problem Logic
Author Role: GA Core Developer
CS212 Artificial Intelligence
"""

import random

def create_chromosome(num_items):
    return [random.randint(0, 1) for _ in range(num_items)]

def fitness_function(items, chromosome, capacity):
    total_weight = 0.0
    total_value = 0.0

    for gene, item in zip(chromosome, items):
        if gene == 1:
            total_weight += item["weight"]
            total_value += item["value"]

    
    if total_weight <= capacity:
        return total_value

    excess = total_weight - capacity
    penalty = excess * (total_value / total_weight if total_weight > 0 else 1)

    return total_value - penalty * 2

def crossover(parent_a, parent_b):
    if len(parent_a) <= 1:
        return parent_a[:], parent_b[:]

    point = random.randint(1, len(parent_a) - 1)

    child_a = parent_a[:point] + parent_b[point:]
    child_b = parent_b[:point] + parent_a[point:]

    return child_a, child_b

def mutation(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

def decode_solution(chromosome, items):
    selected = []
    total_weight = 0.0
    total_value = 0.0

    for gene, item in zip(chromosome, items):
        if gene == 1:
            selected.append({
                "name": item["name"],
                "weight": item["weight"],
                "value": item["value"],
                "quantity": 1,
            })
            total_weight += item["weight"]
            total_value += item["value"]

    return {
        "selected_items": selected,
        "total_weight": total_weight,
        "total_value": total_value,
        "quantities": chromosome[:],
    }