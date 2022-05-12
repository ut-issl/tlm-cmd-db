# tomlファイルの書き方

## 指定できるtype

| type     | bit数 | 備考    |
| -------- | ----- | ------- |
| int8_t   | 8     |
| int16_t  | 16    |
| int32_t  | 32    |
| uint8_t  | 8     |
| uint16_t | 16    |
| uint32_t | 32    |
| float    | 32    |
| double   | 64    |
| raw      | -     | SGCのみ |

## TLM_DB

* 共通部分は`<prefix>_TLM_DB.toml`に置く
    * `Examples/TLM_DB/SAMPLE_MOBC_TLM_DB.toml`参照
* 最初の5行は以下のように設定を置く

```toml
Target = "OBC"
PacketID = "0x45"
"Enable/Disable" = "ENABLE"
IsRestricted = "FALSE"
"Local Var" = ""
```

* 各フィールドは以下のような構成(bit圧縮なしの場合)
    * is_hex と status と poly(a0~a5) は排他なので片方のみ指定可能

```toml
[[tlm]] # 各フィールドの最初に設置
name = "APP0_INITIALIZER" # 必須
type = "uint32_t" # 必須
exp = "(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].initializer)" # Variable of Function Name
is_hex = true # HEXの場合
status = "6.1" # status.tomlで設定したキーを指定
a0 = 0.0 # POLYの場合
desc = "" # Desc.
note = "" # Note
```

* bit圧縮がある場合は以下のような構成
    * `[[tlm.comp]]`の上のtypeのビット数と`[[tlm.comp]]`内の`bitlen`の和が等しい必要がある
    * 式はそれぞれに置くことも`[[tlm.comp]]`の前に置くこともできる. それぞれに置いた場合には変換時にビット圧縮される.

```toml
[[tlm]] # 各フィールド最初に設置
type = "uint16_t" # type と exp はここに設置, 必須
[[tlm.comp]] # ビット圧縮をする各フィールドに設置
name = "PH.VER" # 必須
bitlen = 3 # ビット長, 必須
desc = "" # Desc. と Noteはcomp内に設置
note = ""
[[tlm.comp]]
name = "PH.TYPE"
bitlen = 1
[[tlm.comp]]
name = "PH.SH_FLAG"
bitlen = 1
[[tlm.comp]]
name = "PH.APID"
bitlen = 11
```

## CMD_DB

### SGC

* 各フィールドは以下のような構成
    * パラメタは6つまで設定可能

```toml
[[C2A_CORE]]
code = "0x0000" # 最初だけcodeでPacketIDを指定する必要がある
name = "Cmd_NOP"
params = 0
desc = "ダミーコマンド"

[[C2A_CORE]]
name = "Cmd_AH_REGISTER_RULE" # 必須
params = 6 # パラメタの数, 必須
param1type = "uint8_t"
param1desc = "id"
param2type = "uint8_t"
param2desc = "group"
param3type = "uint8_t"
param3desc = "local"
param4type = "uint8_t"
param4desc = "cond"
param5type = "uint8_t"
param5desc = "threshold"
param6type = "uint16_t"
param6desc = "bc_index"
is_danger = false
desc = "AHパラメタを設定する"
note = ""
```

### BCT

* 各フィールドは以下のような構成

```toml
[[bct]]
name = "BC_HK_CYCLIC_TLM" # 必須
sname = "BC_HK10S" # short name
bcid = 60 # 必須
is_deploy = true
is_setblockposition = true
is_clear = true
is_activate = true
is_inactivate = true
desc = ""
note = ""
```

* コメントを残したい場合には, `comment`だけを持つフィールドを作る

```toml
[[bct]]
comment = """==== 各系領域 ====
./C2A/TlmCmd/NormalBlockCommandDefinition/で定義
アノマリハンドラはBC_AH_など，接頭辞を適切につけること！"""
```

## より単純化するために(block, seq)

* 一部共通しているフィールドについてはblockやseqを用いてまとめることができる.
* `python check.py`の実行時にblock, seqを展開したtomlファイルが`<path_to_toml>/expanded`以下に出力される
* 以下で説明するが, `<path_to_toml>`配下のtomlファイルと`<path_to_toml>/expanded`配下のtomlファイルを見比べれば便利さが分かる
* 間違っている場合にはエラーが出力されるので積極的にまとめることを推奨する
* まとめ方の例は`Examples/TLM_DB/toml/SAMPLE_MOBC_TLM_DB_HK.toml`にある

### チートシート

