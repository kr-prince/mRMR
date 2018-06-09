import math
import re

def pearson_coefficient( n1, x, y ):
    sum_x = sum_y = sum_sq_dif_x = sum_sq_dif_y = upper = 0.0
    for i in range(n1):
        sum_x += x[i]
        sum_y += y[i]

    mean_x = float(sum_x/n1)
    mean_y = float(sum_y/n1)
    for i in range(n1):
        sum_sq_dif_x += ((x[i] - mean_x)**2)
        sum_sq_dif_y += ((y[i] - mean_y)**2)
        upper += ((x[i] - mean_x) * (y[i] - mean_y))

    lower = float(math.sqrt(sum_sq_dif_x * sum_sq_dif_y))
    if lower == 0:
        corr_coef = 0.0
    else:
        corr_coef = float(upper/lower)
    return abs(corr_coef)

# l1 = [15.5,13.6,13.5,13.0,13.3,12.4,11.1,13.1,16.1,16.4,13.4,13.2,14.3,16.1]
# l2 = [0.450,0.420,0.440,0.395,0.395,0.370,0.390,0.400,0.445,0.470,0.390,0.400,0.420,0.450]
# normal = [56,56,65,65,50,25,87,44,35]
# Hypervent = [87,91,85,91,75,28,122,66,58]
# print pearson_coefficient(14, l1, l2)
# print pearson_coefficient(9, normal, Hypervent)

def read_DataFile(filepath):
    # Open the data file
    fid = open(filepath, "r+")
    # fid = open("file.txt", "r+")
    # Read the data line wise and store in 2-D list
    data = []
    while True:
        line = fid.readline().strip()
        if line == '':
            break
        else:
            data.append(re.findall(r"[-]?\d*\.\d+|[-]?\d+", line))
    # Close opened file
    fid.close()
    return data