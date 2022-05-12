import toml
import copy
import re
from pathlib import Path
from abc import abstractmethod, ABCMeta
from .convert_base import TLMBase, SGCBase
from .utils import print_progress, get_exp_comp

type2size_list = {
    "int8_t": ["TF_copy_i8", 1],
    "int16_t": ["TF_copy_i16", 2],
    "int32_t": ["TF_copy_i32", 4],
    "uint8_t": ["TF_copy_u8", 1],
    "uint16_t": ["TF_copy_u16", 2],
    "uint32_t": ["TF_copy_u32", 4],
    "float": ["TF_copy_float", 4],
    "double": ["TF_copy_double", 8]
}
type2temp = {
    "int8_t": "temp_i8",
    "int16_t": "temp_i16",
    "int32_t": "temp_i32",
    "uint8_t": "temp_u8",
    "uint16_t": "temp_u16",
    "uint32_t": "temp_u32",
    "float": "temp_f",
    "double": "temp_d",
}
type2byte = {
    "int8_t": 1,
    "int16_t": 2,
    "int32_t": 4,
    "uint8_t": 1,
    "uint16_t": 2,
    "uint32_t": 4,
    "float": 4,
    "double": 8,
}


def make_tlm_db(settings):
    tlm_db = {}
    tlm_db["dest_path"] = settings[0]["dest_path"]
    tlm_db["db_prefix"] = settings[0]["db_prefix"] + "_TLM_DB_"
    tlm_db["data"] = {}
    for p in settings[0]["data"]["tlm"]:
        data = {}
        data["tlm_name"] = re.sub(fr'^.*?{tlm_db["db_prefix"]}', r'', p.stem).upper()
        data["data"] = toml.load(open(p, encoding="utf-8"))
        packet_id = data["data"]["PacketID"]
        tlm_db["data"][int(packet_id, 0)] = data

    tlm_db["is_other_obc"] = False
    if len(settings) >= 2:
        tlm_db["other_obc"] = []
        for setting in settings[1:]:
            if not setting["is_enable"]:
                continue
            tlm_other_obc_db = {}
            tlm_other_obc_db["dest_path"] = setting["dest_path"]
            tlm_other_obc_db["db_prefix"] = setting["db_prefix"] + "_TLM_DB_"
            tlm_other_obc_db["name"] = setting["name"]
            tlm_other_obc_db["driver_name"] = setting["driver_name"]
            tlm_other_obc_db["driver_type"] = setting["driver_type"]
            tlm_other_obc_db["code_when_tlm_not_found"] = setting["code_when_tlm_not_found"]
            tlm_other_obc_db["max_tlm_num"] = setting["max_tlm_num"]
            tlm_other_obc_db["data"] = {}
            for p in setting["data"]["tlm"]:
                data = {}
                data["tlm_name"] = re.sub(fr'^.*?{tlm_other_obc_db["db_prefix"]}', r'', p.stem).upper()
                data["data"] = toml.load(open(p, encoding="utf-8"))
                packet_id = data["data"]["PacketID"]
                tlm_other_obc_db["data"][int(packet_id, 0)] = data

            tlm_db["other_obc"].append(tlm_other_obc_db)
        if len(tlm_db["other_obc"]) != 0:
            tlm_db["is_other_obc"] = True
    return tlm_db


def make_sgc_db(settings):
    sgc_db = {}
    p = settings[0]["data"]["sgc"]
    sgc_db["dest_path"] = settings[0]["dest_path"]
    sgc_db["data"] = toml.load(open(p, encoding="utf-8"))
    sgc_db["is_other_obc"] = False
    if len(settings) >= 2:
        sgc_db["other_obc"] = []
        for setting in settings[1:]:
            if not setting["is_enable"]:
                continue
            sgc_other_obc_db = {}
            p = setting["data"]["sgc"]
            sgc_other_obc_db["dest_path"] = setting["dest_path"]
            sgc_other_obc_db["name"] = setting["name"]
            sgc_other_obc_db["data"] = toml.load(open(p, encoding="utf-8"))
            sgc_db["other_obc"].append(sgc_other_obc_db)
        if len(sgc_db["other_obc"]) != 0:
            sgc_db["is_other_obc"] = True
    return sgc_db


