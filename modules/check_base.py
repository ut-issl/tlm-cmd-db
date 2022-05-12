from .utils import type2bit, err


def check_type_exists(data, path):
    assert data["type"] in type2bit.keys(), err(path, data, f'typeは{list(type2bit.keys())}の中から指定してださい')


def check_hex_status_poly(data, path):
    assert ("is_hex" in data) + ("status" in data) + ("a0" in data) <= 1, err(path, data, 'is_hex / status / poly(a0~a5) は排他です.')


def check_data_name_duplicate(data, name_list, path):
    if "comp" in data:
        for data_comp in data["comp"]:
            assert data_comp["name"] not in name_list, err(path, data, "nameに重複があります. 共通部分を記述したファイルを含めて確認してください")
            name_list.append(data_comp["name"])
        return name_list
    else:
        assert data["name"] not in name_list, err(path, data, "nameに重複があります, 共通部分を記述したファイルや????と??などを確認してください")
        name_list.append(data["name"])
        return name_list


def check_exp_brackets(data, path):
    assert data["exp"].count("(") == data["exp"].count(")"), err(path, data, "expの括弧の数が合いません, 確認してください")
    assert data["exp"].count("{") == data["exp"].count("}"), err(path, data, "expの波括弧の数が合いません, 確認してください")


def check_max_tlm_num(packet, max_tlm_num):
    assert packet <= max_tlm_num, f"packetが最大値を超えています. \npacket_size: {packet}\nmax_tlm_num_size: {max_tlm_num}"


def check_toml_base_exists(path_list, fname_included):
    assert len([p for p in path_list if f"{fname_included}.toml" in p.name]) == 1, f'共通部分を記述したtomlファイル {path_list[0].parent}/{fname_included}.toml が存在しません. 共通部分がない場合にもファイルを作成してください'


def check_type(data, expand_option, path, is_last=False):
    if expand_option["type"] != "":
        assert "type" not in data, err(path, data, "typeはすでに上の階層で定義されています.個別で定義する場合には上の階層の定義を消してください.")
    else:
        if is_last:
            assert "type" in data, err(path, data, "typeが定義されていません. 定義してください")
    if "type" in data:
        assert expand_option["type"] == "", err(path, data, "typeはすでに上の階層で定義されています.個別で定義する場合には上の階層の定義を消してください.")
        expand_option["type"] = data["type"]


def check_block_num(data, path):
    assert data["block_num"] == len(data["block"]), err(path, data, f'block_numとblock数が異なります, 適切に設定してください\nblock_num = {data["block_num"]}\nblock数 = {len(data["block"])}')


def check_seq_num(data, path):
    assert data["seq_num"] == len(data["seq"]), err(path, data, f'seq_numとseq数が異なります, 適切に設定してください\nseq_num = {data["seq_num"]}\nseq数 = {len(data["seq"])}')


def check_all_params(params, params_str, data, path):
    assert len([v for k, v in data.items() if k not in params]) == 0, err(path, data, f"{params_str}以外のキーを定義することはできません")


def check_param_in(name, param, data, path):
    assert param in data, err(path, data, f'[[{name}]]の中で{param}を定義してください')


def check_param(param, data, path):
    assert param in data, err(path, data, f'{param}を定義してください')


def check_name_base_not_in(data, path):
    assert "name_base" not in data, err(path, data, 'seqが存在しないところでname_baseを定義しています')


def check_param_not_in(name, param, data, path):
    assert param not in data, err(path, data, f'[[{name}]]の中では{param}を定義できません')


def check_param_before(name, param, data, path):
    assert param in data, err(path, data, f'[[{name}]]の前で{param}を定義してください')


def check_no_seq(data, path):
    assert "seq" not in data, err(path, data, f'seqを用いる場合は[[seq]]の前でseq数を以下のように定義してください\nseq_num = {len(data["seq"])}')


def check_no_block(data, path):
    assert "block" not in data, err(path, data, f'blockを用いる場合は[[block]]の前でblock数を以下のように定義してください\nblock_num = {len(data["block"])}')


def check_not_seq_block_block(data, expand_option, path):
    if len(expand_option["layer"]) >= 2:
        assert expand_option["layer"][-2:] != ["seq", "block"], err(path, data, "[[seq.block.block]]は定義できません")


def check_not_block_3(data, expand_option, path):
    assert expand_option["block"] <= 2, err(path, data, "blockは2層までしか定義できません.")


