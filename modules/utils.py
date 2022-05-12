import json
import toml
import os
from pathlib import Path

typelist = {
    "int8_t": 8,
    "int16_t": 16,
    "int32_t": 32,
    "uint8_t": 8,
    "uint16_t": 16,
    "uint32_t": 32,
    "float": 32,
    "double": 64,
}
dict_status = toml.load(open("status.toml"))["status"]
dict_settings = json.load(open("settings.json"))


def status2md(path_to_md="status.md"):
    txt = """# Status Table\n
Length|Index|Status
-|-|-
"""
    for length, dict_status_ in dict_status.items():
        for index, status in dict_status_.items():
            txt += f'{length}|{index}|{status}\n'
        else:
            continue
    Path(path_to_md).write_text(txt)


def get_path(path, suffix=None):
    p = Path(path)
    assert p.exists()

    if p.is_file():
        return [p]
    elif p.is_dir():
        if suffix is not None:
            return list(p.glob(f"*.{suffix}"))


def _make_dirs(opt, is_tlm=False, is_cmd=False):
    if is_tlm:
        os.makedirs(opt.tlm_md, exist_ok=True)
        os.makedirs(opt.tlm_csv, exist_ok=True)
        os.makedirs(opt.tlm_toml, exist_ok=True)
    if is_cmd:
        os.makedirs(opt.cmd_md, exist_ok=True)
        os.makedirs(opt.cmd_csv, exist_ok=True)
        os.makedirs(opt.cmd_toml, exist_ok=True)


def checksettings(opt):
    try:
        opt.is_tlm = False
        opt.is_cmd = False
        if opt.input is not None:
            assert opt.obc.upper() in dict_settings["obc_data"], f'settings.jsonで{opt.obc.upper()}(大文字)の設定を記述してください'
            opt.is_tlm = opt.tlm
            opt.is_cmd = opt.cmd
        if opt.tlm:
            opt.is_tlm = True
            opt.tlm_md = dict_settings["tlm"]["path"]["md"] if opt.md is None else opt.md
            opt.tlm_csv = dict_settings["tlm"]["path"]["csv"] if opt.csv is None else opt.csv
            opt.tlm_toml = dict_settings["tlm"]["path"]["toml"] if opt.toml is None else opt.toml
            _make_dirs(opt, is_tlm=True)
            return opt
        if opt.cmd:
            opt.is_cmd = True
            opt.cmd_md = dict_settings["cmd"]["path"]["md"] if opt.md is None else opt.md
            opt.cmd_csv = dict_settings["cmd"]["path"]["csv"] if opt.csv is None else opt.csv
            opt.cmd_toml = dict_settings["cmd"]["path"]["toml"] if opt.toml is None else opt.toml
            _make_dirs(opt, is_cmd=True)
            return opt
        if dict_settings["tlm"]["is_check"]:
            opt.is_tlm = True
            opt.tlm_md = dict_settings["tlm"]["path"]["md"]
            opt.tlm_csv = dict_settings["tlm"]["path"]["csv"]
            opt.tlm_toml = dict_settings["tlm"]["path"]["toml"]
            _make_dirs(opt, is_tlm=True)
        if dict_settings["cmd"]["is_check"]:
            opt.is_cmd = True
            opt.cmd_md = dict_settings["cmd"]["path"]["md"]
            opt.cmd_csv = dict_settings["cmd"]["path"]["csv"]
            opt.cmd_toml = dict_settings["cmd"]["path"]["toml"]
            _make_dirs(opt, is_cmd=True)
        return opt
    except BaseException:
        raise NameError("settings.jsonの設定を確認してください")
