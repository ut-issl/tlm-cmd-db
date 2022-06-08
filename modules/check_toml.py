import re
import toml
import copy
from abc import abstractmethod, ABCMeta

from .utils import get_path_list, type2bit, print_progress, err
from .convert_toml import Toml2MdStatus, Toml2MdTLM, Toml2CsvTLM, Toml2MdSGC, Toml2CsvSGC, Toml2MdBCT, Toml2CsvBCT
from .check_base import *


def add_dict_if_param_exists(dict_, params, k, alt=None):
    if k in params and params[k] != "":
        dict_[k] = params[k] if alt is None else alt


class CheckTomlBase(metaclass=ABCMeta):
    def __init__(self, is_tlm=False, is_sgc=False, is_bct=False):
        self.is_tlm = is_tlm
        self.is_sgc = is_sgc
        self.is_bct = is_bct

    def init(self, p):
        self.p = p
        if self.is_bct:
            self.bcids = []
        self.packet = 0
        self._dict = toml.load(open(p, encoding="utf-8"))
        self._dict_expand = {}

    def get_settings(self):
        return self.settings

    def expand(self):
        (self.p.parent / "expanded").mkdir(exist_ok=True)
        _dict_output = self.make_output_data()

        output_path = self.p.parent / "expanded" / self.p.name
        toml.dump(_dict_output, open(output_path, mode='w', encoding="utf-8"))
        _dict_output_str = output_path.read_text()
        _dict_output_str = re.sub(r'(.\n)\[\[', r'\1\n[[', _dict_output_str)
        _dict_output_str = re.sub(r'\n\n\[\[(.*?\.)', r'\n[[\1', _dict_output_str)
        output_path.write_text(_dict_output_str)
        return _dict_output

    @abstractmethod
    def make_output_data(self):
        pass

    def check(self):
        for k, data in self._dict.items():
            self.key = k
            self._list_expand = []
            if isinstance(data, list):
                for _data in data:
                    self.add_expand(_data)
                self._dict_expand[self.key] = self._list_expand
            else:
                self._dict_expand[self.key] = data

    def check_meta(self):
        pass

    def _err(self, data, txt):
        return err(self.p, data, txt)

    def check_common(self):
        pass

    @abstractmethod
    def _add(self, data):
        pass

    def _add_comp(self, data, expand_option, is_seq=False):
        data_expand = copy.deepcopy(data)
        data_expand["comp"] = []
        data_expand["bitlen"] = []
        data_expand["type"] = expand_option["type"]
        for data_comp in data["comp"]:
            expand_option_comp = copy.deepcopy(expand_option)
            expand_option_comp = self.check_expand_option(data_comp, expand_option_comp)
            if is_seq:
                expand_option_comp = self._add_seq_option(data_comp, expand_option_comp)
                data_expand_comp = self._add_seq_data(data_comp, expand_option_comp)
            if "block" in data_comp:
                data_expand_comp = self._add_block(data_comp, expand_option_comp)
            elif "seq" in data_comp:
                data_expand_comp = self._add_seq(data_comp, expand_option_comp)
            else:
                data_expand_comp = [self.data_replace(data_comp, expand_option_comp)]
            for data_expand_comp_ in data_expand_comp:
                data_expand["bitlen"].append(data_expand_comp_["bitlen"])
            data_expand["comp"].extend(data_expand_comp)
        else:
            expand_option_comp = copy.deepcopy(expand_option)
            expand_option_comp = self.check_expand_option(data_expand, expand_option_comp)
        data_expand = self.data_replace(data_expand, expand_option)
        self._add(data_expand)

    def add_expand(self, data):
        if self.is_tlm:
            expand_option = {"layer": [], "block": 0, "seq": 0, "comp": 0, "need_exp": False, "name_base": "", "exp_base": "",
                             "block_seq_name": "", "block_seq_exp": "", "seq_name": "", "seq_exp": "", "q1": "", "q2": "", "type": ""}
        else:
            expand_option = {"layer": [], "block": 0, "seq": 0, "name_base": "",
                             "block_seq_name": "", "seq_name": "", "q1": "", "q2": ""}
        # layer: 階層把握
        # block, seq, comp: それぞれ何度呼ばれたか
        # need_exp: expが定義されている必要があるか
        # name_base, exp_base: seq前の情報の保持
        # block_seq_name/block_seq_exp: {{}}の置換先
        # seq_name/seq_exp: {}の置換先
        # q1: ??の置換先
        # q2: ????の置換先
        # type: 型
        expand_option = self.check_expand_option(data, expand_option)

        if expand_option["layer"] == []:
            self._add(data)
        elif self.is_tlm and expand_option["comp"] == 1:
            self._add_comp(data, expand_option)
        elif expand_option["layer"] == ["block_seq"]:
            for data_seq in data["seq"]:
                q_range = data_seq["q_range"] if data_seq["q_range"] != [] else [0, 0]
                expand_option["block_seq_name"] = data_seq["name"]
                if self.is_tlm and "exp" in data_seq:
                    expand_option["block_seq_exp"] = data_seq["exp"]
                    expand_option["need_exp"] = True
                data_ = copy.deepcopy(data)
                data_["q_range"] = q_range
                self._add_block(data_, expand_option)
        elif expand_option["block"] == 1:
            self._add_block(data, expand_option)
        elif expand_option["seq"] == 1:
            self._add_seq(data, expand_option)
        else:
            raise ValueError("予期していない挙動です. 開発者に報告してください")

    def _add_seq_option(self, data, expand_option):
        expand_option["seq_name"] = data["name"]
        if self.is_tlm:
            expand_option["seq_exp"] = data["exp"] if "exp" in data else ""
        return expand_option

    def _add_seq_data(self, data, expand_option, is_block=False):
        suffix = "_base" if is_block else ""
        data[f"name{suffix}"] = expand_option["name_base"]
        if self.is_tlm and "exp_base" in expand_option and expand_option["exp_base"] != "":
            data[f"exp{suffix}"] = expand_option["exp_base"]
        return data

    def _add_common(self, data, expand_option, data_comp_list=[], is_seq=False):
        expand_option_common = copy.deepcopy(expand_option)
        expand_option_common = self.check_expand_option(data, expand_option_common)  # option確認
        data_expand = copy.deepcopy(data)

        if self.is_tlm and expand_option["comp"] == 1:
            if is_seq:
                expand_option_common = self._add_seq_option(data_expand, expand_option_common)
                data_expand = self._add_seq_data(data_expand, expand_option_common)
            data_expand = self.data_replace(data_expand, expand_option_common)
            data_comp_list.append(data_expand)
            return data_comp_list

        elif expand_option["seq"] == 1 and not is_seq:  # seq.block
            expand_option_common = self._add_seq_option(data_expand, expand_option_common)
            data_expand = self._add_seq_data(data_expand, expand_option_common)
            data_expand = self.data_replace(data_expand, expand_option_common)
            if self.is_tlm:
                data_expand["type"] = expand_option_common["type"]
            self._add(data_expand)

        elif "block" in data:  # block.block
            if is_seq:
                data_expand = self._add_seq_data(data_expand, expand_option_common, is_block=is_seq)
            self._add_block(data, expand_option_common)

        elif "seq" in data and not is_seq:  # block.seq
            self._add_seq(data, expand_option_common)

        elif self.is_tlm and "comp" in data:
            self._add_comp(data, expand_option_common, is_seq=is_seq)

        else:
            if is_seq:
                expand_option_common = self._add_seq_option(data_expand, expand_option_common)
                data_expand = self._add_seq_data(data_expand, expand_option_common)
            data_expand = self.data_replace(data_expand, expand_option_common)
            if self.is_tlm:
                data_expand["type"] = expand_option_common["type"]
            self._add(data_expand)

    def _add_seq(self, data, expand_option):
        data_expand_list = [] if self.is_tlm and expand_option["comp"] == 1 else None

        for data_seq in data["seq"]:  # 各seq内
            data_expand_list = self._add_common(copy.deepcopy(data_seq), expand_option, data_comp_list=data_expand_list, is_seq=True)
        else:
            if self.is_tlm and expand_option["comp"] == 1:
                return data_expand_list

    def _add_block(self, data, expand_option):
        data_expand_list = [] if self.is_tlm and expand_option["comp"] == 1 else None

        if expand_option["block"] == 2:
            if len(data["q_range"]) == 3 and data["q_range"][2] == 1:  # [0, 7, 1]といった場合
                q_range = data["q_range"][1] - data["q_range"][0] + 1
                data["q_range"][0] = q_range * expand_option["q1"]
                data["q_range"][1] = q_range * (expand_option["q1"] + 1) - 1

        for q in range(data["q_range"][0], data["q_range"][1] + 1):
            q_key = "q2" if expand_option["block"] == 2 else "q1"
            expand_option[q_key] = q
            for data_block in data["block"]:  # 各block内
                data_expand_list = self._add_common(copy.deepcopy(data_block), expand_option, data_comp_list=data_expand_list)
        else:
            if self.is_tlm and expand_option["comp"] == 1:
                return data_expand_list

    def check_expand_option(self, data, expand_option):
        if "block_num" in data and "seq_num" in data:  # tlm.block, tlm.seq
            assert expand_option["layer"] == [], self._err(data, "同じ階層にblockとseqを定義できるのは最初の階層のみです.")
            for data_seq in data["seq"]:
                assert "q_range" in data_seq, self._err(data, "[[root.seq]]の中でq_rangeを定義してください")
                assert "name" in data_seq, self._err(data, "[[root.seq]]の中でnameを定義してください")
                if self.is_tlm:
                    assert "exp" in data_seq, self._err(data, 'expが存在しない場合も[[tlm.seq]]の中でexp=""として指定してください')

            check_all_params(["block_num", "seq_num", "block", "seq"], "block_numとseq_num", data, self.p)
            check_block_num(data, self.p)
            check_seq_num(data, self.p)

            expand_option["layer"].append("block_seq")
            expand_option["block"] += 1

        elif "block_num" in data:
            check_not_seq_block_block(data, expand_option, self.p)
            check_not_block_3(data, expand_option, self.p)
            if expand_option["seq"] == 0:
                if self.is_tlm:
                    check_all_params(["q_range", "block_num", "block", "type"], "block_numとq_rangeとtype", data, self.p)
                else:
                    check_all_params(["q_range", "block_num", "block"], "block_numとq_range", data, self.p)
            check_no_seq(data, self.p)
            check_param_before("block", "q_range", data, self.p)
            check_block_num(data, self.p)
            if self.is_tlm:
                check_type(data, expand_option, self.p)

            expand_option["layer"].append("block")
            expand_option["block"] += 1

        elif "seq_num" in data:
            check_seq_once(data, expand_option, self.p)
            check_no_block(data, self.p)
            if self.is_tlm:
                check_all_params(["name_base", "exp_base", "seq_num", "type", "seq"], "name/exp_baseとseq_numとtype", data, self.p)
            else:
                check_all_params(["name_base", "seq_num", "seq"], "name_baseとseq_num", data, self.p)
            check_param_before("seq", "name_base", data, self.p)
            check_seq_num(data, self.p)
            if self.is_tlm:
                check_type(data, expand_option, self.p)

            if self.is_tlm and "exp_base" in data:
                expand_option["need_exp"] = True
                expand_option["exp_base"] = data["exp_base"]
            expand_option["name_base"] = data["name_base"]
            expand_option["layer"].append("seq")
            expand_option["seq"] += 1

        elif self.is_tlm and "comp" in data and "bitlen" in data and expand_option["comp"] == 1:
            check_bit_comp(data, self.p)
        elif self.is_tlm and "comp" in data:
            check_comp_once(data, expand_option, self.p)
            check_type(data, expand_option, self.p, is_last=True)

            expand_option["layer"].append("comp")
            expand_option["comp"] += 1
        else:
            check_no_block(data, self.p)
            check_no_seq(data, self.p)
            if self.is_tlm:
                check_name_base_not_in(data, self.p)
                check_param("name", data, self.p)
            if self.is_sgc:
                check_param("name", data, self.p)
                check_param("params", data, self.p)
                check_sgc_params(data, self.p)
            if self.is_bct:
                if "comment" in data:
                    check_only_comment(data, self.p)
                    return expand_option

            if len(expand_option["layer"]) != 0:
                if self.is_tlm:
                    if expand_option["comp"] == 1:
                        check_name_base_bracket_num(data, expand_option, self.p)
                        check_param_in("comp", "bitlen", data, self.p)
                        check_param_not_in("comp", "type", data, self.p)
                    else:
                        check_tlm_poly(data, self.p)

                    if expand_option["layer"][-1] == "seq":
                        check_name_base_bracket_num(data, expand_option, self.p)
                        if expand_option["need_exp"]:
                            check_exp_after_exp_base(data, self.p)
                            check_exp_base_bracket_num(data, expand_option, self.p)
                        check_exp_without_exp_base(data, expand_option, self.p)
                        check_type(data, expand_option, self.p, is_last=True)

                    elif expand_option["layer"][-1] in ["block", "block_seq"]:
                        if expand_option["need_exp"]:
                            check_exp_after_exp_base(data, self.p)
                        check_type(data, expand_option, self.p, is_last=True)
                elif self.is_sgc:
                    if expand_option["layer"][-1] == "seq":
                        check_name_base_bracket_num(data, expand_option, self.p)
                elif self.is_bct:
                    check_param("name", data, self.p)
                    check_param("bcid", data, self.p)
                    if expand_option["layer"][-1] == "seq":
                        check_name_base_bracket_num(data, expand_option, self.p)
            else:
                if self.is_tlm:
                    check_param_in("tlm", "type", data, self.p)
                    check_tlm_poly(data, self.p)

        return expand_option

    def data_replace(self, data, expand_option):
        if self.is_tlm:
            keys = ["name", "exp"]
        else:
            keys = ["name"]
        for key in keys:
            if key in data:
                if self.is_tlm:
                    check_data_replace_type(data, key, expand_option, self.p)
                check_data_replace_block_seq(data, key, expand_option, self.p)
                check_data_replace_block(data, key, expand_option, self.p)

                data[key] = data[key].replace("{{}}", expand_option[f"block_seq_{key}"])
                if isinstance(expand_option[f"seq_{key}"], list):
                    for expand_option_seq in expand_option[f"seq_{key}"]:
                        data[key] = data[key].replace("{}", expand_option_seq, 1)
                else:
                    data[key] = data[key].replace("{}", expand_option[f"seq_{key}"])
                if self.is_tlm:
                    data[key] = data[key].replace("{type}", f'({expand_option["type"]})')
                data[key] = data[key].replace("????", str(expand_option["q2"])).replace("??", str(expand_option["q1"]))
        if self.is_bct and "bcid" in data:
            data["bcid"] = int(data["bcid"].replace("????", str(expand_option["q2"])).replace("??", str(expand_option["q1"])))
        return data