def make_bct_db(settings):
    bct_db = {}
    p = settings[0]["data"]["bct"]
    bct_db["dest_path"] = settings[0]["dest_path"]
    bct_db["data"] = toml.load(open(p, encoding="utf-8"))
    return bct_db


class C2ACodeGenerator:
    @print_progress("Generate C2A Code")
    def __init__(self, settings):
        tlm_db = make_tlm_db(settings)
        sgc_db = make_sgc_db(settings)
        bct_db = make_bct_db(settings)
        Toml2CTLM(copy.deepcopy(tlm_db))
        Toml2HTLM(copy.deepcopy(tlm_db))
        Toml2CSGC(copy.deepcopy(sgc_db))
        Toml2HSGC(copy.deepcopy(sgc_db))
        Toml2HBCT(copy.deepcopy(bct_db))
        if tlm_db["is_other_obc"]:
            Toml2CTLMBuffer(copy.deepcopy(tlm_db))
            Toml2HTLMBuffer(copy.deepcopy(tlm_db))
            Toml2HTLMDataDef(copy.deepcopy(tlm_db))


class GenerateC2ABase(metaclass=ABCMeta):
    def header_generator(self):
        pass


class Toml2CTLMBuffer(TLMBase, GenerateC2ABase):
    @print_progress("toml to telemetry_buffer.c")
    def __init__(self, tlm_db, param_name="tlm"):
        self._param_name = param_name
        TLMBase.__init__(self)
        for other_obc in tlm_db["other_obc"]:
            self.name_lower = other_obc["name"].lower()
            self.name_upper = other_obc["name"].upper()
            driver_type = other_obc["driver_type"]
            driver_name = other_obc["driver_name"]
            dest_path = other_obc["dest_path"] / f"{self.name_lower}_telemetry_buffer.c"
            other_obc["data"] = [data[1] for data in sorted(other_obc["data"].items(), key=lambda x: x[0])]

            print(f"-----generating {str(dest_path)}")

            self.txt = self.header_generator()

            for data in other_obc["data"]:
                TLMBase.__init__(self)
                tlm_name = data["tlm_name"]
                tlm_name_lower = tlm_name.lower()
                self.txt += f"static DS_ERR_CODE {self.name_upper}_analyze_tlm_{tlm_name_lower}_(const CommonTlmPacket* packet, {self.name_upper}_TLM_CODE tlm_id, {driver_type}* {driver_name});\n"
            self.txt += f"\nstatic CommonTlmPacket {self.name_upper}_ctp_;\n\n"
            self.txt += f"""void {self.name_upper}_init_tlm_buffer({driver_type}* {driver_name})
{{
  // packet などは，上位の driver の初期化で driver もろとも memset 0x00 されていると期待して，ここではしない
  int i = 0;
  for (i = 0; i < {self.name_upper}_MAX_TLM_NUM; ++i)
  {{
    {driver_name}->tlm_buffer.tlm[i].is_null_packet = 1;
  }}
}}

DS_ERR_CODE {self.name_upper}_buffer_tlm_packet(DS_StreamConfig* p_stream_config, {driver_type}* {driver_name})
{{
  {self.name_upper}_TLM_CODE tlm_id;
  DS_ERR_CODE ret;

  ret = DS_C2AFMT_get_ctp(p_stream_config, &{self.name_upper}_ctp_);
  if (ret != DS_ERR_CODE_OK) return ret;

  tlm_id  = ({self.name_upper}_TLM_CODE)CTP_get_id(&{self.name_upper}_ctp_);

  switch (tlm_id)
  {{
"""
            for data in other_obc["data"]:
                TLMBase.__init__(self)
                tlm_name = data["tlm_name"]
                tlm_name_upper = tlm_name.upper()
                tlm_name_lower = tlm_name.lower()
                self.txt += f"""  case {self.name_upper}_Tlm_CODE_{tlm_name_upper}:
    return {self.name_upper}_analyze_tlm_{tlm_name_lower}_(&{self.name_upper}_ctp_, tlm_id, {driver_name});
"""
            self.txt += f"""  default:
    {other_obc["code_when_tlm_not_found"]}
    return DS_ERR_CODE_ERR;
  }}
}}
"""
            for data in other_obc["data"]:
                TLMBase.__init__(self)
                tlm_name = data["tlm_name"]
                tlm_name_upper = tlm_name.upper()
                tlm_name_lower = tlm_name.lower()
                self._dict = data["data"]
                self.txt += f'''
static DS_ERR_CODE {self.name_upper}_analyze_tlm_{tlm_name_lower}_(const CommonTlmPacket* packet, {self.name_upper}_TLM_CODE tlm_id, {driver_type}* {driver_name})
{{
  const uint8_t* f = packet->packet;
'''
                for k, v in type2temp.items():
                    if k == "float":
                        self.txt += f"  {k} {v} = 0.0f;\n"
                    elif k == "double":
                        self.txt += f"  {k} {v} = 0.0;\n"
                    else:
                        self.txt += f"  {k} {v} = 0;\n"
                self.txt += f'''
  // GS へのテレメ中継のためのバッファーへのコピー
  CTP_copy_packet(&({driver_name}->tlm_buffer.tlm[tlm_id].packet), packet);
  {driver_name}->tlm_buffer.tlm[tlm_id].is_null_packet = 0;
  // TODO: CRC チェック

  // MOBC 内部でテレメデータへアクセスしやすいようにするための構造体へのパース
'''
                for data in self._dict[self._param_name]:
                    type_ = data["type"]
                    if "comp" in data:
                        for data_comp in data["comp"]:
                            self.update_pos(data_comp, is_comp=True)
                            name = data_comp["name"]
                            var_name = f'{driver_name}->tlm_data.{tlm_name_lower}.{name.lower()}'
                            self.txt += f"  endian_memcpy(&{type2temp[type_]}, &(f[{self.octet_pos}]), {type2byte[type_]});\n"
                            self.txt += f"  {type2temp[type_]} >>= {type2byte[type_] * 8 - self.bit_pos - self.bit_len};\n"
                            self.txt += f'  {type2temp[type_]} &= {hex(int("0b" + "1" * self.bit_len, 2))};\n'
                            self.txt += f"  {var_name} = {type2temp[type_]};\n"
                    else:
                        self.update_pos(data)
                        name = data["name"]
                        var_name = f'{driver_name}->tlm_data.{tlm_name_lower}.{name.lower()}'
                        self.txt += f"  endian_memcpy(&({var_name}), &(f[{self.octet_pos}]), {type2byte[type_]});\n"
                self.txt += "  // TODO: ビットフィールドをつかっている系は，様々なパターンがあり得るので，今後，バグが出ないか注視する\n\n  // ワーニング回避\n"
                for k, v in type2temp.items():
                    self.txt += f'  (void){v};\n'
                self.txt += '\n  return DS_ERR_CODE_OK;\n}\n'

            self.txt += f'''
TF_TLM_FUNC_ACK {self.name_upper}_pick_up_tlm_buffer(const {driver_type}* {driver_name}, {self.name_upper}_TLM_CODE tlm_id, uint8_t* packet, uint16_t* len, uint16_t max_len)
{{
  const CommonTlmPacket* buffered_packet;

  if (tlm_id >= {self.name_upper}_MAX_TLM_NUM) return TF_TLM_FUNC_ACK_NOT_DEFINED;
  if ({driver_name}->tlm_buffer.tlm[tlm_id].is_null_packet) return TF_TLM_FUNC_ACK_NULL_PACKET;

  buffered_packet = &({driver_name}->tlm_buffer.tlm[tlm_id].packet);
  *len = CTP_get_packet_len(buffered_packet);

  if (*len > max_len) return TF_TLM_FUNC_ACK_TOO_SHORT_LEN;

  memcpy(packet, &buffered_packet->packet, (size_t)(*len));
  return TF_TLM_FUNC_ACK_SUCCESS;
}}

#pragma section
'''
            dest_path.write_text(self.txt)

    def header_generator(self):
        return f"""#pragma section REPRO
/**
 * @file
 * @brief  テレメトリバッファー（テレメ中継）
 * @note   このコードは自動生成されています！
 */
#include "./{self.name_lower}_telemetry_definitions.h"
#include "./{self.name_lower}_telemetry_buffer.h"
#include "./{self.name_lower}.h"
#include <string.h>

"""


