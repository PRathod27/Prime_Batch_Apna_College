a = 10
b = 20
sum = a+b

# normal formatting
print("language is {}".format("Python"))
print("sum of {} & {} is {}".format(a,b,sum))

# index based formatting
print("sum of {1} & {0} is {2}".format(a,b,sum))

# value based formatting
print("values of vars {a} and {b}".format(a=90,b=20))


# F string
print(f'sum of {a} and {b} is {a+b}')