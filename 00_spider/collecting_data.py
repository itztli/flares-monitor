#!/usr/bin/env python3
#
#    vdelaluz@enesmorelia.unam.mx
#    Copyright (C) 2022  Victor De la Luz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import json
from datetime import datetime

def readConfig(configFile):
    with open(configFile) as f:
        lines = f.readlines()

    config = []
    for line in lines:
        if line[0] != '#':
            config.append(line.strip())
    return config

config = readConfig('/home/vdelaluz/git/flares-monitor/00_spider/config.dat')
    
output_directory=config[0]

os.system('wget --directory-prefix='+output_directory+'/backup https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json')

dir_path = output_directory + '/backup/'

max = -1

for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        split_file = path.split('.')
        print(split_file)
        if len(split_file) == 2:
            max = -1
        if len(split_file) > 2:
            if int(split_file[2]) > max:
                max = int(split_file[2])

if max == -1:
    filename = 'xray-flares-latest.json'
else:
    filename = 'xray-flares-latest.json.'+str(max)

#print(output_directory+'/backup/'+filename)

# 1) Leer informacion del last.dat (el ultimo max_time, en caso de que no exista, lo creamos)

try:
    with open(output_directory+'/last.dat') as file:
        linestr = file.read()
        max_time = datetime.strptime(linestr.strip(), '%Y-%m-%dT%H:%M:%SZ')
except OSError as e:
    print(e.errno)
    print("Ignoring last.dat")
    max_time = datetime.strptime('1980-01-01 01:01:01', '%Y-%m-%d %H:%M:%S')



# 2) Leer la informacion del ultimo archivo bajado con wget

f = open(output_directory+'/backup/'+filename)
data = json.load(f)

#print(data[0]['max_time'])
#print(data[0]['max_class'])
XML_string = ''
XML_string = XML_string + '<xml>\n'
XML_string = XML_string + ' <flare>\n'
XML_string = XML_string + '  <time>\n'
XML_string = XML_string + '   '+data[0]['max_time']+'\n'
XML_string = XML_string + '  </time>\n'
XML_string = XML_string + '  <class>\n'
XML_string = XML_string + '   '+data[0]['max_class']+'\n'
XML_string = XML_string + '  </class>\n'
XML_string = XML_string + ' </flare>\n'
XML_string = XML_string + '</xml>'
print(XML_string)
f.close()

# 3) si wget > last actualizar last.dat y conservar el archivo wget, en otro caso borrar wget.

last_time =  datetime.strptime((data[0]['max_time']).strip(),'%Y-%m-%dT%H:%M:%SZ') 
if last_time > max_time:
    #delete output_directory+'/backup/'+filename
    if not '-rf' in  output_directory+'/backup/'+filename:
        os.remove(output_directory+'/backup/'+filename)

    try:
        with open(output_directory+'/last.dat','w') as file:
            file.write(data[0]['max_time'])
    except OSError as e:
        print(e.errno)

