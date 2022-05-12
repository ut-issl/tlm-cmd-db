from pathlib import Path
import toml
from .convert_base import TLMBase, SGCBase
from .utils import print_progress, err, type2bit, get_exp_comp


class Toml2MdStatus:
    @print_progress("status.toml to status.md")
    def __init__(self, path_to_status_toml, setting):
        self.p = path_to_status_toml
        dict_status_tmp = toml.load(open(path_to_status_toml, encoding="utf-8"))
        assert "status" in dict_status_tmp, err(path_to_status_toml, "status", "[status]が存在しません")
        assert len(dict_status_tmp.keys()) == 1, err(path_to_status_toml, dict_status_tmp.keys(), "status以外のキーは指定できません")
        self.dict_status = dict_status_tmp["status"]
        setting["dict_status"] = self.dict_status

        self.txt = self.header_generator()
        self._path_to_md = path_to_status_toml.parent / (str(path_to_status_toml.stem) + '.md')
        print(f"---{self.p}")
        print("------checking")
        self.check()
        self.check_meta()

        print(f"------converting to {self._path_to_md}")
        self.add()
        self.write()

    def get_status(self):
        return self.dict_status

    def write(self):
        Path(self._path_to_md).write_text(self.txt, encoding="utf-8", errors="ignore")

    def header_generator(self):
        return """# Status Table\n
Length|Index|Status
-|-|-
"""

    def add(self):
        for length, dict_status_ in self.dict_status.items():
            for index, status in dict_status_.items():
                self.txt += f'{length}|{index}|{status}\n'
            else:
                continue

    def check_meta(self):
        pass

    def check(self):
        for length, dict_status_ in self.dict_status.items():
            for index, status in dict_status_.items():
                for status_index in status:
                    assert status_index.isdigit() or status_index == "*" or isinstance(int(status_index, 0), int), err(self.p, {f'status.{length}.{index}': status}, f'キーには整数(2,8,16進数含む)とアスタリスク(*)のみ使用できます')


class Toml2MdTLM(TLMBase):
    def __init__(self, p, _dict, path_to_md, setting, param_name="tlm", encoding="utf-8"):
        self.p = p
        self._dict = _dict
        self._path_to_md = path_to_md
        self._param_name = param_name
        self.dict_status = setting["dict_status"]
        self.encoding = encoding
        self.txt = self.header_generator()

        super().__init__()

    def write(self):
        (Path(self._path_to_md) / f"{self.p.stem}.md").write_text(self.txt, encoding=self.encoding, errors="ignore")

    def header_generator(self):
        return f"""# {self.p.stem}\n
Name|Type|Exp.|Octet Pos.|bit Pos.|bit Len.|HEX|Status|a0|a1|a2|a3|a4|a5|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
"""

    def add(self):
        TLMBase.__init__(self)
        for data in self._dict[self._param_name]:
            self.data = data
            if "comp" in data:
                self.add_comp()
            else:
                self.update_pos()
                self.add_name()
                self.add_type()
                self.add_exp()
                self.add_pos()
                self.add_hex()
                self.add_status()
                self.add_poly()
                self.add_desc_note()
                self.txt += "\n"

    def add_comp(self):
        is_comp_init = True
        for data in self.data["comp"]:
            self.update_pos(data=data, is_comp=True)
            self.add_name(data=data)
            if is_comp_init:
                self.add_type()
                self.add_exp()
                is_comp_init = False
            else:
                self.txt += "||"
            self.add_pos()
            self.add_hex(data=data)
            self.add_status(data=data)
            self.add_poly(data=data)
            self.add_desc_note(data=data)
            self.txt += "\n"

    def add_name(self, data=None):
        data = self.data if data is None else data
        self.txt += f'{data["name"]}|'

    def add_type(self, data=None):
        data = self.data if data is None else data
        self.txt += f'{data["type"]}|'

    def add_exp(self, data=None):
        data = self.data if data is None else data
        self.txt += f'{data["exp"].replace("|", "&#124;")}|' if "exp" in data else "|"

    def add_pos(self):
        self.txt += f'{self.octet_pos}|{self.bit_pos}|{self.bit_len}|'

    def add_hex(self, data=None):
        data = self.data if data is None else data
        self.txt += 'o|' if "is_hex" in data and data["is_hex"] else "|"

    def add_status(self, data=None):
        data = self.data if data is None else data
        self.txt += f'{data["status"]}|' if "status" in data else "|"

    def add_poly(self, data=None):
        data = self.data if data is None else data
        for i in range(6):
            if f"a{i}" in data:
                self.txt += f'{str(data["a" + str(i)])}|'
            else:
                self.txt += "|"

    def add_desc_note(self, data=None):
        data = self.data if data is None else data
        self.txt += f'{data["desc"]}|' if "desc" in data else "|"
        self.txt += f'{data["note"]}|' if "note" in data else "|"


