import argparse
from pathlib import Path
from modules.check_toml import CheckTomlTLM, CheckTomlSGC, CheckTomlBCT
from modules.generate_c2a import C2ACodeGenerator
from modules.utils import Util, print_progress


class CheckSettingsJson(Util):
    @print_progress("check settings.json")
    def __init__(self):
        self.settings, self.path_base = self.get_settings_json()
        self.check_settings_json_params()
        self.shape_settings()
        self.check_settings_json_path()

    def get_settings(self):
        return self.settings

    def check_settings_json_params(self):
        self.check_param("is_main_obc")
        if "other_obc_data" not in self.settings:
            self.settings["is_main_obc"] = False
        self.check_param("is_c2a_enable")
        self.check_param("db_prefix")
        self.check_param("db_path")
        self.check_param("dest_path")
        self.check_param("max_tlm_num")
        if self.settings["is_main_obc"]:
            self.check_param("other_obc_data", "name")
            self.check_param("other_obc_data", "driver_name")
            self.check_param("other_obc_data", "driver_type")
            self.check_param("other_obc_data", "is_enable")
            self.check_param("other_obc_data", "db_prefix")
            self.check_param("other_obc_data", "db_path")
            self.check_param("other_obc_data", "dest_path")
            self.check_param("other_obc_data", "max_tlm_num")
            self.check_param("other_obc_data", "code_when_tlm_not_found")

    def shape_settings(self):
        name = "MOBC" if self.settings["is_main_obc"] else "main"
        settings_shaped = []
        settings_shaped.append({
            "is_enable": self.settings["is_c2a_enable"],
            "name": name,
            "db_prefix": self.settings["db_prefix"],
            "db_path": Path(self.path_base) / self.settings["db_path"],
            "dest_path": Path(self.path_base) / self.settings["dest_path"],
            "max_tlm_num": self.settings["max_tlm_num"],
        })
        if self.settings["is_main_obc"]:
            for obc_data in self.settings["other_obc_data"]:
                settings_shaped.append({
                    "is_enable": obc_data["is_enable"],
                    "name": obc_data["name"],
                    "driver_name": obc_data["driver_name"],
                    "driver_type": obc_data["driver_type"],
                    "db_prefix": obc_data["db_prefix"],
                    "db_path": Path(self.path_base) / obc_data["db_path"],
                    "dest_path": Path(self.path_base) / obc_data["dest_path"],
                    "max_tlm_num": obc_data["max_tlm_num"],
                    "code_when_tlm_not_found": obc_data["code_when_tlm_not_found"]
                })
        self.settings = settings_shaped

    def check_settings_json_path(self):
        for setting in self.settings:
            self.check_path(setting, "db_path", is_db=True)
            self.check_path(setting, "dest_path")


@print_progress("main")
def main(settings):
    for index, setting in enumerate(settings):
        setting = CheckTomlTLM(setting).get_settings()
        setting = CheckTomlSGC(setting).get_settings()
        setting = CheckTomlBCT(setting).get_settings()
        settings[index] = setting
    if settings[0]["is_enable"]:
        C2ACodeGenerator(settings)


if __name__ == "__main__":
    settings = CheckSettingsJson().get_settings()
    main(settings)
