import random
import math 


MAX_COPIES =20



def create_chromosome(num_items,capacity,items):
    chromosome= []
    for item in items:
        if item["weight"] > 0:
            max_copies= min(MAX_COPIES, int(capacity / item["weight"]))
        else:
            max_copies= MAX_COPIES
        chromosome.append(random.randint(0,max(1,max_copies))) 
    return chromosome


def fitness_function(chromosome,items,capacity):
    total_weight=0.0
    total_value=0.0

    for count, item in zip(chromosome, items):
        total_weight+= count * item["weight"]
        total_value+= count * item["value"]

    if total_weight <= capacity:
        return total_value
    else:
        excess= total_weight - capacity
        penalty_rate =(total_value / total_weight) if total_weight > 0 else 1.0
        return total_value - excess * penalty_rate * 3


def crossover(parent_a, parent_b):
    child_a=[]
    child_b=[]
    for gene_a,gene_b in zip(parent_a,parent_b):
        if random.random() < 0.5:
            child_a.append(gene_a)
            child_b.append(gene_b)
        else:
            child_a.append(gene_b)
            child_b.append(gene_a)

    return child_a, child_b


def mutation(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            action = random.choice(["increment","decrement","reset"])
            if action=="increment":
                chromosome[i]=min(MAX_COPIES, chromosome[i]+1)
            elif action == "decrement":
                chromosome[i]=max(0,chromosome[i]-1)
            else:
                chromosome[i]=0

    return chromosome


def decode_solutions(chromosome, items):
    selected=[]
    total_weight=0.0
    total_value=0.0

    for count, item in zip(chromosome,items):
        if count > 0:
            selected.append({
                "name": item["name"],
                "weight": item["weight"],
                "value": item["value"],
                "quantity": count,
            })
            total_weight+= count * item["weight"]
            total_value+= count * item["value"]
    return {
        "selected_items": selected,
        "total_weight": total_weight,
        "total_value": total_value,
        "quantities": chromosome[:],
    
    }


    

    