class Toml2CsvTLM(TLMBase):
    def __init__(self, p, _dict, path_to_csv, setting, param_name="tlm", encoding="cp932"):
        self.p = p
        self._dict = _dict
        self._path_to_csv = path_to_csv
        self._param_name = param_name
        self.dict_status = setting["dict_status"]
        self.encoding = encoding
        self.txt = self.header_generator()

        super().__init__()

    def write(self):
        (Path(self._path_to_csv) / f"{self.p.stem}.csv").write_text(self.txt, encoding=self.encoding, errors="ignore")

    def header_generator(self):
        return f""",Target,{self._dict["Target"]},Local Var,,,,,,,,,,,,,,
,PacketID,{self._dict["PacketID"]},{self._dict["Local Var"]},,,,,,,,,,,,,,
,Enable/Disable,{self._dict["Enable/Disable"]},,,,,,,,,,,,,,,
,IsRestricted,{self._dict["IsRestricted"]},,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,
Comment,TLM Entry,Onboard Software Info.,,Extraction Info.,,,,Conversion Info.,,,,,,,,Description,Note
,Name,Var.%%##Type,Variable or Function Name,Ext.%%##Type,Pos. Desiginator,,,Conv.%%##Type,Poly (��a_i * x^i),,,,,,Status,,
,,,,,Octet%%##Pos.,bit%%##Pos.,bit%%##Len.,,a0,a1,a2,a3,a4,a5,,,
"""

    def add(self):
        TLMBase.__init__(self)
        for data in self._dict[self._param_name]:
            self.data = data
            if "comp" in data:
                self.add_comp()
            else:
                self.update_pos()
                self.add_name()
                self.add_type()
                self.add_exp()
                self.add_pos()
                self.add_conv()
                self.add_desc_note()
                self.txt += "\n"

    def add_comp(self):
        is_comp_init = True
        exp = get_exp_comp(self.data)
        if exp is not None:
            self.data["exp"] = exp

        for data in self.data["comp"]:
            self.update_pos(data=data, is_comp=True)
            self.add_name(data=data)
            if is_comp_init:
                self.add_type()
                if "exp" in self.data:
                    self.add_exp()
                else:
                    self.add_exp(data=data)
                is_comp_init = False
            else:
                self.txt += ","
                self.add_exp(data=data)
            self.add_pos()
            self.add_conv(data=data)
            self.add_desc_note(data=data)
            self.txt += "\n"

    def add_name(self, data=None):
        data = self.data if data is None else data
        self.txt += f',{data["name"]},'

    def add_type(self, data=None):
        data = self.data if data is None else data
        self.txt += f'{data["type"]},'

    def add_exp(self, data=None):
        data = self.data if data is None else data
        self.txt += f'{data["exp"].replace(",", "@@")},PACKET,' if "exp" in data else ",PACKET,"

    def add_pos(self):
        self.txt += f'{self.octet_pos},{self.bit_pos},{self.bit_len},'

    def add_conv(self, data=None):
        data = self.data if data is None else data
        conv = "NONE,,,,,,,"
        if "is_hex" in data and data["is_hex"]:
            conv = "HEX,,,,,,,"
        elif "status" in data:
            index = data["status"].split(".")
            status_txt = ""
            for k, v in self.dict_status[index[0]][index[1]].items():
                status_txt += f"{k}={v}@@ "
            conv = f"STATUS,,,,,,,{status_txt[:-3]}"
        elif "a0" in data:
            poly_txt = ""
            for i in range(6):
                if f"a{i}" in data:
                    poly_txt += f'{str(data["a" + str(i)])},'
                else:
                    poly_txt += ","
            conv = f'POLY,' + poly_txt
        self.txt += f"{conv}"

    def add_desc_note(self, data=None):
        data = self.data if data is None else data
        self.txt += f',{data["desc"]}' if "desc" in data else ","
        self.txt += f',{data["note"]}' if "note" in data else ","


