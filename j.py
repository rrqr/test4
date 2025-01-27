import os
import sys
from module.l4 import *
from module.l7 import *
from module.method import *
from Tools.main import *
from pystyle import Colorate, Colors

# الوظيفة لعرض الشعار
def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.cyan_to_green,"""                              
                    ╔═╗╔═╗╦╔═╗
                    ╔═╝║ ║║║  
                    ╚═╝╚═╝╩╚═╝    
                              
            ╔════════════════════════╗
            ║        [method]        ║            
            ║   Type to see command  ║
            ╚════════════════════════╝            
                      """))

# وظيفة التثبيت
def install():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.cyan_to_green,"""                              
                    ┌─┐┌─┐┌┬┐┬ ┬┌─┐
                    └─┐├┤  │ │ │├─┘
                    └─┘└─┘ ┴ └─┘┴    
                                                                    
"""))
    print("""
     ██╗ ██████╗ ██╗  ██╗███╗   ██╗    ██████╗     ██╗ ██████╗ 
     ██║██╔═══██╗██║  ██║████╗  ██║    ╚════██╗██╗███║██╔════╝ 
     ██║██║   ██║███████║██╔██╗ ██║     █████╔╝╚═╝╚██║███████╗ 
██   ██║██║   ██║██╔══██║██║╚██╗██║     ╚═══██╗██╗ ██║██╔═══██╗
╚█████╔╝╚██████╔╝██║  ██║██║ ╚████║    ██████╔╝╚═╝ ██║╚██████╔╝
 ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═════╝     ╚═╝ ╚═════╝
          """)
    os.system("pip install aiosonic --break-system-packages")
    os.system("pip install cloudscraper --break-system-packages")
    os.system("pip install aiohttp --break-system-packages")
    os.system("pip install scapy --break-system-packages")
    os.system("git pull")

# الوظيفة الرئيسية
def main():
    while True:
        logo()
        select = input(Colorate.Horizontal(Colors.green_to_blue,"""   
╔═══[root@ZOIC~$]   
╚══> """))
        
        # إضافة الخيار لتثبيت المكتبات
        if select == "install" or select.lower() == "i":
            install()

        elif select == "method" or select.lower() == "h":
            method_main()

        elif select == "layer7" or select.lower() == "l7":
            layer7()

        elif select == "layer4" or select.lower() == "l4":
            layer4()

        elif select == "Tools" or select.lower() == "t":
            Tools_main()

if __name__ == "__main__":
    main()
