import subprocess
import shutil
from typing import Type
    
def getShellSize():
    col, line = shutil.get_terminal_size()
    col = int(int(col)/2)
    line = int(int(line)/2)
    return col, line

def whiptailCommandAndResult(list):
    result = subprocess.run(list, stderr=subprocess.PIPE)
    return result.stderr.decode('utf-8').strip() , result.returncode

class whiptailConfig():
    def __init__(self, type: str, value, option: list = None, default: str = None):
        self.type = str(type)
        self.value = (isinstance(value, bool) and value) or str(value)
        self.option = option
        self.default =  list[0] or default

    def __repr__(self) -> str:
        return "{}".format(self.value)

    def display(self, name: str = None, parent: str = None):
        column, line = getShellSize()
        if name == "finish":
            list = ["whiptail", "--title", "{}".format(parent), "--{}".format(self.type), "--default-item", "yes", "Finish {}".format(parent), "{}".format(line), "{}".format(column)]
            result, returnCode = whiptailCommandAndResult(list)
            self.value = not returnCode
        elif self.type == "menu" and self.option != None:
            whiptailOption = []
            for index, value in enumerate(self.option):
                whiptailOption.append(str(index))
                whiptailOption.append(str(value))
            list = ["whiptail", "--title", "{}-{}".format(parent,name), "--{}".format(self.type), "--default-item", "{}".format(self.default), "Choose an option", "{}".format(line), "{}".format(column), "{}".format(line - 8)]+whiptailOption
            result, returnCode = whiptailCommandAndResult(list)
            if returnCode == 0:
                self.value = self.option[int(result)]
                self.default = str(result)
        elif self.type == "inputbox":
            list = ["whiptail", "--title", "{}-{}".format(parent,name), "--{}".format(self.type), "Input {}, current {}".format(name, self.value), "{}".format(line), "{}".format(column)]
            result, returnCode = whiptailCommandAndResult(list)
            if returnCode == 0:
                if result != "":
                    self.value = str(result)

        
            

class configMenu(whiptailConfig):
    def __init__(self, config: dict):
        super().__init__(type = "menu", value = "", default = next(iter(config)))
        self.config = config
        self.config['finish'] = whiptailConfig("yesno", False)
        
    def __repr__(self) -> str:
        rep = []
        for key, value in self.config.items():
            rep.append("{}: {}".format(key, str(value)))

        return ", ".join(rep)
    def display(self, name, parent=None):
        shouldFinish = False
        while not shouldFinish:
            whiptailMenu = []
            for key, value in self.config.items():
                if key == "whiptail":
                    continue
                if key == "finish":
                    whiptailMenu.append(str(key))
                    whiptailMenu.append("")
                    continue

                whiptailMenu.append(str(key))
                whiptailMenu.append(str(value))

            column, line = getShellSize()

            list = ["whiptail", "--title", "{}".format(name), "--{}".format(self.type), "--default-item", "{}".format(
                self.default), "Choose an option", "{}".format(line), "{}".format(column), "{}".format(line - 8)]+whiptailMenu
            result, returnCode = whiptailCommandAndResult(list)
            if returnCode == 1:
                return
            self.default = result

            self.config[result].display(result, name)
            
            if self.config["finish"].value==True:
                return
            if not isinstance(self.config[result], configMenu):
                list = ["whiptail", "--title", "{}".format(name), "--yesno", "--default-item", "yes", "Continue setting", "{}".format(line), "{}".format(column)]
                result = subprocess.run(list)
                shouldFinish = result.returncode
