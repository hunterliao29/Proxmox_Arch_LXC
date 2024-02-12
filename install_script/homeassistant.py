from lib.lxc_config import lxc_config

class config(lxc_config):
    def __init__(self):
        super().__init__()
        self.config.config["cores"].value = 5
    