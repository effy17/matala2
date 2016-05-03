import sys
import re
import math


def main():

    in_filename = "2.txt"
    out_filename = "taa5.csv"

    kml_file = open(out_filename, 'w')

    kml_file.write('date_and_time, Numberofsatellites,lon,speed\n')
    for line in open(in_filename, 'r'):

        if not line:
            continue

        # Try to catch corrupt lines early
        if not line.startswith('$GP'):
            continue

        # Skip any sentence other than GPGGA
        if not line.startswith('$GPGGA'):
            continue

        list = line.split(',')


        hhmmss = list[1]
        time = hhmmss[0:2] + ":" + hhmmss[2:4] + ":" + hhmmss[4:10]
        lat2 = float(list[2][:2]) + (float(list[2][2:]) / 60)
        latitude = list[2] + " " + list[3]
        lon2 = float(list[4][:3]) + (float(list[4][3:]) / 60)
        longtitude = list[4] + " " + list[5]
        Numberofsatellites =list[7]
        altitude = list[9]
        kml_file.write('%s,%s,%s,%s\n'% (time, Numberofsatellites, longtitude, altitude) )
    kml_file.close();


if __name__ == '__main__':
    main()