class CheckTomlTLM(CheckTomlBase):
    @print_progress("check tlm toml")
    def __init__(self, setting, param_name="tlm"):
        self._param_name = param_name
        super().__init__(is_tlm=True)
        self.max_tlm_num = setting["max_tlm_num"]
        toml2md = Toml2MdTLM
        toml2csv = Toml2CsvTLM
        setting["dict_status"] = Toml2MdStatus(setting["db_path"] / "TLM_DB" / "status.toml", setting).get_status()
        path_to_toml = setting["db_path"] / "TLM_DB" / "toml"
        path_to_md = setting["db_path"] / "TLM_DB" / "md"
        path_to_csv = setting["db_path"] / "TLM_DB" / "csv"
        db_prefix = f'{setting["db_prefix"]}_TLM_DB'

        self.p_list = get_path_list(path_to_toml, db_prefix=db_prefix, suffix="toml")  # パスリスト取得
        assert len(self.p_list) != 0, f"指定されたディレクトリ{path_to_toml}にtomlファイルが存在しません"
        self.db_prefix = db_prefix

        check_toml_base_exists(self.p_list, self.db_prefix)

        for p in self.p_list:
            if f"{self.db_prefix}.toml" in str(p):  # 共通部分をまとめたファイルの読み込み
                self.init(p)  # 初期化
                self.names = []
                self.check()  # 文法チェック
                self.names_common = copy.deepcopy(self.names)

                self.packet_common = copy.deepcopy(self.packet)
                self._dict_expand_common = copy.deepcopy(self._dict_expand)
                self.p_list.remove(p)  # ファイルリストから除く
                break

        setting["data"] = {}
        setting["data"]["tlm"] = []
        for p in self.p_list:  # 各ファイルを読み込み
            print(f"--- {p}")
            print("------checking")
            self.names = copy.deepcopy(self.names_common)
            self.init(p)  # 初期化
            self.check_meta()  # パラメタチェック
            self.check()  # 文法チェック
            self.check_max_tlm_num()

            print("------expanding")
            _dict_output = self.expand()  # 展開

            print(f"------converting to {p.stem}.md")
            to_md = toml2md(p, _dict_output, path_to_md, setting)
            to_md.add()
            to_md.write()

            print(f"------converting to {p.stem}.csv")
            to_csv = toml2csv(p, _dict_output, path_to_csv, setting)
            to_csv.add()
            to_csv.write()
            setting["data"]["tlm"].append(p.parent / "expanded" / p.name)
        self.settings = setting

    def check_max_tlm_num(self):
        check_max_tlm_num(self.packet + self.packet_common, self.max_tlm_num)

    def make_output_data(self):
        _dict_output = {}
        _dict_output["Target"] = self._dict["Target"]
        _dict_output["PacketID"] = self._dict["PacketID"]
        _dict_output["Enable/Disable"] = self._dict["Enable/Disable"]
        _dict_output["IsRestricted"] = self._dict["IsRestricted"]
        _dict_output["Local Var"] = self._dict["Local Var"]
        _dict_output[self._param_name] = []
        if self._param_name in self._dict_expand_common:
            _dict_output[self._param_name] = copy.deepcopy(self._dict_expand_common)[self._param_name]
        _dict_output[self._param_name] += self._dict_expand[self._param_name]
        return _dict_output

    def check_meta(self):
        # 上の4行は必ず必要
        assert "Target" in self._dict, self._err("Target", 'Targetが定義されていません. 以下のように定義してください\nTarget = "OBC"')
        assert "PacketID" in self._dict, self._err("PacketID", 'PacketIDが定義されていません. 以下のように定義してください\nPacketID="0x00"')
        assert "Enable/Disable" in self._dict, self._err("EnableDisable", 'EnableDisableが定義されていません. 以下のように定義してください\nEnableDisable = "ENABLE"')
        assert "IsRestricted" in self._dict, self._err("IsRestricted", 'IsRestrictedが定義されていません. 以下のように定義してください\nIsRestricted = "FALSE"')
        assert "Local Var" in self._dict, self._err("Local Var", 'Local Varが定義されていません. 存在しない場合も以下のように定義してください\n"Local Var"=""')
        assert "tlm" in self._dict, self._err("tlm", "[[tlm]]が存在しません")
        assert len(self._dict.keys()) == 6, self._err(self._dict.keys(), "Target, PacketID, Enable/Disable, IsRestricted, Local Var, tlm以外のキーは指定できません")

    def check_common(self, data):
        check_type_exists(data, self.p)
        check_hex_status_poly(data, self.p)
        self.names = check_data_name_duplicate(data, self.names, self.p)
        if "exp" in data:
            check_exp_brackets(data, self.p)

    def _add(self, data):
        data_expand = {}
        self.check_common(data)
        add_dict_if_param_exists(data_expand, data, "type")
        add_dict_if_param_exists(data_expand, data, "name")
        add_dict_if_param_exists(data_expand, data, "exp")
        add_dict_if_param_exists(data_expand, data, "is_hex", True)
        add_dict_if_param_exists(data_expand, data, "status")
        for i in range(6):
            add_dict_if_param_exists(data_expand, data, f"a{i}")
        add_dict_if_param_exists(data_expand, data, "desc")
        add_dict_if_param_exists(data_expand, data, "note")
        add_dict_if_param_exists(data_expand, data, "comp")
        self.packet += type2bit[data["type"]] / 8
        self._list_expand.append(data_expand)


