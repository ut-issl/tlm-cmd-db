import argparse
from pathlib import Path
from modules.make_toml import Csv2TomlTLM, Csv2TomlSGC, Csv2TomlBCT
from modules.utils import print_progress, Util


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help='input db_root path')
    opt = parser.parse_args()
    assert opt.input is not None and Path(opt.input).exists(), "1つ目の引数には存在するパスを指定してください"
    return opt


class CheckSettingsJson(Util):
    @print_progress("check settings.json")
    def __init__(self, opt):
        self.settings, self.path_base = self.get_settings_json()
        self.settings["db_input_path"] = Path(self.path_base) / opt.input
        self.settings["db_path"] = Path(self.path_base) / self.settings["db_path"]
        self.check_settings_json_params()
        self.check_settings_json_path()

    def get_settings(self):
        return self.settings

    def check_settings_json_params(self):
        self.check_param("db_path")

    def check_settings_json_path(self):
        self.check_path(self.settings, "db_path", is_db=True)
        self.check_path(self.settings, "db_input_path")


@print_progress("main")
def main(settings):
    if (Path(settings["db_input_path"]) / "TLM_DB").exists():
        Csv2TomlTLM(settings)
    if (Path(settings["db_input_path"]) / "CMD_DB").exists():
        Csv2TomlSGC(settings)
        Csv2TomlBCT(settings)


if __name__ == "__main__":
    opt = parse_opt()
    settings = CheckSettingsJson(opt).get_settings()
    main(settings)
