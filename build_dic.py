import os
import re
import shutil

def merge_files(inFiles):
    text = ""
    lines = []
    for file in inFiles:
        with open(file, 'r') as f:
            text += f.read() + "\n"

    lines = sorted(list(text.splitlines()))
    text = "\n".join(lines).strip()
    text = re.sub(r"#.*?\n", "\n", text).strip()  # remove comments
    text = "{}\n".format(text.count('\n')+1) + text
    with open('en-Academic.dic', 'w') as f:
        f.write(text)


def copyDic2(dest):
    shutil.copy2('en-Academic.dic', dest)
    shutil.copy2('en-Academic.aff', dest)    



def create_oxt():
    copyDic2('./addons/oxt')
    shutil.make_archive('addons/acamedic', 'zip', './addons/oxt/')
    os.rename('addons/acamedic.zip', 'addons/acamedic-libreoffice.oxt')

def create_xpi():
    copyDic2('./addons/xpi/dictionaries')
    shutil.make_archive('addons/acamedic', 'zip', './addons/xpi/')
    os.rename('addons/acamedic.zip', 'addons/acamedic-mozilla.xpi')




def install():
    home = os.path.expanduser("~")

    ## Windows
    if os.name == 'nt':
        pass  # todo, not implemented yet

    ## Linux
    elif os.name == 'posix':

        ### Sublime Text 3:
        if os.path.isdir(home+'/.config/sublime-text-3/Packages/'):
            if not os.path.isdir(home+'/.config/sublime-text-3/Packages/Language - English'):
                os.mkdir(home+'/.config/sublime-text-3/Packages/Language - English')
            copyDic2(home+'/.config/sublime-text-3/Packages/Language - English/')





# merge dictionaries
# ==========================================
merge_files(['src/base/en_US_20.dic', 
             'src/base/en_US_extra.dic', 
             'src/base/en_US_abbr.dic', 
             'src/base/en_Latin.dic', 
             'src/academic/en_US_tech.dic', 
             'src/academic/en_US_computer.dic', 
             'src/academic/en_US_math.dic', 
             'src/academic/en_US_physics.dic', 
             'src/academic/en_US_unit.dic', 
             'src/academic/en_US_symbols.dic', 
             'src/academic/en_US_chem.dic', 
             'src/academic/en_US_med.dic', 
             'src/names/names_geo.dic', 
             'src/names/names_people.dic', 
             'src/names/names_misc.dic',
             'src/names/names_brands.dic',
             'src/names/names_scientists.dic',
             'src/code/code_latex.dic',
             'src/code/code_c.dic',
             'src/code/code_fileextension.dic',
             'src/own.dic',
             ])


# install
install()

# create extensions for LibreOffice and Thunderbird
create_oxt()
create_xpi()