class CheckTomlSGC(CheckTomlBase):
    @print_progress("check tlm sgc")
    def __init__(self, setting):
        toml2md = Toml2MdSGC
        toml2csv = Toml2CsvSGC
        super().__init__(is_sgc=True)
        path_to_toml = setting["db_path"] / "CMD_DB" / "toml"
        path_to_md = setting["db_path"] / "CMD_DB" / "md"
        path_to_csv = setting["db_path"] / "CMD_DB" / "csv"
        db_prefix = f'{setting["db_prefix"]}_CMD_DB_CMD_DB'

        self.p_list = get_path_list(path_to_toml, db_prefix=db_prefix, suffix="toml")  # パスリスト取得
        assert len(self.p_list) != 0, f"指定されたディレクトリ{path_to_toml}に{db_prefix}.tomlファイルが存在しません"
        p = self.p_list[0]

        print(f"--- {p}")
        print("------checking")
        self.names = []
        self.init(p)  # 初期化
        self.check_meta()  # パラメタチェック
        self.check()  # 文法チェック

        print("------expanding")
        _dict_output = self.expand()  # 展開

        print(f"------converting to {p.stem}.md")
        to_md = toml2md(p, _dict_output, path_to_md)
        to_md.add()
        to_md.write()

        print(f"------converting to {p.stem}.csv")
        to_csv = toml2csv(p, _dict_output, path_to_csv)
        to_csv.add()
        to_csv.write()

        setting["data"]["sgc"] = p.parent / "expanded" / p.name
        self.settings = setting

    def make_output_data(self):
        _dict_output = {}
        _dict_output = self._dict_expand
        return _dict_output

    def check_common(self, data):
        if data["params"] != 0:
            for i in range(data["params"]):
                assert data[f"param{i+1}type"] in list(type2bit.keys()) + ["raw"], self._err(data, f'typeに指定した{data[f"param{i+1}type"]}は存在しません.\n{list(type2bit.keys()) + ["raw"]}の中から指定してください.')
        assert data["name"] not in self.names, self._err(data, "nameに重複があります, ????と??などを確認してください")
        self.names.append(data["name"])

    def _add(self, data):
        data_expand = {}
        self.check_common(data)
        add_dict_if_param_exists(data_expand, data, "code")
        add_dict_if_param_exists(data_expand, data, "name")
        add_dict_if_param_exists(data_expand, data, "is_no_code")
        add_dict_if_param_exists(data_expand, data, "params")
        for i in range(1, 7):
            add_dict_if_param_exists(data_expand, data, f"param{i}type")
            add_dict_if_param_exists(data_expand, data, f"param{i}desc")
        add_dict_if_param_exists(data_expand, data, "is_danger", True)
        add_dict_if_param_exists(data_expand, data, "is_restricted", True)
        add_dict_if_param_exists(data_expand, data, "desc")
        add_dict_if_param_exists(data_expand, data, "note")
        self._list_expand.append(data_expand)