class Toml2HTLMBuffer(TLMBase, GenerateC2ABase):
    @print_progress("toml to telemetry_buffer.h")
    def __init__(self, tlm_db, param_name="tlm"):
        self._param_name = param_name
        TLMBase.__init__(self)
        for other_obc in tlm_db["other_obc"]:
            self.name_lower = other_obc["name"].lower()
            self.name_upper = other_obc["name"].upper()
            driver_type = other_obc["driver_type"]
            driver_name = other_obc["driver_name"]
            max_tlm_num = other_obc["max_tlm_num"]
            dest_path = other_obc["dest_path"] / f"{self.name_lower}_telemetry_buffer.h"

            print(f"-----generating {str(dest_path)}")

            self.txt = self.header_generator()
            self.txt += f'''typedef struct {driver_type} {driver_type};

#define {self.name_upper}_MAX_TLM_NUM ({max_tlm_num})

typedef struct
{{
  CommonTlmPacket packet;   //!< 最新のテレメパケットを保持
  uint8_t is_null_packet;   //!< 一度でもテレメを受信しているか？（空配列が読み出されるのを防ぐため）
}} {self.name_upper}_TlmBufferElem;

typedef struct
{{
  {self.name_upper}_TlmBufferElem tlm[{self.name_upper}_MAX_TLM_NUM];   //!< TLM ID ごとに保持
}} {self.name_upper}_TlmBuffer;

void {self.name_upper}_init_tlm_buffer({driver_type}* {driver_name});

DS_ERR_CODE {self.name_upper}_buffer_tlm_packet(DS_StreamConfig* p_stream_config, {driver_type}* {driver_name});

TF_TLM_FUNC_ACK {self.name_upper}_pick_up_tlm_buffer(const {driver_type}* {driver_name}, {self.name_upper}_TLM_CODE tlm_id, uint8_t* packet, uint16_t* len, uint16_t max_len);
'''
            self. txt += "\n#endif\n"
            dest_path.write_text(self.txt)

    def header_generator(self):
        return f"""/**
 * @file
 * @brief  テレメトリバッファー（テレメ中継）
 * @note   このコードは自動生成されています！
 */
#ifndef {self.name_upper}_TELEMETRY_BUFFER_H_
#define {self.name_upper}_TELEMETRY_BUFFER_H_

#include "./{self.name_lower}_telemetry_definitions.h"
#include <src_core/Drivers/Super/driver_super.h>
#include <src_core/TlmCmd/common_tlm_packet.h>
#include <src_core/TlmCmd/telemetry_frame.h>

"""


