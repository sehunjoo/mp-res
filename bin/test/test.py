from ase.formula import Formula
w = Formula('Li2Ni2O4')

print(w)

fu, nfu = w.reduce()
print(fu)

w2 = w.format('hill')
print(w2)

fu, nfu = w.convert('hill').reduce()
print(fu)