class CheckTomlBCT(CheckTomlBase):
    @print_progress("check tlm bct")
    def __init__(self, setting, param_name="bct"):
        toml2md = Toml2MdBCT
        toml2csv = Toml2CsvBCT
        super().__init__(is_bct=True)
        self._param_name = param_name
        path_to_toml = setting["db_path"] / "CMD_DB" / "toml"
        path_to_md = setting["db_path"] / "CMD_DB" / "md"
        path_to_csv = setting["db_path"] / "CMD_DB" / "csv"
        db_prefix = f'{setting["db_prefix"]}_CMD_DB_BCT'

        self.p_list = get_path_list(path_to_toml, db_prefix=db_prefix, suffix="toml")  # パスリスト取得
        assert len(self.p_list) != 0, f"指定されたディレクトリ{path_to_toml}に{db_prefix}.tomlファイルが存在しません"
        p = self.p_list[0]

        print(f"--- {p}")
        print("------checking")
        self.names = []
        self.init(p)  # 初期化
        self.check_meta()  # パラメタチェック
        self.check()  # 文法チェック

        print("------expanding")
        _dict_output = self.expand()  # 展開

        print(f"------converting to {p.stem}.md")
        to_md = toml2md(p, _dict_output, path_to_md)
        to_md.add()
        to_md.write()

        print(f"------converting to {p.stem}.csv")
        to_csv = toml2csv(p, _dict_output, path_to_csv)
        to_csv.add()
        to_csv.write()

        setting["data"]["bct"] = p.parent / "expanded" / p.name
        self.settings = setting

    def check_meta(self):
        assert self._param_name in self._dict, self._err(self._param_name, f"[[{self._param_name}]]が存在しません")
        assert len(self._dict.keys()) == 1, self._err(self._dict.keys(), f"{self._param_name}以外をキーに持つことはできません")

    def make_output_data(self):
        _dict_output = {}
        _dict_output[self._param_name] = self._dict_expand[self._param_name]
        return _dict_output

    def check_common(self, data):
        assert data["name"] not in self.names, self._err(data, "nameに重複があります, ????と??などを確認してください")
        self.names.append(data["name"])
        if "??" not in str(data["bcid"]):
            assert data["bcid"] not in self.bcids, self._err(data, "bcidに重複があります")
            self.bcids.append(data["bcid"])

    def _add(self, data):
        data_expand = {}
        if "comment" in data:
            add_dict_if_param_exists(data_expand, data, "comment")
        else:
            self.check_common(data)
            add_dict_if_param_exists(data_expand, data, "name")
            add_dict_if_param_exists(data_expand, data, "sname")
            add_dict_if_param_exists(data_expand, data, "bcid")
            add_dict_if_param_exists(data_expand, data, "is_deploy", True)
            add_dict_if_param_exists(data_expand, data, "is_setblockposition", True)
            add_dict_if_param_exists(data_expand, data, "is_clear", True)
            add_dict_if_param_exists(data_expand, data, "is_activate", True)
            add_dict_if_param_exists(data_expand, data, "is_inactivate", True)
            add_dict_if_param_exists(data_expand, data, "is_danger", True)
            add_dict_if_param_exists(data_expand, data, "desc")
            add_dict_if_param_exists(data_expand, data, "note")
        self._list_expand.append(data_expand)
