import toml
import copy
import re
import csv
from .utils import get_path_list, type2bit, print_progress
from abc import abstractmethod, ABCMeta
from .convert_toml import Toml2MdStatus
from pathlib import Path


def add_dict_if_param_exists(dict_, params, k, alt=None, isfloat=False, isdigit=False):
    if params[k] != "":
        if alt is not None:
            dict_[k] = alt
        elif isfloat:
            dict_[k] = float(params[k])
        elif isdigit:
            dict_[k] = int(params[k])
        else:
            dict_[k] = params[k]


def list2dict_with_dict_index(list_, dict_index):
    params = {}
    for i, v in enumerate(list_):
        params[dict_index[i]] = v
    return params


def get_exp_list(txt):
    txt = re.sub(r"^\((.?int\d{0,1}_t|float|double)\)\((.*)\)$", r"\2", txt.strip())  # (型)を消す
    txts = [_txt.strip() for _txt in txt.split("|")]
    exp_list = []
    for txt in txts:
        txt = re.sub(r"^\((.*)\s\<\<\s\d\)$", r"\1", txt).strip()  # ( ... << 4) を消す
        txt = re.sub(r"^\((.*)\s&\s0x..\)$", r"\1", txt).strip()  # ( ... & 0x00) を消す
        txt = re.sub(r"\s\<\<\s\d$", r"", txt).strip()  # << 4 を消す
        # txt = re.sub(r"^\((.*)\)$", r"\1", txt).strip()
        exp_list.append(txt)
    return exp_list


class Csv2TomlBase(metaclass=ABCMeta):
    def __init__(self, path_to_csv, path_to_toml, dict_index=None, db_prefix=None, num_start_line=0, encoding="cp932", delimiter=","):
        self.encoding = encoding
        self.delimiter = delimiter
        self.dict_index = dict_index
        self.num_start_line = num_start_line
        self.is_err = False
        self.err_list = []

        # パス取得
        p_list = get_path_list(path_to_csv, db_prefix=db_prefix, suffix="csv")

        for p in p_list:
            self.p = p
            output_path_to_toml = Path(path_to_toml) / f"{p.stem}.toml"
            # 出力先確認
            if output_path_to_toml.exists():
                res = ""
                is_init = True
                while res not in ["yes", "no"]:
                    if is_init:
                        is_init = False
                        print(f"---warning ファイル{output_path_to_toml}が存在します")
                        print(f"           上書きしますか: yes / no")
                    else:
                        print(f"---warning yer か no を入力してください")
                    res = input()
                if res == "no":
                    continue

            print(f"-----converting {p}")
            # 作成
            self._make_base_data()
            self._make_data()
            if self.is_err:
                continue
            # 出力
            toml.dump(self.data, open(output_path_to_toml, mode='w', encoding="utf-8"))
            # tomlファイル整形
            self.data = Path(output_path_to_toml).read_text(encoding="utf-8")
            self.data = re.sub(r'(.\n)\[\[', r'\1\n[[', self.data)  # 空行を入れる
            self.data = re.sub(r'\n(\n\[\[.*?\..*?\]\])', r'\1', self.data)  # bit圧縮の場合は詰める
            Path(output_path_to_toml).write_text(self.data, encoding="utf-8")
        else:
            if self.is_err:
                err_list = sorted(self.err_list)
                err_list_output = []
                length_pre = 0
                length_index = 0
                for err_status in err_list:
                    header = err_status.split("\n")[0][1:-1]
                    body = err_status.split("\n")[1:]
                    length = int(header.split(".")[1])
                    if length != length_pre:
                        length_pre = length
                        length_index = 1
                        txt = "\n"
                    else:
                        length_index += 1
                        txt = ""
                    err_list_output.append(txt + f"[status.{length}.{length_index}]\n" + "\n".join(body))
                raise NameError("\n".join(err_list_output) + f'\n\n未定義のstatusがあります.\n以上を {str(path_to_toml.parent)}/status.toml に追加してください')

    def _make_base_data(self):
        self.data = {}
        self._f = [row for row in csv.reader(open(self.p, "r", encoding=self.encoding, errors="ignore"), delimiter=self.delimiter)]
        self.make_base_data()
        del self._f[:self.num_start_line]

    def _make_data(self):
        self.make_data_init()
        self._f = iter(self._f)
        for row in self._f:
            if not any(row):
                break
            self.row = [elem.replace("@@", ",") for elem in row]
            self.params = list2dict_with_dict_index(self.row, self.dict_index)
            self.make_data_main()
        self.make_data_last()

    def make_base_data(self):
        pass

    def make_data_init(self):
        pass

    def make_data_main(self):
        pass

    def make_data_last(self):
        pass

    @abstractmethod
    def _parse_csv(self):
        pass


