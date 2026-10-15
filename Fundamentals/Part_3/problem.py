info = [
    ("Alice","Math"),
    ("Bob","Science"),
    ("Charlie","English"),
    ("David","Math"),
    ("Emma","English"),
    ("Frank","Science"),
]

print(info[0][1])


set1 = set()
for tup in info:
    set1.add(tup[1])

print(set1)

# list students learning abc course
for name, course in info:
    if(course == "English"):
        print(name)
