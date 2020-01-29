"""ambient_downloader.py - download an ambient XML file from ambient-mixer.com
 
Usage:
  ambient_downloader.py <url>
 
Options:
  <url>                 URL of the ambient mix.
  -h --help          Show this help message.
 
"""
__author__      = "Philooz"
__copyright__   = "2017 GPL"

import re, os
import subprocess
#from subprocess import check_output

import requests
import untangle

template_url = "http://xml.ambient-mixer.com/audio-template?player=html5&id_template="
re_js_reg = re.compile(r"AmbientMixer.setup\('#mixer-gui-box', ([0-9]+)\);")

def makedirs():
    if not os.path.exists("sounds_named"):
        os.makedirs("sounds_named")
    if not os.path.exists("presets"):
        os.makedirs("presets")

def download_file(url, save = False, filename = None):
    if(len(url.strip()) == 0):
        return
    response = requests.get(url)
    if(save):
        if filename is None:
            filename = url.split('/')[-1]
        with open(filename, "wb") as file:
            file.write(response.content)
        print("Saved {} as {}.".format(url, filename))
    else:
        return response.text

def get_correct_file(url, filename = None):
    if(filename is None):
        filename = url.split("/")[-1]
    if(not url.startswith(template_url)):
            page = download_file(url)
            val = re_js_reg.findall(str(page))[0]
            url = template_url + val
    fname = os.path.join("presets", "{}.xml".format(filename))
    download_file(url, True, fname)
    return fname

def download_sounds(xml_file):
    obj = untangle.parse(xml_file)
    script_path = os.path.dirname(os.path.realpath(__file__))
    print('script path: ', script_path)
    freaccmd_exe_path = 'C:\\Program Files\\freac-1.0.32-bin\\freaccmd.exe'
#    name_batch_file_for_conversion = 'convert_me.bat'
#    f = open(name_batch_file_for_conversion, 'a')
    for chan_num in range(1,9):
        channel = getattr(obj.audio_template, "channel{}".format(chan_num))
        #print('channel.name_audio.cdata: ', channel.name_audio.cdata)
        new_filename = channel.name_audio.cdata
        url = channel.url_audio.cdata
        ext = url.split('.')[-1]
        filename = os.path.join("sounds_named", new_filename + "." + ext)
        filename_ogg = os.path.join("sounds_named", new_filename + ".ogg")
        if not(os.path.exists(filename) or os.path.exists(filename_ogg)):
            download_file(url, True, filename)
        print('processing sound: ', new_filename)
        #print(r'check_output(\'\"D:\Progs\\freac\freaccmd.exe\" -e LAME \"' + script_path + '\sounds_named\\' + new_filename + '.mp3\" -o \"' + script_path + '\sounds_named\\' + new_filename + '.ogg\"\n\')')
        subprocess.call('\"' + freaccmd_exe_path + '\" -e VORBIS \"' + script_path + '\sounds_named\\' + new_filename + '.mp3\" -o \"' + script_path + '\sounds_named\\' + new_filename + '.ogg\"')
        
		#os.remove(script_path + '\sounds_named\\' + new_filename + '.mp3')

#        f.write('freaccmd.exe -e LAME \"sounds_named\\' + new_filename + '.mp3\" -o \"sounds_named\\' + new_filename + '.ogg\"\n')
#    f.write('del ' + name_batch_file_for_conversion)
#    f.close()
#    check_output("convert_me.bat")

#def convert_sounds(filename_current):
#    #os.system('freaccmd.exe -e LAME \"' + filename_current + '.mp3\" -o \"' + filename_current + '.ogg\"')
#    print('converting: ', filename_current)
#    print('freaccmd.exe -e LAME \"' + filename_current + '.mp3\" -o \"' + filename_current + '.ogg\"')
#    #subprocess.call('freaccmd.exe -e LAME \"' + filename_current + '.mp3\" -o \"' + filename_current + '.ogg\"') #, shell=True) 
#    check_output('freaccmd.exe -e LAME \"' + filename_current + '.mp3\" -o \"' + filename_current + '.ogg\"', shell=True)

from docopt import docopt
if __name__ == "__main__":
    arguments = docopt(__doc__, version = '0.1ß')
    makedirs()
    xml_file = get_correct_file(arguments.get('<url>'))
#    xml_file = get_correct_file('https://harry-potter-sounds.ambient-mixer.com/gryffindor-common-room')    
    download_sounds(xml_file)
    #
    
    
    