class Csv2TomlTLM(Csv2TomlBase):
    @print_progress("tlm csv to toml")
    def __init__(self, settings, param_name="tlm", encoding="cp932", delimiter=","):
        self._param_name = param_name
        dict_index = {
            0: "comment",
            1: "name",
            2: "type",
            3: "exp",
            4: "ext",
            5: "octetpos",
            6: "bitpos",
            7: "bitlen",
            8: "conv",
            9: "a0",
            10: "a1",
            11: "a2",
            12: "a3",
            13: "a4",
            14: "a5",
            15: "status",
            16: "desc",
            17: "note",
        }
        num_start_line = 8
        path_to_csv = settings["db_input_path"] / "TLM_DB"
        if settings["is_example"]:
            path_to_toml = settings["db_path"] / "TLM_DB" / "toml_example"
        else:
            path_to_toml = settings["db_path"] / "TLM_DB" / "toml"
        self.dict_status = Toml2MdStatus(settings["db_path"] / "TLM_DB" / "status.toml", settings).get_status()
        super().__init__(path_to_csv, path_to_toml, dict_index=dict_index, db_prefix="TLM_DB", num_start_line=num_start_line, encoding=encoding, delimiter=delimiter)

    def make_base_data(self):
        data = self.data
        data[self._param_name] = []
        if "" in [self._f[0][1], self._f[1][1], self._f[2][1], self._f[3][1], self._f[0][3],
                  self._f[0][2], self._f[1][2], self._f[2][2], self._f[3][2]]:
            raise ValueError(f"Target/PacketID/EnableDisable/IsRestricted is empty at {self.p}")
        # self._f[2][1] = self._f[2][1].replace("/", "") # Enable/Disableのスラッシュを消す
        # self._f[0][3] = self._f[0][3].replace(" ", "") # Var Localの空白を消す
        data[f"{self._f[0][1]}"] = self._f[0][2]
        data[f"{self._f[1][1]}"] = self._f[1][2]
        data[f"{self._f[2][1]}"] = self._f[2][2]
        data[f"{self._f[3][1]}"] = self._f[3][2]
        data[f"{self._f[0][3]}"] = self._f[1][3]

    def make_data_init(self):
        # toml用データ作成
        self.is_comp = False
        self.exp_list = []

    def make_data_main(self):
        data = self.data
        params = self.params
        params["type"] = "" if "||" == params["type"].strip() else params["type"]  # ||は空白と同義
        params["exp"] = "" if "||" == params["exp"].strip() else params["exp"]  # ||は空白と同義
        if params["type"] != "":  # 通常時
            # データ追加
            data[self._param_name].append(self._parse_csv(params))
            # bitlenは削除
            if len(data[self._param_name]) >= 2 and "bitlen" in data[self._param_name][-2]:
                data[self._param_name][-2].pop("bitlen")
            # ビット圧縮ではない
            self.is_comp = False
            self.exp_list = []
        else:  # ビット圧縮の場合. 2行目からtypeが空白になる
            if not self.is_comp:  # ビット圧縮とわかる一つ前のデータを変更して追加
                data_last = copy.deepcopy(data[self._param_name][-1])
                data[self._param_name][-1].clear()
                data[self._param_name][-1]["type"] = data_last.pop("type")
                if "exp" in data_last:
                    # expが結合された形の場合, 分割して配列に保持
                    if "|" in data_last["exp"]:
                        self.exp_list = get_exp_list(data_last["exp"])
                    # 結合されていない場合そのまま
                    else:
                        data[self._param_name][-1]["exp"] = data_last.pop("exp")
                # expの配列があれば順に入れる
                if len(self.exp_list) != 0:
                    data_last["exp"] = self.exp_list.pop(0)
                data[self._param_name][-1]["comp"] = [data_last]
                self.is_comp = True
            # expの配列があれば順に入れる
            if len(self.exp_list) != 0:
                params["exp"] = self.exp_list.pop(0)
            # ビット圧縮の場合のデータ追加
            data[self._param_name][-1]["comp"].append(self._parse_csv(params, True))

    def make_data_last(self):
        # 最終行の"bitlen"が残っているので削除
        if "bitlen" in self.data[self._param_name][-1]:
            self.data[self._param_name][-1].pop("bitlen")

    def _parse_csv(self, params, is_comp=False):
        # name & bitlen
        dict_ = {}
        if not is_comp:
            dict_["type"] = params["type"]
        dict_["name"] = params["name"]
        dict_["bitlen"] = int(params["bitlen"]) if params["bitlen"].isdigit() else type2bit[params["type"]]

        # exp
        add_dict_if_param_exists(dict_, params, "exp")
        # HEX
        if params["conv"] == "HEX":
            dict_["is_hex"] = True
        # status
        if params["status"] != "":
            dict_["status"] = {}
            elems = params["status"].replace(" ", "").split(",")
            for elem in elems:
                kv = elem.split("=")
                dict_["status"][kv[0]] = kv[1]
            for length, dict_status_ in self.dict_status.items():
                for index, status in dict_status_.items():
                    if status == dict_["status"]:
                        dict_["status"] = f"{length}.{index}"
                        break
                else:
                    continue
                break
            else:
                len_patch = 1 if "*" in dict_["status"] else 0
                example = f'[status.{len(dict_["status"])-len_patch}.x]\n'
                for k, v in dict_["status"].items():
                    k = int(k) if k.isdigit() else f'"{k}"'
                    example += f'{k} = "{v}"\n'
                self.is_err = True
                if example[:-1] not in self.err_list:
                    self.err_list.append(example[:-1])
        for i in range(6):
            add_dict_if_param_exists(dict_, params, f"a{i}", isfloat=True)
        add_dict_if_param_exists(dict_, params, "desc")
        add_dict_if_param_exists(dict_, params, "note")
        return dict_


