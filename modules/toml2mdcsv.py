import toml
from pathlib import Path
from abc import abstractmethod
from .utils import get_path, typelist, dict_status


class Toml2MdCsvBase:
    def __init__(self, path_to_toml, path_to_md, path_to_csv):
        p_list = get_path(path_to_toml, suffix="toml")
        for p in p_list:
            print(f"-----converting {p}")
            if "status.toml" in str(p):
                continue
            self._dict = toml.load(open(p))
            self.md_txt = self.md_header_generator(p)
            self.csv_txt = self.csv_header_generator(p)
            self.add()
            path_to_md_file = Path(path_to_md) / f"{p.stem}.md"
            path_to_md_file .write_text(self.md_txt)
            path_to_csv_file = Path(path_to_csv) / f"{p.stem}.csv"
            path_to_csv_file.write_text(self.csv_txt)

    @abstractmethod
    def md_header_generator(self, p):
        pass

    @abstractmethod
    def csv_header_generator(self, p):
        pass

    @abstractmethod
    def add(self):
        pass


class Toml2MdCsvTLM(Toml2MdCsvBase):
    def __init__(self, path_to_toml, path_to_md, path_to_csv, param_name="tlm_field"):
        self._param_name = param_name
        super().__init__(path_to_toml, path_to_md, path_to_csv)

    def md_header_generator(self, p):
        return f"""# {p.stem}\n
Name|Type|Exp.|Octet Pos.|bit Pos.|bit Len.|HEX|Status|Desc.|Note
-|-|-|-|-|-|-|-|-|-
"""

    def csv_header_generator(self, p):
        return f""",Target,{self._dict["Target"]},OBC,Local Var,
,PacketID,{self._dict["PacketID"]},{self._dict["Local Var"]},
,Enable/Disable,{self._dict["Enable/Disable"]},
,IsRestricted,{self._dict["IsRestricted"]},,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,
Comment,TLM Entry,Onboard Software Info.,,Extraction Info.,,,,Conversion Info.,,,,,,,,Description,Note
,Name,Var.%%##Type,Variable or Function Name,Ext.%%##Type,Pos. Desiginator,,,Conv.%%##Type,Poly (��a_i * x^i),,,,,,Status,,
,,,,,Octet%%##Pos.,bit%%##Pos.,bit%%##Len.,,a0,a1,a2,a3,a4,a5,,,
"""

    def add(self):
        self.octet_pos = 0
        self.bit_pos = 0
        self.bit_len = 0
        for elem in self._dict[self._param_name]:
            if "comp" in elem:
                self.add_comp(elem)
            else:
                self.add_name(elem)
                self.add_type(elem)
                self.add_exp(elem)
                self.add_pos(elem)
                self.add_hex(elem)
                self.add_status(elem)
                self.add_conv(elem)  # for csv
                self.add_desc_note(elem)
                self.md_txt += "\n"
                self.csv_txt += "\n"

    def add_comp(self, elem):
        is_comp_init = True
        for elem_ in elem["comp"]:
            self.add_name(elem_)
            if is_comp_init:
                self.add_type(elem)
                self.add_exp(elem)
                is_comp_init = False
            else:
                self.md_txt += "||"
                self.csv_txt += ",,PACKET,"
            self.add_pos(elem_, is_comp=True)
            self.add_desc_note(elem_)
            self.md_txt += "\n"
            self.csv_txt += "\n"

    def add_name(self, elem):
        self.md_txt += f'{elem["name"]}|'
        self.csv_txt += f',{elem["name"]},'

    def add_type(self, elem):
        self.md_txt += f'{elem["type"]}|'
        self.csv_txt += f'{elem["type"]},'

    def add_exp(self, elem):
        self.md_txt += f'{elem["exp"].replace("|", "&#124;")}|' if "exp" in elem else "|"
        self.csv_txt += f'{elem["exp"]},PACKET,' if "exp" in elem else ",PACKET,"

    def add_pos(self, elem, is_comp=False):
        self.octet_pos += int((self.bit_pos + self.bit_len) / 8)
        self.bit_pos = (self.bit_pos + self.bit_len) % 8
        if is_comp:
            self.bit_len = elem["bitlen"]
        else:
            self.bit_len = typelist[elem["type"]]
        self.md_txt += f'{self.octet_pos}|{self.bit_pos}|{self.bit_len}|'
        self.csv_txt += f'{self.octet_pos},{self.bit_pos},{self.bit_len},'

    def add_hex(self, elem):
        self.md_txt += 'o|' if "is_hex" in elem and elem["is_hex"] else "|"

    def add_status(self, elem):
        self.md_txt += f'{elem["status"]}|' if "status" in elem else "|"

    def add_conv(self, elem):
        conv = "NONE,,,,,,,"
        if "is_hex" in elem and elem["is_hex"]:
            conv = "HEX,,,,,,,"
        elif "status" in elem:
            index = elem["status"].split(".")
            status_txt = ""
            for k, v in dict_status[index[0]][index[1]].items():
                status_txt += f"{k}={v}@@"
            conv = f"STATUS,,,,,,{status_txt[:-2]},"
        self.csv_txt += f"{conv}"

    def add_desc_note(self, elem):
        self.md_txt += f'{elem["desc"]}|' if "desc" in elem else "|"
        self.md_txt += f'{elem["note"]}|' if "note" in elem else "|"
        self.csv_txt += f'{elem["desc"]},' if "desc" in elem else ","
        self.csv_txt += f'{elem["note"]},' if "note" in elem else ","