class Toml2MdSGC(SGCBase):
    def __init__(self, p, _dict, path_to_md, encoding="utf-8"):
        self.p = p
        self._dict = _dict
        self._path_to_md = path_to_md
        self.encoding = encoding
        self.txt = self.header_generator()

    def write(self):
        (Path(self._path_to_md) / f"{self.p.stem}.md").write_text(self.txt, encoding=self.encoding, errors="ignore")

    def header_generator(self):
        return f"""# {self.p.stem}\n\n"""

    def add(self):
        for component, _data in self._dict.items():
            if component == "obc":
                continue
            self.component = component
            self.add_meta()
            for data in _data:
                self.data = data
                if self.data["name"] == "":
                    continue
                self.update_code()
                self.add_name()
                self.add_code()
                self.add_params()
                self.add_danger()
                self.add_restricted()
                self.add_desc_note()
                self.txt += "\n"
            self.txt += "\n"

    def add_meta(self):
        self.txt += f"""## {self.component}\n
Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
"""

    def add_name(self):
        self.txt += f'{self.data["name"]}|'

    def add_code(self):
        self.txt += "|" if "is_no_code" in self.data and self.data["is_no_code"] else f'{hex(self.code)}|'

    def add_params(self):
        if "params" in self.data:
            param_num = int(self.data["params"])
            self.txt += f'{param_num}|'
            for i in range(1, 7):
                if param_num >= i:
                    self.txt += f'{self.data[f"param{i}type"]}|'
                    self.txt += f'{self.data[f"param{i}desc"]}|' if f"param{i}.desc" in self.data else "|"
                else:
                    self.txt += "||"
        else:
            self.txt += '0|||||||||||||'

    def add_danger(self):
        self.txt += "o|" if "is_danger" in self.data else "|"

    def add_restricted(self):
        self.txt += "o|" if "is_restricted" in self.data else "|"

    def add_desc_note(self):
        self.txt += f'{self.data["desc"]}|' if "desc" in self.data else "|"
        self.txt += f'{self.data["note"]}|' if "note" in self.data else "|"


class Toml2CsvSGC(SGCBase):
    def __init__(self, p, _dict, path_to_csv, encoding="cp932"):
        self.p = p
        self._dict = _dict
        self._path_to_csv = path_to_csv
        self.encoding = encoding
        self.txt = self.header_generator()

        super().__init__()

    def write(self):
        (Path(self._path_to_csv) / f"{self.p.stem}.csv").write_text(self.txt, encoding=self.encoding, errors="ignore")

    def header_generator(self):
        return """Component,Name,Target,Code,Params,,,,,,,,,,,,,Danger Flag,Is Restricted,Description,Note
MOBC,,,,Num Params,Param1,,Param2,,Param3,,Param4,,Param5,,Param6,,,,,
Comment,,,,,Type,Description,Type,Description,Type,Description,Type,Description,Type,Description,Type,Description,,,,
*,Cmd_EXAMPLE,OBC,,2,uint32_t,address,int32_t,time [ms],,,,,,,,,,,��,�����̐����ƒP�ʂ��������ƁI�i��Ftime [ms]�j"""

    def add(self):
        self.code = 0
        for component, _data in self._dict.items():
            if component == "obc":
                continue
            self.component = component
            self.add_meta()
            for data in _data:
                self.data = data
                if self.data["name"] == "":
                    self.txt += "**,\n"
                    continue
                if not("is_no_code" in self.data and self.data["is_no_code"]):
                    self.update_code()
                self.add_name()
                self.add_code()
                self.add_params()
                self.add_danger()
                self.add_restricted()
                self.add_desc_note()
                self.txt += "\n"

    def add_meta(self):
        self.txt += f'* {self.component},\n'

    def add_name(self):
        if "is_no_code" in self.data and self.data["is_no_code"]:
            self.txt += "*"
        self.txt += f',{self.data["name"]},OBC,'

    def add_code(self):
        self.txt += "," if "is_no_code" in self.data and self.data["is_no_code"] else f'{hex(self.code)},'

    def add_params(self):
        if "params" in self.data:
            param_num = int(self.data["params"])
            self.txt += f'{param_num},'
            for i in range(1, 7):
                if param_num >= i:
                    self.txt += f'{self.data[f"param{i}type"]},'
                    self.txt += f'{self.data[f"param{i}desc"]},' if f"param{i}.desc" in self.data else ","
                else:
                    self.txt += ",,"
        else:
            self.txt += '0,,,,,,,,,,,,,'

    def add_danger(self):
        self.txt += "danger," if "is_danger" in self.data else ","

    def add_restricted(self):
        self.txt += "true," if "is_restricted" in self.data else ","

    def add_desc_note(self):
        self.txt += f'{self.data["desc"].replace(",","@@")},' if "desc" in self.data else ","
        self.txt += f'{self.data["note"].replace(",","@@")},' if "note" in self.data else ","