class Csv2TomlSGC(Csv2TomlBase):
    @ print_progress("sgc csv to toml")
    def __init__(self, settings, encoding="cp932", delimiter=","):
        dict_index = {
            0: "component",
            1: "name",
            2: "target",
            3: "code",
            4: "params",
            5: "param1type",
            6: "param1desc",
            7: "param2type",
            8: "param2desc",
            9: "param3type",
            10: "param3desc",
            11: "param4type",
            12: "param4desc",
            13: "param5type",
            14: "param5desc",
            15: "param6type",
            16: "param6desc",
            17: "is_danger",
            18: "is_restricted",
            19: "desc",
            20: "note"
        }
        num_start_line = 4
        path_to_csv = settings["db_input_path"] / "CMD_DB"
        if settings["is_example"]:
            path_to_toml = settings["db_path"] / "CMD_DB" / "toml_example"
        else:
            path_to_toml = settings["db_path"] / "CMD_DB" / "toml"
        super().__init__(path_to_csv, path_to_toml, dict_index=dict_index, db_prefix="CMD_DB_CMD_DB", num_start_line=num_start_line, encoding=encoding, delimiter=delimiter)

    def make_data_init(self):
        self.prefix = ""
        self.is_code_init = False

    def make_data_main(self):
        data = self.data
        params = self.params
        _prefix = params["component"].replace("*", "").strip()
        if _prefix != "" and _prefix != self.prefix:
            self.prefix = _prefix
            row = next(self._f)
            row = [elem.replace("@@", ",") for elem in row]
            params = list2dict_with_dict_index(row, self.dict_index)
            if params["target"] == "":
                data[self.prefix] = []
                self.is_code_init = True
            else:
                data_next, code_init = self._parse_csv(params)
                data_next["code"] = code_init
                data[self.prefix] = [data_next]
            return
        if self.prefix == "" or params["target"] == "":
            return
        data_next, code_init = self._parse_csv(params)
        if self.is_code_init:
            data_next["code"] = code_init
            self.is_code_init = False
        data[self.prefix].append(data_next)

    def _parse_csv(self, params):
        dict_ = {"name": params["name"]}
        if params["code"] == "":
            dict_["is_no_code"] = True
        if "params" in params:
            if params["params"] == "":
                params["params"] = 0
            else:
                params["params"] = int(params["params"])
        add_dict_if_param_exists(dict_, params, "params")
        for i in range(1, 7):
            add_dict_if_param_exists(dict_, params, f"param{i}type")
            add_dict_if_param_exists(dict_, params, f"param{i}desc")
        add_dict_if_param_exists(dict_, params, "is_danger", True)
        add_dict_if_param_exists(dict_, params, "is_restricted", True)
        add_dict_if_param_exists(dict_, params, "desc")
        add_dict_if_param_exists(dict_, params, "note")
        return dict_, params["code"]


