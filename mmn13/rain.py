Rainfull_mi = "45, 65, 70.4, 82.6, 20.1, 90.8, 76.1, 30.92, 46.8, 67.1, 79.9"

mi_list = Rainfull_mi.split(", ")
num_rainy_months = len([x for x in mi_list if float(x) > 75])
print(num_rainy_months)
