import pymysql
import os
import sys
import re
currDir = os.path.dirname(os.path.realpath(__file__))

GPGGA = re.compile("""
    # Sample line:
    # $GPGGA,035306.200,4735.7144,N,12219.6396,W,1,8,1.42,-2.1,M,-17.3,M,,*46
    ^\$GPGGA,
    (?P<hhmmss>\d{6}(\.\d{3})),      # hhmmss = '035306.200' 1
    (?P<latitude>\d+\.\d+),          # latitude = '4735.7144' 2
    (?P<N_S>[NS]),                   # N_S = 'N' 3
    (?P<longitude>\d+\.\d+),         # longitude = '12219.6396' 4
    (?P<W_E>[WE]),                   # W_E = 'W' 5
    (?P<fix_qual>[012]),             # fix_qual = '1' 6
    (?P<num_sat>\d+),                # num_sat = '8' 7
    (?P<hdop>\d+(\.\d+)),            # hdop = 1.42 8
    (?P<altitude>(\-)?\d+(\.\d+)),M, # altitude = -2.1 9
    (?P<height>(\-)?\d+(\.\d+)),M,   # height = -17.3 11
    (?P<dgps>([!\,]+)?),             # dgps = '' 13
    (?P<checksum>\*\w\w)$            # checksum = '*46' 14
""", re.VERBOSE)
    

KML_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
xmlns:atom="http://www.w3.org/2005/Atom"
xmlns:gx="http://www.google.com/kml/ext/2.2">
<Document>
<Placemark>
<gx:Track>
"""

KML_FOOTER = """</gx:Track>
</Placemark>
</Document>
</kml>
"""


NMEA_TABLE_CREATE = " USE nmea; CREATE TABLE IF NOT EXISTS `nmeas` (`ID` int(11) NOT NULL AUTO_INCREMENT,`TALKER_ID` varchar(45) NOT NULL,`SENTENCE` varchar(124) NOT NULL,`FILE_NAME` varchar(124) DEFAULT NULL,PRIMARY KEY (`ID`)) ENGINE=InnoDB AUTO_INCREMENT=5408 DEFAULT CHARSET=utf8;"

#Change the password to the new user password

def connectToDB():
    return pymysql.connect(host='localhost', port=3306, user='root', passwd='1111', db='mysql')

def initDB():
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS nmea;")
    cur.execute(NMEA_TABLE_CREATE)
    cur.close()
    conn.close()

def getKMLLine(row):
    minus = {'N':'', 'S':'-', 'W':'-', 'E':''}
    kmlLine = ""
    line = row[0].strip()

    if not line:
        return ""
    if not line.startswith('$GP'):
        return ""
    if not line.startswith('$GPGGA'):
        return ""
    result = dict.fromkeys(["hhmmss", "latitude", "N_S", "longitude", "W_E", "fix_qual", "num_sat", "hdop", "altitude", "height", "dgps", "checksum"])
    try:
    # Try to match a valid GPGGA sentence
        cells = line.split(",")
        result["hhmmss"]  = cells[1]
        result["latitude"]  = cells[2]
        result["N_S"]  = cells[3]
        result["longitude"] = cells[4]
        result["W_E"]   = cells[5]
        result["fix_qual"]  = cells[6]
        result["num_sat"]  = cells[7]
        result["hdop"]  = cells[8]
        result["altitude"]  = cells[9]
        result["height"]  = cells[11]
        result["dgps"]  = cells[13]
        result["checksum"]   = cells[14]
    except Error:
        print ('Bad line: ', Error)
        return ""

    if not result['W_E']:
        return ""
    if not result['N_S']:
        return ""

    hhmmss = result['hhmmss']
    result['time_string'] = ':'.join((hhmmss[0:2], hhmmss[2:4], hhmmss[4:10]))
    result['latitude'] = minus[result['N_S']] + result['latitude']
    result['longitude'] = minus[result['W_E']] + result['longitude']
    kmlLine += '<when>T%(time_string)sZ</when>' % result
    kmlLine += '<gx:coord>%(longitude)s %(latitude)s %(altitude)s</gx:coord>\n' % result

    return kmlLine



def startFunction():
    action = input("1. Import NMEA file  ")
    if action == "1":
        fileName = input("1. Enter file to import(from current directory): ")
        file_path = currDir +"\\" + fileName
        fileExists = os.path.exists(file_path)
        if fileExists:
            f = open(file_path, 'r')
            text = f.read()
            lines = text.split("\n")
            conn = connectToDB()
            cur = conn.cursor()
            for line in lines:
                talkerId = line.split(",")[0]
                add_row = ("INSERT INTO nmea.nmeas "
                       "(TALKER_ID, SENTENCE) "
                       "VALUES (%s, %s)")
                add_row_value = (talkerId, line.strip());
                cur.execute(add_row, add_row_value)
            conn.commit()
            cur.close()
            conn.close()
            print("File Loaded to DB Successfully!!!!!!!!!!! \n")
        else:
            print("File not exisits!!!!!!!!!!! \n")

        startFunction()
        
    elif action =="2":
        nmea = input("Select NMEA sentence (use * for all):")
        
        conn = connectToDB()
        cur = conn.cursor()

        if nmea == "*":
            cur.execute("SELECT SENTENCE FROM nmea.nmeas")
        else:
            cur.execute("SELECT SENTENCE FROM nmea.nmeasb WHERE TALKER_ID ='" + nmea + "'" )
        
        kml = KML_HEADER
        csv = ""
        for row in cur:
            kml += getKMLLine(row)
            csv += row[0] + "\n"

        kml += KML_FOOTER
        
       # kmlFile = open("result.kml", 'w')
        kmlFile.write(kml)
        kmlFile.close()
        #csvFile = open("result.csv", 'w')
        csvFile.write(csv)
        csvFile.close()

        cur.close()
        conn.close()
        
        print("Finish Successfully!!!")
        print("CSV file created in: " + currDir +"\\result.csv")
        startFunction()
    elif action =="3":
        conn = connectToDB()
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE nmea.nmeas;")
        conn.commit()
        cur.close()
        conn.close()
        startFunction()
    else:
        print("Invalid option!!! \n")
        startFunction()
            
initDB()
startFunction()

#cur.execute("SELECT * FROM nmea.nmeas")

#for row in cur:
#    print(row)
