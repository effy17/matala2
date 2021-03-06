import sys
import re
import math


def main():

    in_filename = "asi.txt"
    out_filename = "testigalgo.kml"

    kml_file = open(out_filename, 'w')

    kml_file.write('<?xml version="1.0"  encoding="UTF-8"?>\n')
    kml_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    kml_file.write('<Document>\n')
    kml_file.write('<Folder>\n')
    kml_file.write('<name>Point Features</name>\n')
    kml_file.write('<description>Point Features</description>\n')

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

        kml_file.write('<Placemark>\n')
        hhmmss = list[1]
        time = hhmmss[0:2] + ":" + hhmmss[2:4] + ":" + hhmmss[4:10]
        lat2 = float(list[2][:2]) + (float(list[2][2:]) / 60)
        latitude = list[2] + " " + list[3]
        lon2 = float(list[4][:3]) + (float(list[4][3:]) / 60)
        longtitude = list[4] + " " + list[5]
        altitude = list[9]
        kml_file.write('<Point>\n')
        kml_file.write('<coordinates> %s,%s,%s </coordinates>\n' % (lon2, lat2, altitude))
        kml_file.write('</Point>\n')
        kml_file.write('</Placemark>\n')

    kml_file.write('</Folder>\n')
    kml_file.write('</Document>\n')
    kml_file.write('</kml>\n')
    kml_file.close();


if __name__ == '__main__':
    main()