class Toml2HTLMDataDef(TLMBase, GenerateC2ABase):
    @ print_progress("toml to telemetry_data_definitions.h")
    def __init__(self, tlm_db, param_name="tlm"):
        self._param_name = param_name
        TLMBase.__init__(self)
        for other_obc in tlm_db["other_obc"]:
            self.name_lower = other_obc["name"].lower()
            self.name_upper = other_obc["name"].upper()
            dest_path = other_obc["dest_path"] / f"{self.name_lower}_telemetry_data_definitions.h"
            other_obc["data"] = [data[1] for data in sorted(other_obc["data"].items(), key=lambda x: x[0])]

            print(f"-----generating {str(dest_path)}")

            self.txt = self.header_generator()
            self.txt += "typedef struct\n{\n"
            for data in other_obc["data"]:
                TLMBase.__init__(self)
                self._dict = data["data"]
                self.tlm_name = data["tlm_name"]
                self.txt += self.add()
            self.txt += "}" + f" {self.name_upper}_TlmData;\n"
            self.txt += "\n#endif\n"
            dest_path.write_text(self.txt)

    def add(self):
        structure = {}

        def set_structure(_structure, _name_list, type_):
            if _name_list[0] not in _structure:
                if len(_name_list) == 1:
                    if len(_structure) == 0:
                        return {_name_list[0]: type_}
                    else:
                        _structure[_name_list[0]] = type_
                        return _structure
                if len(_name_list) >= 2:
                    _structure[_name_list[0]] = set_structure({}, _name_list[1:], type_)
                    return _structure
            if _name_list[0] in _structure:
                if not isinstance(_structure[_name_list[0]], dict):
                    raise ValueError(f"名前が重複しています. 予期していない(checkで吸収されるべきバグです.\n{_name_list[0]}, {_structure}", type_)
                else:
                    _structure[_name_list[0]] = set_structure(_structure[_name_list[0]], _name_list[1:], type_)
                    return _structure

        def make_txt_from_structure(_txt, _structure, indent, new_key):
            _txt += f'{" " * indent}struct\n{" " * indent}{{\n'
            for key in _structure:
                if isinstance(_structure[key], dict):
                    _txt = make_txt_from_structure(_txt, _structure[key], indent + 2, key)
                else:
                    _txt += " " * (indent + 2) + f'{_structure[key]} {key.lower()};\n'
            _txt += " " * indent + "}" + f" {new_key.lower()};\n"
            return _txt

        for i, data in enumerate(self._dict[self._param_name]):
            type_ = data["type"]
            if "comp" in data:
                for data_comp in data["comp"]:
                    name = data_comp["name"]
                    structure = set_structure(structure, name.split("."), type_)
            else:
                name = data["name"]
                structure = set_structure(structure, name.split("."), type_)

        txt = make_txt_from_structure("", structure, 2, self.tlm_name)
        return txt

    def header_generator(self):
        return f"""/**
 * @file
 * @brief  バッファリングされているテレメをパースしてMOBC内でかんたんに利用できるようにするためのテレメデータ構造体定義
 * @note   このコードは自動生成されています！
 */
#ifndef {self.name_upper}_TELEMETRY_DATA_DEFINITIONS_H_
#define {self.name_upper}_TELEMETRY_DATA_DEFINITIONS_H_

"""