| まとめたい項目                     | 何を用いるか | base(1階層目)に置くもの | base(2階層目)に置くもの | 各フィールド                       |
| ---------------------------------- | ------------ | ----------------------- | ----------------------- | ---------------------------------- |
| 0, 1, 2, 3, 4                      | block        | q_range=[0, 4]          |                         | "??"                               |
| 00, 0, 01, 1, 02, 2                | block        | q_range=[0, 2]          |                         | "0??", "??"                        |
| 0-0, 0-1, 1-0, 1-1, 2-0, 2-1       | block.block  | q_range=[0, 2]          | q_range=[0, 1]          | "??-????"                          |
| abc_a, abc_b, abc_c                | seq          | xxx_base="abc_{}"       |                         | "a", "b", "c"                      |
| a-xx-b, c-xx-d, e-xx-f             | seq          | xxx_base="{}-xx-{}"     |                         | ["a", "b"], ["c", "d"], ["e", "f"] |
| a-xx-a, b-xx-b, c-xx-c             | seq          | xxx_base="{}-xx-{}"     |                         | "a", "b", "c"                      |
| 0-abc_a, 0-abc_b, 1-abc_a, 1-abc_b | block.seq    | q_range=[0, 1]          | xxx_base="??-abc_{}"    | "a", "b"                           |
| abc_a-0, abc_a-1, abc_b-0, abc_b-1 | seq.block    | xxx_base="abc_{}-??"    | q_range=[0, 1]          | "a", "b"                           |

blockとseqを同じ階層に置く使い方もできる.

#### 利用例

`TLM_DB/toml/SAMPLE_MOBC_TLM_DB_HK.toml`にコメント付きで様々な使い方が記載されていて
`TLM_DB/toml/expanded/SAMPLE_MOBC_TLM_DB_HK.toml`にseq,block展開後のものがあるので比較すると分かりやすい

| seq&block例     |
| --------------- |
| comp            |
| block           |
| seq             |
| block.comp      |
| seq.comp        |
| block.seq       |
| block.block     |
| block.seq.comp  |
| block.seq.block |
| block & seq     |

### block

* フィールドの中に登場する連続する数字を`??`としてまとめる.
    * 連続する数字の範囲を`q_range=[start, end]`として指定する
    * blockの前にはblockの数`block_num`を指定する
* 以下のキーで利用できる
    * TLM_DB: name, exp
    * CMD_DB, SGC: name
    * CMD_DB, BCT: name, bcid
* (TLM_DBのみ)typeは`q_range`と同じ階層で定義すると全て共通になる. 個別に設定したい場合には各blockで定義する
* (TLM_DBのみ)キャストする場合を考えてtypeも置換したい時は`(uint8_t)`などを`{type}`とする.

#### blockが1つのとき

* イメージ
    * フィールド内に出てくる数字が0, 1, 2, 3, ...となる場合をまとめられる

共通化前

```toml
[[tlm]]
name = "APP0_INITIALIZER"
exp = "(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].initializer)"
type = "uint32_t"
is_hex = true

[[tlm]]
name = "APP1_INITIALIZER"
exp = "(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+1].initializer)"
type = "uint32_t"
is_hex = true

[[tlm]]
name = "APP2_INITIALIZER"
exp = "(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+2].initializer)"
type = "uint32_t"
is_hex = true
```

共通化後

```toml
[[tlm]]
q_range = [0, 2]
block_num = 1
[[tlm.block]]
name = "APP??_INITIALIZER"
exp = "(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+??].initializer)"
type = "uint32_t"
is_hex = true
```

#### blockが複数のとき

* イメージ
    * 0, 0, 0, 1, 1, 1, 2, 2, 2, ...の場合をまとめられる

共通化前

```toml
[[tlm]]
name = "CMD0_ID"
type = "uint16_t"
exp = "(uint16_t)BCT_get_id(block_command_table->pos.block, 0)"
is_hex = true

[[tlm]]
name = "CMD0_TI"
type = "uint32_t"
exp = "(uint32_t)BCT_get_ti(block_command_table->pos.block, 0)"

[[tlm]]
name = "CMD1_ID"
type = "uint16_t"
exp = "(uint16_t)BCT_get_id(block_command_table->pos.block, 1)"
is_hex = true

[[tlm]]
name = "CMD1_TI"
type = "uint32_t"

exp = "(uint32_t)BCT_get_ti(block_command_table->pos.block, 1)"
[[tlm]]
name = "CMD2_ID"
type = "uint16_t"
exp = "(uint16_t)BCT_get_id(block_command_table->pos.block, 1)"
is_hex = true

[[tlm]]
name = "CMD2_TI"
type = "uint32_t"
exp = "(uint32_t)BCT_get_ti(block_command_table->pos.block, 1)"
```

共通化後

```toml
[[tlm]]
q_range = [0, 2]
block_num = 2
[[tlm.block]]
name = "CMD??_ID"
type = "uint16_t"
exp = "(uint16_t)BCT_get_id(block_command_table->pos.block, ??)"
is_hex = true
[[tlm.block]]
name = "CMD??_TI"
type = "uint32_t"
exp = "(uint32_t)BCT_get_ti(block_command_table->pos.block, ??)"
```

#### blockが2階層ある場合

* 連続する数字を`????`に置換する
    * `q_range=[start, end]`もしくは`q_range=[start, end, 1]`とする
    * 最後に1を追加した場合, `start=??の置換先の数 * ????の置換先の数`となる
