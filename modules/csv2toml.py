import toml
import re
import copy
import csv
from .utils import get_path, typelist, dict_status
from abc import abstractmethod
from pathlib import Path


class Csv2TomlBase:
    def __init__(self, path_to_csv, path_to_toml, param_name, encoding="shift_jis", delimiter=",", obc="mobc"):
        self.encoding = encoding
        self.delimiter = delimiter
        self._param_name = param_name
        # パス取得
        p_list = get_path(path_to_csv, suffix="csv")

        for p in p_list:
            self.p = p
            print(f"-----converting {p}")
            # データ型を用意
            data = {"obc": obc.upper()}
            # 作成
            data = self.make_base_data(data)
            data = self.make_data(data)
            # 出力
            output_path_to_toml = Path(path_to_toml) / f"{p.stem}.toml"
            toml.dump(data, open(output_path_to_toml, mode='w'))
            # tomlファイル整形
            data = Path(output_path_to_toml).read_text()
            data = re.sub(r'(.\n)\[\[', r'\1\n[[', data)  # 空行を入れる
            data = re.sub(r'\n(\n\[\[.*?\..*?\]\])', r'\1', data)  # bit圧縮の場合は詰める
            Path(output_path_to_toml).write_text(data)

    @abstractmethod
    def make_base_data(self, data):
        pass

    @abstractmethod
    def make_data(self, data):
        pass


class Csv2TomlTLM(Csv2TomlBase):
    def __init__(self, path_to_csv, path_to_toml, param_name="tlm_field", encoding="shift_jis", delimiter=",", obc="mobc"):
        super().__init__(path_to_csv, path_to_toml, param_name, encoding, delimiter, obc)

    def _parse_csv(self, list_, is_comp=False):
        """list2dict"""
        # name & bitlen
        dict_ = {
            "name": list_[0],
            "bitlen": int(list_[6]) if list_[6].isdigit() else typelist[list_[1]],
        }
        # type
        if not is_comp:
            dict_["type"] = list_[1]
        # exp
        if list_[2] != "":
            dict_["exp"] = list_[2]
        # HEX
        if list_[7] == "HEX":
            dict_["is_hex"] = True
        # status
        if list_[14] != "":
            dict_["status"] = {}
            elems = list_[14].replace(" ", "").replace("@@", ",").split(",")
            for elem in elems:
                kv = elem.split("=")
                dict_["status"][kv[0]] = kv[1]
            for length, dict_status_ in dict_status.items():
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
                raise NameError(f"未定義のstatus: {dict_['status']}\n以下を`status.toml`に追加してください\n{example[:-1]}")
        # desc
        if list_[15] != "":
            dict_["desc"] = list_[15]
        # note
        if list_[16] != "":
            dict_["note"] = list_[16]
        return dict_

    def make_base_data(self, data):
        data[self._param_name] = []
        self._f = [row[1:] for row in csv.reader(open(self.p, "r", encoding=self.encoding), delimiter=self.delimiter)]
        if "" in [self._f[0][0], self._f[1][0], self._f[2][0], self._f[3][0], self._f[0][2],
                  self._f[0][1], self._f[1][1], self._f[2][1], self._f[3][1]]:
            raise ValueError(f"Target/PacketID/EnableDisable/IsRestricted is empty at {self.p}")
        # self._f[2][0] = self._f[2][0].replace("/", "") # Enable/Disableのスラッシュを消す
        # self._f[0][2] = self._f[0][2].replace(" ", "") # Var Localの空白を消す
        data[f"{self._f[0][0]}"] = self._f[0][1]
        data[f"{self._f[1][0]}"] = self._f[1][1]
        data[f"{self._f[2][0]}"] = self._f[2][1]
        data[f"{self._f[3][0]}"] = self._f[3][1]
        data[f"{self._f[0][2]}"] = self._f[1][2]
        del self._f[:8]
        return data

    def make_data(self, data):
        def get_exp_list(txt):
            txt = re.sub(r"^\((.?int\d{0,1}_t|float|double)\)\((.*)\)$", r"\2", txt.strip())  # (型)を消す
            txts = [_txt.strip() for _txt in txt.split("|")]
            exp_list = []
            for txt in txts:
                txt = re.sub(r"^\((.*)\s\<\<\s\d\)$", r"\1", txt).strip()  # ( ... << 4) を消す
                txt = re.sub(r"^\((.*)\s&\s0x..\)$", r"\1", txt).strip()  # ( ... & 0x00) を消す
                txt = re.sub(r"\s\<\<\s\d$", r"", txt).strip()  # << 4 を消す
                txt = re.sub(r"^\((.*)\)$", r"\1", txt).strip()
                exp_list.append(txt)
            return exp_list

        # toml用データ作成
        is_comp = False
        exp_list = []
        for row in self._f:
            if not any(row):  # 空行があればbreak
                break
            row[1] = "" if "||" in row[1] else row[1]  # ||は空白と同義
            if row[1] != "":  # 通常時
                # データ追加
                data[self._param_name].append(self._parse_csv(row))

                # bitlenは削除
                if len(data[self._param_name]) >= 2 and "bitlen" in data[self._param_name][-2]:
                    data[self._param_name][-2].pop("bitlen")

                # ビット圧縮ではない
                is_comp = False
            else:  # ビット圧縮の場合. 2行目からtypeが空白になる
                if not is_comp:  # ビット圧縮とわかる一つ前のデータを変更して追加
                    data_last = copy.deepcopy(data[self._param_name][-1])
                    data[self._param_name][-1].clear()
                    data[self._param_name][-1]["type"] = data_last.pop("type")

                    # expが結合された形の場合, 分割して配列に保持
                    if "exp" in data_last and "|" in data_last["exp"]:
                        exp_list = get_exp_list(data_last["exp"])

                    data[self._param_name][-1]["comp"] = [data_last]
                    is_comp = True

                # expの配列があれば順に入れる
                if len(exp_list) != 0:
                    row[2] = exp_list.pop(0)

                # ビット圧縮の場合のデータ追加
                data[self._param_name][-1]["comp"].append(self._parse_csv(row, True))

        # 最終行の"bitlen"が残っているので削除
        if "bitlen" in data[self._param_name][-1]:
            data[self._param_name][-1].pop("bitlen")

        return data


