import toml
from abc import abstractmethod
from .utils import get_path, typelist, dict_settings


class CheckTomlBase:
    def __init__(self, path_to_toml, param_name):
        p_list = get_path(path_to_toml, suffix="toml")

        for p in p_list:
            print(f"---checking {p}")
            self.p = p
            self._dict = toml.load(open(p))
            self._param_name = param_name
            self.check()

    @abstractmethod
    def check(self):
        pass


class CheckTomlTLM(CheckTomlBase):
    def __init__(self, path_to_toml, param_name="tlm_field"):
        super().__init__(path_to_toml, param_name)

    def check(self):
        self.check_meta()
        self.check_phsh()
        for elem in self._dict[self._param_name]:
            self.check_type(elem)
            self.check_bit(elem)
            self.check_exp(elem)
            self.check_conv(elem)
        self.check_max_packet()

    def check_meta(self):
        # 上の4行は必ず必要
        def _check_meta_assert(k, ex):
            return f'キー"{k}"がありません, 追加してください ({str(self.p)})\nex.) {ex}'
        assert "obc" in self._dict, _check_meta_assert("obc", 'obc = "MOBC"')
        assert "Target" in self._dict, _check_meta_assert("Target", 'Target = "OBC"')
        assert "PacketID" in self._dict, _check_meta_assert("PacketID", 'PacketID = "0x00"')
        assert "Enable/Disable" in self._dict, _check_meta_assert("EnableDisable", 'EnableDisable = "ENABLE"')
        assert "IsRestricted" in self._dict, _check_meta_assert("IsRestricted", 'IsRestricted = "FALSE"')

    def check_max_packet(self):
        # パケットの最大長で弾く
        assert self._dict["obc"].upper() in dict_settings["obc_data"], f'settings.jsonで{self._dict["obc"].upper()}(大文字)の設定を記述してください'
        assert "max_packet" in dict_settings["obc_data"][self._dict["obc"].upper()], \
            f'settings.jsonで{self._dict["obc"].upper()}.max_packetの設定を記述してください'
        max_packet = dict_settings["obc_data"][self._dict["obc"].upper()]["max_packet"]
        packet = sum([typelist[elem["type"]] / 8 for elem in self._dict[self._param_name] if elem["type"] in typelist])
        assert packet <= max_packet, f"packetが最大値を超えています. \npacket_size: {packet}\nmax_packet_size: {max_packet}"

    def check_type(self, elem):
        assert elem["type"] in typelist, f'There is no such type: {elem["type"]} (name: {elem["name"]})'

    def check_bit(self, elem):
        if "comp" in elem:
            bitsum_default = typelist[elem["type"]]
            bitsum = sum([comp_["bitlen"] for comp_ in elem["comp"]])
            assert bitsum == bitsum_default, f"sum(bitlen) != default bitlen({bitsum} != {bitsum_default})"

    def check_exp(self, elem):
        if "exp" in elem:
            lbracket = elem["exp"].count("(")
            rbracket = elem["exp"].count(")")
            assert lbracket == rbracket, f'The number of brackets does not match. (: {lbracket}, ): {rbracket}'

    def check_phsh(self):
        def _err(phsh, path):
            return f"{phsh} is different from default. ({path})"
        # ph, shは共通なので確認
        assert {'comp': [{'bitlen': 3, 'name': 'PH.VER'},
                         {'bitlen': 1, 'name': 'PH.TYPE'},
                         {'bitlen': 1, 'name': 'PH.SH_FLAG'},
                         {'bitlen': 11, 'name': 'PH.APID'}], "type": "uint16_t"} in self._dict[self._param_name], \
            _err("PH.VER, PH.TYPE, PH.SH_FLAG, PH.APID", f"{self.p}")
        assert {"name": "PH.PACKET_LEN", "type": "uint16_t"} in self._dict[self._param_name], \
            _err("PH.PACKET_LEN", f"{self.p}")
        assert {'comp': [{'bitlen': 2, 'name': 'PH.SEQ_FLAG'},
                         {'bitlen': 14, 'name': 'PH.SEQ_COUNT'}], "type": "uint16_t"} in self._dict[self._param_name],\
            _err("PH.SEQ_FLAG, PH.SEQ_COUNT", f"{self.p}")
        assert {'name': 'PH.PACKET_LEN', 'type': 'uint16_t'} in self._dict[self._param_name],\
            _err("PH.PACKET_LEN", f"{self.p}")
        assert {'name': 'SH.VER', 'type': 'uint8_t'} in self._dict[self._param_name], \
            _err("SH.VER", f"{self.p}")
        assert {'name': 'SH.TI', 'type': 'uint32_t'} in self._dict[self._param_name], \
            _err("SH.VER", f"{self.p}")
        assert {'is_hex': True, 'name': 'SH.TLM_ID', 'type': 'uint8_t'} in self._dict[self._param_name], \
            _err("SH.TLM_ID", f"{self.p}")
        assert {'name': 'SH.GLOBAL_TIME', 'type': 'double'} in self._dict[self._param_name],\
            _err("SH.GLOBAL_TIME", f"{self.p}")
        assert {'name': 'SH.ON_BOARD_SUBNET_TIME', 'type': 'uint32_t'} in self._dict[self._param_name], \
            _err("SH.ON_BOARD_SUBNET_TIME", f"{self.p}")
        assert {'is_hex': True, 'name': 'SH.DEST_FLAGS', 'type': 'uint8_t'} in self._dict[self._param_name],\
            _err("SH.DEST_FLAGS", f"{self.p}")
        assert {'name': 'SH.DR_PARTITION', 'type': 'uint8_t'} in self._dict[self._param_name], \
            _err("SH.DR_PATITION", f"{self.p}")

    def check_conv(self, elem):
        # status, hex, poly, Noneは排他
        th = ("is_hex" in elem) + ("status" in elem) + ("poly" in elem)
        assert th <= 1, f'is_hex / status / poly should mutually exclude each other. (name: {elem["name"]}, {self.p})'


class CheckTomlCMD(CheckTomlBase):
    def __init__(self, path_to_toml, param_name="cmd_field"):
        super().__init__(path_to_toml, param_name)

    def check(self):
        pass