class Toml2MdCsvCMD(Toml2MdCsvBase):
    def __init__(self, path_to_toml, path_to_md, path_to_csv):
        super().__init__(path_to_toml, path_to_md, path_to_csv)

    def md_header_generator(self, p):
        return f"""# {p.stem}\n\n"""

    def csv_header_generator(self, p):
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
                    self.csv_txt += "**,\n"
                    continue
                self.add_name()
                self.add_code()
                self.add_params()
                self.add_danger()
                self.md_txt += "\n"
                self.csv_txt += "\n"
            self.md_txt += "\n"

    def add_meta(self):
        self.md_txt += f"""## {self.component}\n
Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
"""
        self.csv_txt += f'* {self.component},\n'

    def add_name(self):
        self.md_txt += f'{self.data["name"]}|'
        self.csv_txt += f',{self.data["name"]},OBC,'

    def add_code(self):
        if "code" in self.data and self.data["code"] != "":
            self.code = int(self.data["code"], 16)
        else:
            self.code += 1
        self.md_txt += "|" if "is_no_code" in self.data and self.data["is_no_code"] else f'{hex(self.code)}|'
        self.csv_txt += "," if "is_no_code" in self.data and self.data["is_no_code"] else f'{hex(self.code)},'

    def add_params(self):
        if "params" in self.data:
            param_num = len(self.data["params"])
            self.md_txt += f'{param_num}|'
            self.csv_txt += f'{param_num},'
            for i in range(6):
                if i < param_num:
                    self.md_txt += f'{self.data["params"][i]["type"]}|'
                    self.md_txt += f'{self.data["params"][i]["desc"]}|' if "desc" in self.data["params"][i] else "|"
                    self.csv_txt += f'{self.data["params"][i]["type"]},'
                    self.csv_txt += f'{self.data["params"][i]["desc"]},' if "desc" in self.data["params"][i] else ","
                else:
                    self.md_txt += "||"
                    self.csv_txt += ",,"
        else:
            self.md_txt += '0|||||||||||||'
            self.csv_txt += '0,,,,,,,,,,,,,'

    def add_danger(self):
        self.md_txt += "o|" if "is_danger" in self.data else "|"
        self.csv_txt += "danger," if "is_danger" in self.data else ","

    def add_restricted(self):
        self.md_txt += "o|" if "is_restricted" in self.data else "|"
        self.csv_txt += "true," if "is_restricted" in self.data else ","

    def add_desc_note(self):
        self.md_txt += f'{self.data["desc"]}|' if "desc" in self.data else "|"
        self.md_txt += f'{self.data["note"]}|' if "note" in self.data else "|"
        self.csv_txt += f'{self.data["desc"]},' if "desc" in self.data else ","
        self.csv_txt += f'{self.data["note"]},' if "note" in self.data else ","
