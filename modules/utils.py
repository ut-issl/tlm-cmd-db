from pathlib import Path
import json


def get_path_list(path, db_prefix=None, suffix="csv"):
    p = Path(path)
    p_list = list(p.glob(f"*.{suffix}"))
    if db_prefix is not None:
        p_list = [p for p in p_list if db_prefix in str(p)]
    return p_list


def print_progress(txt):
    def _print_progress(f):
        def wrapper(*args, **kwargs):
            print(f"START {txt}")
            res = f(*args, **kwargs)
            print(f"END {txt}")
            return res
        return wrapper
    return _print_progress


def err(p, data, txt):
    return f"""
-----error file-----
{str(p)}
-----error data-----
{data}
-----error txt-----
{txt}"""


type2bit = {
    "int8_t": 8,
    "int16_t": 16,
    "int32_t": 32,
    "uint8_t": 8,
    "uint16_t": 16,
    "uint32_t": 32,
    "float": 32,
    "double": 64,
}


class Util:
    def check_param(self, *args):
        if len(args) == 1:
            assert args[0] in self.settings, f"settings.jsonに{args[0]}を定義してください"
        else:
            for setting in self.settings[args[0]]:
                assert args[1] in setting, f"settings.jsonに{args[0]}.{args[1]}を定義してください"

    def check_path(self, setting, key, is_db=False):
        def make_dirs(path):
            if is_db:
                (path / "TLM_DB" / "md").mkdir(exist_ok=True, parents=True)
                (path / "TLM_DB" / "csv").mkdir(exist_ok=True, parents=True)
                (path / "TLM_DB" / "toml").mkdir(exist_ok=True, parents=True)
                (path / "CMD_DB" / "md").mkdir(exist_ok=True, parents=True)
                (path / "CMD_DB" / "csv").mkdir(exist_ok=True, parents=True)
                (path / "CMD_DB" / "toml").mkdir(exist_ok=True, parents=True)
                (path / "TLM_DB" / "status.toml").touch(exist_ok=True)
                if (path / "TLM_DB" / "status.toml").read_text() == "":
                    (path / "TLM_DB" / "status.toml").write_text("[status]")
        path = Path(self.path_base) / setting[key]
        assert path.exists() and path.is_dir(), f'{str(path)}が存在しません.'
        make_dirs(path)

    @ staticmethod
    def get_settings_json():
        path_base = Path(__file__).parent.parent
        if (Path(path_base) / "settings.json").exists():
            dict_settings = json.load(open(path_base / "settings.json", encoding="utf-8"))
            dict_settings["is_example"] = False
            path_base = path_base
        elif (Path(path_base.parent) / "settings.json").exists():
            dict_settings = json.load(open(path_base.parent / "settings.json", encoding="utf-8"))
            dict_settings["is_example"] = False
            path_base = path_base.parent
        else:
            is_init = True
            res = ""
            while res not in ["yes", "no"]:
                if is_init:
                    is_init = False
                    print(f"---warning settings.jsonが存在しないため, settings_example.jsonに従って実行します.")
                    print(f"---warning よろしいですか: yes / no")
                else:
                    print(f"---warning yes か no を入力してください")
                res = input()
            if res == "no":
                raise NameError("settings_example.jsonをコピーしてsettings.jsonを作成した上で実行してください")
            dict_settings = json.load(open(path_base / "settings_example.json", encoding="utf-8"))
            dict_settings["is_example"] = True
        return dict_settings, path_base


def get_exp_comp(_data):
    exp_list = []
    bitlen_list = []
    if "exp" not in _data and "exp" in _data["comp"][0]:
        is_exp_init = True
        for i, data in enumerate(_data["comp"]):
            if is_exp_init:
                is_exp_init = False
            if "exp" in data:
                exp_list.append(data["exp"])
                bitlen_list.append(data["bitlen"])
                if not is_exp_init:
                    _data["comp"][i].pop("exp")
        # bit圧縮
        maxbyte = type2bit[_data["type"]]
        exp = f'({_data["type"]})('
        for i, byte_ in enumerate(bitlen_list):
            exp += f'({exp_list[i]} << {maxbyte-byte_} & {int("0b" + "1"*byte_ + "0"*(maxbyte-byte_), 0):#04x}) | '
            exp = exp.replace("<< 0 ", "")
            maxbyte -= byte_
        exp = exp[:-3] + ")"
        return exp
    elif "exp" in _data:
        return _data["exp"]
    else:
        return None
