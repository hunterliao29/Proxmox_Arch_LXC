from utility import proxmox
from utility import whiptail
import subprocess

whiptailConfig = whiptail.whiptailConfig
configMenu = whiptail.configMenu

class lxc_config:
    def __init__(self):
        self.config = configMenu({
            "vmid": whiptailConfig("inputbox", 100),
            "memory": whiptailConfig("inputbox", 2048),
            "rootfs": configMenu({
                "storage": whiptailConfig("menu", "test1", ["test1", "local", "test2"], "1"),
                "size": whiptailConfig("inputbox", 4),
            } ),
            "cores": whiptailConfig("inputbox", 1),
        })
    def menu(self):
        self.config.display("LXC Configuration")

   