class Toml2MdBCT:
    def __init__(self, p, _dict, path_to_md, param_name="bct", encoding="utf-8"):
        self.p = p
        self._dict = _dict
        self._path_to_md = path_to_md
        self._param_name = param_name
        self.encoding = encoding
        self.txt = self.header_generator()

    def write(self):
        (Path(self._path_to_md) / f"{self.p.stem}.md").write_text(self.txt, encoding=self.encoding, errors="ignore")

    def header_generator(self):
        return f"""# {self.p.stem}\n
Name|Short Name|BCID|Deploy|SetBlockPosition|Clear|Activate|Inactivate|Danger|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-
"""

    def add(self):
        for data in self._dict[self._param_name]:
            if "comment" in data:
                continue
            else:
                self.data = data
                self.add_name()
                self.add_bcid()
                self.add_alias()
                self.add_danger()
                self.add_desc_note()
                self.txt += "\n"

    def add_name(self):
        self.txt += f'{self.data["name"]}|'
        self.txt += f'{self.data["sname"]}|' if "sname" in self.data else "|"

    def add_bcid(self):
        self.txt += f'{self.data["bcid"]}|'

    def add_alias(self):
        self.txt += 'o|' if "is_deploy" in self.data else "|"
        self.txt += 'o|' if "is_setblockposition" in self.data else "|"
        self.txt += 'o|' if "is_clear" in self.data else "|"
        self.txt += 'o|' if "is_activate" in self.data else "|"
        self.txt += 'o|' if "is_inactivate" in self.data else "|"

    def add_danger(self):
        self.txt += "o|" if "is_danger" in self.data else "|"

    def add_desc_note(self):
        self.txt += f'{self.data["desc"]}|' if "desc" in self.data else "|"
        self.txt += f'{self.data["note"]}|' if "note" in self.data else "|"


class Toml2CsvBCT:
    def __init__(self, p, _dict, path_to_csv, param_name="bct", encoding="cp932"):
        self.p = p
        self._dict = _dict
        self._path_to_csv = path_to_csv
        self._param_name = param_name
        self.encoding = encoding
        self.txt = self.header_generator()

        super().__init__()

    def write(self):
        (Path(self._path_to_csv) / f"{self.p.stem}.csv").write_text(self.txt, encoding=self.encoding, errors="ignore")

    def path_to_dest(self):
        return Path(self._path_to_csv) / f"{self.p.stem}.csv"

    def header_generator(self):
        return """Comment,Name,ShortName,BCID,�G�C���A�X,,,,,Danger Flag,Description,Note
,,,,Deploy,SetBlockPosition,Clear,Activate,Inactivate,,,
"""

    def add(self):
        for data in self._dict[self._param_name]:
            if "comment" in data:
                comments = data["comment"].split("\n")
                self.txt += "*"
                for comment in comments:
                    self.txt += f'*,{comment.replace(",", "@@")},,,,,,,,,,\n'
            else:
                self.data = data
                self.add_name()
                self.add_bcid()
                self.add_alias()
                self.add_danger()
                self.add_desc_note()
                self.txt += "\n"

    def add_name(self):
        self.txt += f',{self.data["name"]},'
        self.txt += f'{self.data["sname"]},'if "sname" in self.data else ","

    def add_bcid(self):
        self.txt += f'{self.data["bcid"]},'

    def add_alias(self):
        self.txt += '��,'if "is_deploy" in self.data else ","
        self.txt += '��,'if "is_setblockposition" in self.data else ","
        self.txt += '��,'if "is_clear" in self.data else ","
        self.txt += '��,'if "is_activate" in self.data else ","
        self.txt += '��,'if "is_inactivate" in self.data else ","

    def add_danger(self):
        self.txt += "danger" if "is_danger" in self.data else ""

    def add_desc_note(self):
        self.txt += f',{self.data["desc"]}'if "desc" in self.data else ","
        self.txt += f',{self.data["note"]}'if "note" in self.data else ","
