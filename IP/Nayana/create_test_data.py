import numpy as np

#WRITE TEST DATA

odlc_data = np.empty((0,5),dtype=str)

#path, shape colour, letter colour, shape

odlc_data = np.append(odlc_data, [['pic1.JPG', 'blue', 'T', 'red', 'semicircle']], axis=0)
odlc_data = np.append(odlc_data, [['pic2.JPG', 'white', 'V', 'blue', 'square']], axis=0)
odlc_data = np.append(odlc_data, [['pic3.JPG', 'white', 'S', 'gray', 'circle']], axis=0)
odlc_data = np.append(odlc_data, [['pic4.JPG', 'blue', 'O', 'white', 'triangle']], axis=0)
odlc_data = np.append(odlc_data, [['pic5.JPG', 'white', 'B', 'green', 'triangle']], axis=0)
'''
a = np.append(a, ['pic1.JPG', 'red', 'blue', 'semicircle'], axis=0)
a = np.append(a, ['pic2.JPG', 'blue', 'white', 'square'], axis=0)
a = np.append(a, ['pic3.JPG', 'gray', 'white', 'circle'], axis=0)
a = np.append(a, ['pic4.JPG', 'white', 'blue', 'triangle'], axis=0)
a = np.append(a, ['pic5.JPG', 'green', 'white', 'triangle'], axis=0)
'''
np.save('data1',odlc_data)