class Toml2CTLM(TLMBase, GenerateC2ABase):
    @ print_progress("toml to telemetry_definitions.c")
    def __init__(self, tlm_db, param_name="tlm"):
        self._param_name = param_name
        dest_path = tlm_db["dest_path"] / "telemetry_definitions.c"
        TLMBase.__init__(self)
        print(f"-----generating {str(dest_path)}")
        db_all = {}
        other_names = []
        if tlm_db["is_other_obc"]:
            for other_obc in tlm_db["other_obc"]:
                db_all = {**db_all, **tlm_db["data"], **other_obc["data"]}
                other_names.append(other_obc["name"])
        db_all = [data[1] for data in sorted(db_all.items(), key=lambda x: x[0])]
        tlm_db["data"] = [data[1] for data in sorted(tlm_db["data"].items(), key=lambda x: x[0])]

        self.txt = self.header_generator()
        for data in db_all:
            TLMBase.__init__(self)
            self._dict = data["data"]
            tlm_name = data["tlm_name"]
            for other_name in other_names:
                if other_name in tlm_name:
                    self.txt += f'static TF_TLM_FUNC_ACK Tlm_{tlm_name}_(uint8_t* packet, uint16_t* len, uint16_t max_len); // {other_name.upper()} TLM\n'
                    break
            else:
                self.txt += f'static TF_TLM_FUNC_ACK Tlm_{tlm_name}_(uint8_t* packet, uint16_t* len, uint16_t max_len);\n'

        self.txt += "\nvoid TF_load_tlm_table(TF_TlmInfo tlm_table[TF_MAX_TLMS])\n{\n"

        for data in db_all:
            TLMBase.__init__(self)
            self._dict = data["data"]
            tlm_name = data["tlm_name"]
            for other_name in other_names:
                if other_name in tlm_name:
                    self.txt += f'  tlm_table[Tlm_CODE_{tlm_name}].tlm_func = Tlm_{tlm_name}_; // {other_name.upper()} TLM\n'
                    break
            else:
                self.txt += f'  tlm_table[Tlm_CODE_{tlm_name}].tlm_func = Tlm_{tlm_name}_;\n'
        else:
            self.txt += "}\n"

        for data in tlm_db["data"]:
            TLMBase.__init__(self)
            self._dict = data["data"]
            tlm_name = data["tlm_name"]
            self.txt += f"""
static TF_TLM_FUNC_ACK Tlm_{tlm_name}_(uint8_t* packet, uint16_t* len, uint16_t max_len)
""" + "{\n"
            self.txt += self.add_local_var()
            self.txt += self.add_func()
            self.txt += "}\n"

        if tlm_db["is_other_obc"]:
            for other_obc in tlm_db["other_obc"]:
                other_obc["data"] = [data[1] for data in sorted(other_obc["data"].items(), key=lambda x: x[0])]
                driver_name = other_obc["driver_name"]
                name = other_obc["name"]
                for data in other_obc["data"]:
                    TLMBase.__init__(self)
                    self._dict = data["data"]
                    tlm_name = data["tlm_name"]
                    self.txt += f"""
static TF_TLM_FUNC_ACK Tlm_{tlm_name.upper()}_(uint8_t* packet, uint16_t* len, uint16_t max_len)
{{
  return {name.upper()}_pick_up_tlm_buffer({driver_name}, {name.upper()}_Tlm_CODE_{tlm_name.upper()}, packet, len, max_len);
}}
"""

        self.txt += "\n#pragma section\n"

        dest_path.write_text(self.txt)

    def header_generator(self):
        return """#pragma section REPRO
/**
 * @file
 * @brief  テレメトリ定義
 * @note   このコードは自動生成されています！
 */
#include "../../src_core/TlmCmd/telemetry_frame.h"
#include "telemetry_definitions.h"
#include "telemetry_source.h"

"""

    def add_local_var(self):
        txt = ""
        if "Local Var" in self._dict:
            local_var = self._dict["Local Var"].replace("##", "\n  ")
            if local_var[-3:] == "\n  ":
                local_var = local_var[:-3]
            if local_var != "":
                txt += f'  {local_var}\n\n'
        return txt

    def add_func(self):
        txt = ""
        self.max_pos = 0
        self.func_code = ""
        for data in self._dict[self._param_name]:
            self.data = data
            if "comp" in data:
                for data_comp in data["comp"]:
                    self.update_pos(data=data_comp, is_comp=True)
                exp = get_exp_comp(data)
                if exp is None:
                    continue
                self.max_pos = self.octet_pos + type2size_list[data["type"]][1]
                self.func_code += f'  {type2size_list[data["type"]][0]}(&packet[{self.octet_pos}], {exp});\n'
            else:
                self.update_pos()
                if "exp" not in data:
                    continue
                self.max_pos = self.octet_pos + type2size_list[data["type"]][1]
                self.func_code += f'  {type2size_list[data["type"]][0]}(&packet[{self.octet_pos}], {data["exp"]});\n'
        txt += f"""  if ({self.max_pos} > max_len) return TF_TLM_FUNC_ACK_TOO_SHORT_LEN;

#ifndef BUILD_SETTINGS_FAST_BUILD
{self.func_code[:-1]}
#endif

  *len = {self.max_pos};
  return TF_TLM_FUNC_ACK_SUCCESS;
"""
        return txt


