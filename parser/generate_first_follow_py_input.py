production_rules = ""
with open("production_rules.txt", "r") as f:
    for line in f:
        production_rules += line

production_list = production_rules.split("\n")
# print(production_list)
left_side = []
right_side = []
for p in production_list:
    p_split = p.split("->")
    left, right = p_split[0], p_split[1]
    left_side.append(left)
    right_side.append(right)

left_side_set = set("".join(left_side))
right_side_set = set("".join(right_side))

right_side_set_2 = right_side_set.copy()
for l in left_side_set:
    right_side_set_2.remove(l)
right_side_set_2.remove("/")
right_side_set_2.remove("@")

# print("-------------------------------------------------")
print(len(right_side_set_2)) #NUM. OF TERMINALS
for r in right_side_set_2: # TERMINALS
    print(r)

print(len(left_side_set)) # NUM. OF NON-TERMINALS
for l in left_side_set: # NON-TERMINALS
    print(l)

print(production_list[0][0]) # STARTING SYMBOL
print(len(production_list)) # NUM. OF PRODUCTIONS
for p in production_list: # PRODUCTIONS
    print(p)