class Csv2TomlBCT(Csv2TomlBase):
    @ print_progress("bct csv to toml")
    def __init__(self, settings, db_prefix=None, encoding="cp932", delimiter=","):
        dict_index = {
            0: "comment",
            1: "name",
            2: "sname",
            3: "bcid",
            4: "is_deploy",
            5: "is_setblockposition",
            6: "is_clear",
            7: "is_activate",
            8: "is_inactivate",
            9: "is_danger",
            10: "desc",
            11: "note"
        }
        num_start_line = 2
        path_to_csv = settings["db_input_path"] / "CMD_DB"
        if settings["is_example"]:
            path_to_toml = settings["db_path"] / "CMD_DB" / "toml_example"
        else:
            path_to_toml = settings["db_path"] / "CMD_DB" / "toml"
        super().__init__(path_to_csv, path_to_toml, dict_index=dict_index, db_prefix="CMD_DB_BCT", num_start_line=num_start_line, encoding=encoding, delimiter=delimiter)

    def make_data_init(self):
        self.prefix = "bct"
        self.data[self.prefix] = []
        self.comment = ""
        self.has_comment = False

    def make_data_main(self):
        data = self.data
        params = self.params
        if "*" in params["comment"]:
            self.comment += params["name"] + "\n"
            self.has_comment = True
            return
        if self.has_comment:
            data[self.prefix].append({"comment": self.comment[:-1]})
            self.comment = ""
            self.has_comment = False
        data[self.prefix].append(self._parse_csv(params))

    def _parse_csv(self, params):
        # name & bitlen
        params["bcid"] = int(params["bcid"])
        dict_ = {
            "name": params["name"],
            "bcid": params["bcid"]
        }
        add_dict_if_param_exists(dict_, params, "sname")
        add_dict_if_param_exists(dict_, params, "is_deploy", True)
        add_dict_if_param_exists(dict_, params, "is_setblockposition", True)
        add_dict_if_param_exists(dict_, params, "is_clear", True)
        add_dict_if_param_exists(dict_, params, "is_activate", True)
        add_dict_if_param_exists(dict_, params, "is_inactivate", True)
        add_dict_if_param_exists(dict_, params, "is_danger", True)
        add_dict_if_param_exists(dict_, params, "desc")
        add_dict_if_param_exists(dict_, params, "note")
        return dict_
