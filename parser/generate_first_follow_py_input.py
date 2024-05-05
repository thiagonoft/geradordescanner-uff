production = """D->ABCD/ABC
B->E¨B/E
E->F&A/GH/IJ*K(/L/MJ)NON/MJ)NONPA/QN/RN/SNTE/UV/U&A<V/WJ)N/XV/YZMab&A/cd/ef/e&A<f/gV/h/i/j/k/lZ/md/n
a->U/o
V->J<V/J
d->Z<d/Z
H->p<H/p
K->A<K/A
q->N<q/N
f->N'f/N/@
N->rsN/r
r->tur/t
t->vw/w
w->x)w/x+w/x=w/x.w/x,w/x:w/x;w/x
x->y?x/y[x/y
y->z]y/z{y/z
z->[!/!
!->Z#/Z
#->}!
Z->*N(/J/J*q(/p
p->A/$/%"""

production_list = production.split("\n")
print(production_list)
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

print("-------------------------------------------------")
print("TERMINALS ({})".format(len(right_side_set_2)))
for r in right_side_set_2:
    print(r)

print("NON-TERMINALS ({})".format(len(left_side_set)))
for l in left_side_set:
    print(l)

print("PRODUCTIONS ({})".format(len(production_list)))
for p in production_list:
    print(p)