* イメージ
    * 0-0, 0-1, 0-2, 0-3, 1-0, 1-1, 1-2, 1-3, 2-0, ...の場合をまとめられる(2階層目で`q_range=[0, 3]`)
    * 0-0, 0-1, 0-2, 0-3, 1-4, 1-5, 1-6, 1-7, 2-8, ...の場合もまとめられる(2階層目で`q_range=[0, 3, 1]`)

共通化前

```toml
[[tlm]]
name = "CMD0_ID"
type = "uint16_t"
exp = "(uint16_t)BCT_get_id(block_command_table->pos.block, 0)"
is_hex = true

[[tlm]]
name = "CMD0_TI"
type = "uint32_t"
exp = "(uint32_t)BCT_get_ti(block_command_table->pos.block, 0)"

[[tlm]]
name = "CMD0_PARAM0"
type = "uint8_t"
exp = "BCT_get_param_head(block_command_table->pos.block, 0)[0]"
is_hex = true

[[tlm]]
name = "CMD0_PARAM1"
type = "uint8_t"
exp = "BCT_get_param_head(block_command_table->pos.block, 0)[1]"
is_hex = true

[[tlm]]
name = "CMD0_PARAM2"
type = "uint8_t"
exp = "BCT_get_param_head(block_command_table->pos.block, 0)[2]"
is_hex = true

[[tlm]]
name = "CMD1_ID"
type = "uint16_t"
exp = "(uint16_t)BCT_get_id(block_command_table->pos.block, 1)"
is_hex = true

[[tlm]]
name = "CMD1_TI"
type = "uint32_t"
exp = "(uint32_t)BCT_get_ti(block_command_table->pos.block, 1)"

[[tlm]]
name = "CMD1_PARAM0"
type = "uint8_t"
exp = "BCT_get_param_head(block_command_table->pos.block, 1)[0]"
is_hex = true

[[tlm]]
name = "CMD1_PARAM1"
type = "uint8_t"
exp = "BCT_get_param_head(block_command_table->pos.block, 1)[1]"
is_hex = true

[[tlm]]
name = "CMD1_PARAM2"
type = "uint8_t"
exp = "BCT_get_param_head(block_command_table->pos.block, 1)[2]"
is_hex = true
```

共通化後

```toml
[[tlm]]
q_range = [0, 1]
block_num = 3
[[tlm.block]]
name = "CMD??_ID"
type = "uint16_t"
exp = "(uint16_t)BCT_get_id(block_command_table->pos.block, ??)"
is_hex = true
[[tlm.block]]
name = "CMD??_TI"
type = "uint32_t"
exp = "(uint32_t)BCT_get_ti(block_command_table->pos.block, ??)"
[[tlm.block]]
q_range = [0, 2]
block_num = 1
[[tlm.block.block]]
name = "CMD??_PARAM????"
type = "uint8_t"
exp = "BCT_get_param_head(block_command_table->pos.block, ??)[????]"
is_hex = true
```

### seq

* フィールドの中に登場する共通の文字列以外を`{}`としてまとめる.
    * 共通部分をseqの前で`name_base`や`exp_base`として指定する
    * seqの前にはseqの数`seq_num`を指定する
* 以下のキーで利用できる
    * TLM_DB: name, exp(name_base,exp_base)
    * CMD_DB, SGC: name(name_base)
    * CMD_DB, BCT: name(name_base)
* (TLM_DBのみ)typeは`name_base`と同じ階層で定義すると全て共通になる. 個別に設定したい場合には各seqで定義する
* seqは1階層のみ利用できる
* クラスでまとまり意識が持てる
* イメージ
    * abcdef_a,abcdef_b,abcdef_c,abcdef_d
    * seq
        * base: abcdef_{}
        * seq1: a, seq2: b, seq3: c, seq4: d

共通化前

```toml
[[tlm]]
name = "ROTATE_NEXT_CMD"
exp = "BCE_get_bc_exe_params(block_command_table->pos.block)->rotate.next_cmd"
type = "uint8_t"

[[tlm]]
name = "ROTATE_COUNTER"
exp = "BCE_get_bc_exe_params(block_command_table->pos.block)->rotate.counter"
type = "uint16_t"

[[tlm]]
name = "ROTATE_INTERVAL"
exp = "BCE_get_bc_exe_params(block_command_table->pos.block)->rotate.interval"
type = "uint16_t"
```

共通化後

```toml
[[tlm]]
name_base = "ROTATE_{}"
exp_base = "BCE_get_bc_exe_params(block_command_table->pos.block)->rotate.{}"
seq_num = 3
[[tlm.seq]]
type = "uint8_t"
name = "NEXT_CMD"
exp = "next_cmd"
[[tlm.seq]]
type = "uint16_t"
name = "COUNTER"
exp = "counter"
[[tlm.seq]]
type = "uint16_t"
name = "INTERVAL"
exp = "interval"
```

### block & seq

* 特殊な場合
* イメージ
    * 0-abcdef_a, 0-xyz_a, 1-abcdef_b, 1-xyz_b, 2-abcdef_c, 2-xyz_c
    * seq
        * seq1: a, seq2: b, seq3: c
    * block
        * block1: ??-abcdef_{{}}, block2: ??-xyz_{{}}