class Toml2HTLM(GenerateC2ABase):
    @ print_progress("toml to telemetry_definitions.h")
    def __init__(self, tlm_db, param_name="tlm"):
        self._param_name = param_name
        dest_path = (tlm_db["dest_path"] / "telemetry_definitions.h")

        print(f"-----generating {dest_path}")

        other_names = []
        if tlm_db["is_other_obc"]:
            for other_obc in tlm_db["other_obc"]:
                tlm_db["data"] = {**tlm_db["data"], **other_obc["data"]}
                other_names.append(other_obc["name"])
        tlm_db["data"] = [data[1] for data in sorted(tlm_db["data"].items(), key=lambda x: x[0])]

        self.txt = self.header_generator()
        for data in tlm_db["data"]:
            TLMBase.__init__(self)
            self._dict = data["data"]
            self.tlm_name = data["tlm_name"]
            self.txt += self.add(other_names)
        else:
            self.txt += """
  TLM_CODE_MAX
} TLM_CODE;

#endif
"""
        dest_path.write_text(self.txt)

        if tlm_db["is_other_obc"]:
            for other_obc in tlm_db["other_obc"]:
                self.name_lower = other_obc["name"].lower()
                self.name_upper = other_obc["name"].upper()
                dest_path = other_obc["dest_path"] / f"{self.name_lower}_telemetry_definitions.h"

                print(f"-----generating {str(dest_path)}")
                other_obc["data"] = [data[1] for data in sorted(other_obc["data"].items(), key=lambda x: x[0])]
                self.txt = self.header_generator(self.name_upper + "_")
                for data in other_obc["data"]:
                    TLMBase.__init__(self)
                    self._dict = data["data"]
                    self.tlm_name = data["tlm_name"]
                    self.txt += self.add(is_other=True)
                else:
                    self.txt += f"""
  {self.name_upper + "_"}TLM_CODE_MAX
}} {self.name_upper + "_"}TLM_CODE;

#endif
"""
                dest_path.write_text(self.txt)

    def header_generator(self, name_upper=""):
        return f"""/**
 * @file
 * @brief  テレメトリ定義
 * @note   このコードは自動生成されています！
 */
#ifndef {name_upper}TELEMETRY_DEFINITIONS_H_
#define {name_upper}TELEMETRY_DEFINITIONS_H_

typedef enum
{{
"""

    def add(self, other_names=[], is_other=False):
        txt = ""
        if is_other:
            txt += f'  {self.name_upper}_Tlm_CODE_{self.tlm_name} = {self._dict["PacketID"]},\n'
        else:
            for other_name in other_names:
                if other_name in self.tlm_name:
                    txt += f'  Tlm_CODE_{self.tlm_name} = {self._dict["PacketID"]}, // {other_name.upper()} TLM\n'
                    break
            else:
                txt += f'  Tlm_CODE_{self.tlm_name} = {self._dict["PacketID"]},\n'
        return txt


