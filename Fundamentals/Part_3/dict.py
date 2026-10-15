info = {
    "name" : "Prem",
    "cgpa" : 9,
    "subjects" : ["math","science"]
}

print(type(info))
print(info["subjects"][0])


dict_values = list(info.values())
print(dict_values)

print(info.items())

print(info.get("name"))