class Csv2TomlCMD(Csv2TomlBase):
    def __init__(self, path_to_csv, path_to_toml, param_name="cmd", encoding="shift_jis", delimiter=",", obc="mobc"):
        super().__init__(path_to_csv, path_to_toml, param_name, encoding, delimiter, obc)

    def make_base_data(self, data):
        self._f = [row for row in csv.reader(open(self.p, "r", encoding=self.encoding), delimiter=self.delimiter)]
        del self._f[:4]
        return data

    def make_data(self, data):
        prefix = ""
        self._f = iter(self._f)
        for row in self._f:
            if not any(row):
                break
            _prefix = row[0].replace("*", "").strip()
            if _prefix != "" and _prefix != prefix:
                prefix = _prefix
                row = next(self._f)
                if row[2] == "":
                    data[prefix] = []
                else:
                    data_next, code_init = self._parse_csv(row)
                    data_next["code"] = code_init
                    data[prefix] = [data_next]
                continue
            if prefix == "" or row[2] == "":
                continue
            data_next, _ = self._parse_csv(row)
            data[prefix].append(data_next)
        return data

    def _parse_csv(self, list_):
        list_ = [elem.replace("@@", ",") for elem in list_]
        """list2dict"""
        # name & bitlen
        dict_ = {
            "name": list_[1],
        }
        if list_[3] == "":
            dict_["is_no_code"] = True
        if list_[17] != "":
            dict_["is_danger"] = True
        if list_[18] != "":
            dict_["is_restricted"] = True
        if list_[19] != "":
            dict_["desc"] = list_[19]
        if list_[20] != "":
            dict_["note"] = list_[20]

        if list_[5] != "":
            dict_["params"] = []
        for i in range(6):
            if list_[i * 2 + 5] != "":
                dict_param = {"type": list_[i * 2 + 5]}
                if list_[i * 2 + 6] != "":
                    dict_param["desc"] = list_[i * 2 + 6]
                dict_["params"].append(dict_param)
            else:
                break
        return dict_, list_[3]
