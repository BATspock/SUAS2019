lat = str(input())
lon = str(input())

print(float(lat[:2])+float(lat[2:4])/60+ float(lat[4:])/3600)

print('-' + str(float(lon[:2])+float(lon[2:4])/60+ float(lon[4:])/3600))