class Toml2CSGC(SGCBase, GenerateC2ABase):
    @ print_progress("toml to command_definitions.c")
    def __init__(self, sgc_db):
        self.sgc_db = sgc_db
        dest_path = (sgc_db["dest_path"] / "command_definitions.c")
        SGCBase.__init__(self)

        print(f"-----generating {str(dest_path)}")

        self.txt = self.header_generator()
        self.txt += self.add()
        dest_path.write_text(self.txt)

    def header_generator(self):
        return """#pragma section REPRO
/**
 * @file
 * @brief  コマンド定義
 * @note   このコードは自動生成されています！
 */
#include "../../src_core/TlmCmd/command_analyze.h"
#include "command_definitions.h"
#include "command_source.h"

void CA_load_cmd_table(CA_CmdInfo cmd_table[CA_MAX_CMDS])
{
"""

    def add(self):
        txt1 = ""
        txt2 = ""
        for component, _data in self.sgc_db["data"].items():
            if component == "obc":
                continue
            self.component = component
            for data in _data:
                self.data = data
                if self.data["name"] == "":
                    continue
                self.update_code()
                txt1 += self.add_code()
                txt2 += self.add_params()
        txt2 += """}

#pragma section
"""
        return txt1 + "\n" + txt2

    def add_code(self):
        self.name = self.data["name"]
        self.name_code = self.data["name"].replace("Cmd_", "Cmd_CODE_")
        txt = f'  cmd_table[{self.name_code}].cmd_func = {self.name};\n'
        return txt

    def add_params(self):
        txt = ""
        type2size_list = {
            "int8_t": "CA_PARAM_SIZE_TYPE_1BYTE",
            "int16_t": "CA_PARAM_SIZE_TYPE_2BYTE",
            "int32_t": "CA_PARAM_SIZE_TYPE_4BYTE",
            "uint8_t": "CA_PARAM_SIZE_TYPE_1BYTE",
            "uint16_t": "CA_PARAM_SIZE_TYPE_2BYTE",
            "uint32_t": "CA_PARAM_SIZE_TYPE_4BYTE",
            "float": "CA_PARAM_SIZE_TYPE_4BYTE",
            "double": "CA_PARAM_SIZE_TYPE_8BYTE",
            "raw": "CA_PARAM_SIZE_TYPE_RAW",
        }

        if "params" in self.data and int(self.data["params"]) != 0:
            for i in range(int(self.data["params"])):
                index, mod = divmod(i, 2)
                subindex = "first" if mod == 0 else "second"
                txt += f'  cmd_table[{self.name_code}].param_size_infos[{str(index)}].packed_info.bit.{subindex} = '
                txt += f'{type2size_list[self.data[f"param{i+1}type"]]};\n'
        return txt