def check_seq_once(data, expand_option, path):
    assert expand_option["seq"] == 0, err(path, data, "seqは1層までしか定義できません")


def check_comp_once(data, expand_option, path):
    assert expand_option["comp"] == 0, err(path, data, "compは1層までしか定義できません")


def check_bit_comp(data, path):
    assert type2bit[data["type"]] == sum(data["bitlen"]), err(path, data, f'適切にビット圧縮できていません, {type2bit[data["type"]]}({data["type"]}) != {sum(data["bitlen"])}')


def check_name_base_bracket_num(data, expand_option, path):
    if isinstance(data["name"], list):
        assert expand_option["name_base"].count("{}") == len(data["name"]), err(path, data, f'name_base内の波括弧の数({expand_option["name_base"].count("{}")})とnameの要素数({len(data["name"])})が異なります')


def check_exp_after_exp_base(data, path):
    assert "exp" in data, err(path, data, f'exp_baseを定義した場合は[[seq]]内ではexpを定義しましょう')


def check_exp_base_bracket_num(data, expand_option, path):
    assert data["exp"] == "" or "{}" in expand_option["exp_base"], err(path, data, 'expが定義されていますが, exp_baseには波括弧がありません. 波括弧がなくてもいい場合はexp=""としてください.')


def check_exp_without_exp_base(data, expand_option, path):
    if "exp" in data:
        assert "exp_base" in expand_option and expand_option["exp_base"] != "", err(path, data, "expは[[seq]]の前でexp_baseを定義した場合にのみ定義できます. もしexp_baseが必要ない場合にはexp_base=" + "{}" + "と定義してください")
        if isinstance(data["exp"], list):
            assert expand_option["exp_base"].count("{}") == len(data["exp"]), err(path, data, f'exp_base内の波括弧の数({expand_option["exp_base"].count("{}")})とexpの要素数({len(data["exp"])})が異なります')


def check_data_replace_type(data, key, expand_option, path):
    if "{type}" in data[key]:
        assert expand_option["type"] != "", err(path, data, "{type}が存在しているが, typeが定義されていません")


def check_data_replace_block_seq(data, key, expand_option, path):
    if "{{}}" in data[key]:
        assert expand_option[f'block_seq_{key}'] != "", err(path, data, "{{}}" + f'が存在しているが, root.seqで{key}が定義されていません')


def check_data_replace_block(data, key, expand_option, path):
    if "????" in data[key]:
        assert expand_option["q2"] != "", err(path, data, "????が存在しているが, [[block.block]]の前でq_rangeが定義されていません")
    if "??" in data[key]:
        assert expand_option["q1"] != "", err(path, data, "??が存在しているが, [[block]]の前でq_rangeが定義されていません")


def check_sgc_params(data, path):
    assert isinstance(data["params"], int) and 6 >= data["params"] >= 0, err(path, data, "paramsには0~6の整数を指定してください")
    param_list = ["name", "is_no_code", "code", "params", "is_danger", "is_restricted", "desc", "note"]

    if data["params"] != 0:
        for i in range(data["params"]):
            assert f"param{i+1}type" in data, err(path, data, f'params={data["params"]}と定義していますが, param{i+1}typeが存在しません')
            check_param(f"param{i+1}type", data, path)
            param_list.extend([f"param{i+1}type", f'param{i+1}desc'])
    assert len([v for k, v in data.items() if k not in param_list]) == 0, err(path, data, f'{"/".join(param_list)}以外のキーは指定できません.\nキーを確認してください')


def check_tlm_poly(data, path):
    param_list = ["type", "name", "exp", "is_hex", "status", "desc", "note"]
    poly_index = 0
    for k in data:
        if k in [f"a{i}" for i in range(6)]:
            assert f'a{poly_index}' == k, err(path, data, f'{"/".join(param_list)}以外のキーは指定できません(a0~a5は順に指定する必要があります).\nキーを確認してください')
            assert isinstance(data[f"a{poly_index}"], float) or isinstance(data[f"a{poly_index}"], int), err(path, data, f'{"a"+str(poly_index)}には整数か小数を指定してください')
            param_list.append(f"a{poly_index}")
            poly_index += 1
    else:
        assert len([v for k, v in data.items() if k not in param_list]) == 0, err(path, data, f'{"/".join(param_list)}以外のキーは指定できません.\nキーを確認してください')


def check_only_comment(data, path):
    assert list(data.keys()) == ["comment"], err(path, data, f'commentを定義する場合, comment以外のキーは指定できません.')
