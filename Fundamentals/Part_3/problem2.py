info = [
    ("Alice","Math"),
    ("Bob","Science"),
    ("Charlie","English"),
    ("David","Math"),
    ("Emma","English"),
    ("Frank","Science"),
]

dict = {}
for name, course in info:
    if(dict.get(name) == None):
        dict.update({name:set()})
        dict[name].add(course)
    else:
        dict[name].add(course)
print(dict)
