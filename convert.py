import os
for i in range(321, 800):
         os.system("gdal_translate -scale_1 20 1463 -scale_2 114 1808 -scale_3 139 1256 -ot Byte -of PNG Vegas_" + str(i) + ".tif " + str(i) + ".png")