class Toml2HSGC(SGCBase, GenerateC2ABase):
    @ print_progress("toml to command_definitions.h")
    def __init__(self, sgc_db):
        self.sgc_db = sgc_db
        dest_path = (sgc_db["dest_path"] / "command_definitions.h")
        SGCBase.__init__(self)

        print(f"-----generating {str(dest_path)}")
        self._dict = sgc_db["data"]
        self.txt = self.header_generator()
        self.txt += self.add()
        dest_path.write_text(self.txt)

        if sgc_db["is_other_obc"]:
            for db in sgc_db["other_obc"]:
                self._dict = db["data"]
                self.name_upper = db["name"].upper()
                self.name_lower = db["name"].lower()
                self.txt = self.header_generator(self.name_upper + "_")
                self.txt += self.add(self.name_upper + "_", is_other=True)
                (db["dest_path"] / f'{self.name_lower}_command_definitions.h').write_text(self.txt)

    def header_generator(self, name_upper=""):
        return f"""/**
 * @file
 * @brief  コマンド定義
 * @note   このコードは自動生成されています！
 */
#ifndef {name_upper}COMMAND_DEFINITIONS_H_
#define {name_upper}COMMAND_DEFINITIONS_H_

typedef enum
{{
"""

    def add(self, name_upper="", is_other=False):
        txt = ""
        for component, _data in self._dict.items():
            if component == "obc":
                continue
            self.component = component
            for data in _data:
                self.data = data
                if self.data["name"] == "":
                    continue
                self.update_code()
                txt += self.add_code(is_other)
                txt += "\n"
        txt += f"""
  {name_upper}Cmd_CODE_MAX
}} {name_upper}CMD_CODE;

#endif
"""
        return txt

    def add_code(self, is_other=False):
        self.name = self.data["name"]
        if is_other:
            self.name_code = self.data["name"].replace("Cmd_", f"{self.name_upper}_Cmd_CODE_")
        else:
            self.name_code = self.data["name"].replace("Cmd_", "Cmd_CODE_")
        txt = f'  {self.name_code} = 0x{self.code:04X},'
        return txt


class Toml2HBCT(GenerateC2ABase):
    @ print_progress("toml to block_command_definitions.h")
    def __init__(self, bct_db):
        self.bct_db = bct_db
        dest_path = (bct_db["dest_path"] / "block_command_definitions.h")

        print(f'-----generating {str(dest_path)}')

        self._dict = bct_db["data"]
        self.txt = self.header_generator()
        self.txt += self.add()
        dest_path.write_text(self.txt)

    def header_generator(self):
        return """/**
 * @file
 * @brief  ブロックコマンド定義
 * @note   このコードは自動生成されています！
 */
#ifndef BLOCK_COMMAND_DEFINITIONS_H_
#define BLOCK_COMMAND_DEFINITIONS_H_

// 登録されるBlockCommandTableのblock番号を規定
typedef enum
{
"""

    def add(self):
        txt = ""
        for data in self._dict["bct"]:
            self.data = data
            is_comment = False
            if "comment" in data:
                comment = "  // " + data["comment"].replace("\n", "\n  // ").replace("  // \n", "\n")
                if not is_comment:
                    txt += "\n"
                    is_comment = True
                txt += f'{comment}\n'
                continue
            if is_comment:
                is_comment = False
            txt += self.add_code()
            txt += "\n"
        txt += """
  BC_ID_MAX    // BCT 自体のサイズは BCT_MAX_BLOCKS で規定
} BC_DEFAULT_ID;

void BC_load_defaults(void);

#endif
"""
        return txt

    def add_code(self):
        txt = ""
        txt += f'  {self.data["name"]} = {self.data["bcid"]},'
        if "desc" in self.data:
            txt += f'    // {self.data["desc"]}'
        return txt
