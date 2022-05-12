# TlmCmd DB

- C2A を搭載した OBC 以外を含めたすべてのコンポーネント（コンポ）についてのテレメトリ・コマンド（テレコマ）を，統一的に管理するための Database のマスターファイル．
    - これによって，統一的な C2A の自動コード生成や，各コンポ試験時の WINGS 連携が可能となる．
- これまで Excel マクロブックを用いていたが, 軽量化のため toml ファイルを用いることとした
- 以下の理由より脱Excelが唱えられていた
    - 動作が重い
    - Excel に埋め込まれる VBA が git 管理しづらい．
    - Windows 以外で使いづらい．

## 使い方

### 前提

* `status.toml`, `check.py`, `settings.json`が同じ階層にあること
* `settings.json`が適切に記述されていること
* `status.toml`が適切に記述されていること

### コマンド

* 既存のcsvファイル: 既存のExcelファイルと同じ階層にあるcsvファイル
* 引数の順序は任意

```bash
# <path_to_csv_dir>: csvファイルか, csvファイルが含まれるディレクトリ(ディレクトリ内の全てのcsvが対象)
# 既存のCMD_DBのcsvファイルからtomlファイルを生成
python check.py --cmd --input <path_to_csv_file_or_dir> --obc <mobc/aobc/tobc>
# 既存のTLM_DBのcsvファイルからtomlファイルを生成
python check.py --tlm --input <path_to_csv_file_or_dir> --obc <mobc/aobc/tobc>

# tomlファイルをチェックしてmdファイルとcsvファイルを生成(settings.jsonが適切に設定されている場合)
python check.py

# TLM_DB/CMD_DBのみ実行
python check.py --tlm/--cmd

# settings.jsonで設定したパスとは異なるディレクトリにあるtomlファイルを対象にする場合
# --tlm or --cmdの指定が必要
python check.py --tlm/--cmd --toml <path_to_toml_dir>

# settings.jsonで設定したパスとは異なるディレクトリにmd/csvファイルを出力
# --tlm or --cmdの指定が必要
python check.py --tlm/--cmd --csv <path_to_csv_dir> --md <path_to_md_dir>

# settings.jsonで設定したパスとは異なるディレクトリにあるtomlファイルからsettings.jsonで設定したパスとは異なるディレクトリにmd/csvファイルを出力
python check.py --tlm/--cmd --toml <path_to_toml_dir> --csv <path_to_csv_dir> --md <path_to_md_dir>
```

## settings.jsonの書き方

* OBCの種類を大文字で記述することに注意する

```json
{
    "tlm": { // TLM_DB
        "is_check": true, // デフォルトでエラーチェックを行うか
        "path": { // check.pyからの相対パス
            "csv": "TLM_DB/csv", // csvファイルの出力先
            "md": "TLM_DB/md", // mdファイルの出力先
            "toml": "TLM_DB/toml" // tomlファイルの出力先,入力元
        }
    },
    "cmd": { // CMD_DB
        "is_check": true, // デフォルトでエラーチェックを行うか
        "path": { // check.pyからの相対パス
            "csv": "CMD_DB/csv", // csvファイルの出力先
            "md": "CMD_DB/md", // mdファイルの出力先
            "toml": "CMD_DB/toml" // tomlファイルの出力先,入力元
        }
    },
    "obc_data": { // 各OBCのデータ
        "MOBC": { // 大文字
            "max_packet": 432 // 許容最大パケット
        }
    }
}
```

## status.tomlの書き方

* statusを下のように一つ一つ記述する
* キー`[status.x.x]`を被らないように設定する
    * デフォルトでは`[status.<enumの取る値の数>.<index>]`としている

```toml
[status.2.1]
0 = "SUCCESS"
1 = "ERROR"

[status.2.2]
0 = "FINISHED"
1 = "PROGRESS"
"*" = "N/A"
```

なお, `check.py`を実行すると`status.md`が自動的に生成される

## tomlの書き方

### TLM_DBの場合

* 最初の5行は以下のような設定を置く

```toml
obc = "MOBC" # mobcなどを指定
Target = "OBC"
PacketID = "0x45"
"Enable/Disable" = "ENABLE"
IsRestricted = "FALSE"
"Local Var" = ""
```

* 各フィールドは以下の例ような構成(bit圧縮なし)
    * is_hex と status は排他なので片方のみ指定可能

```toml
[[tlm_field]] # 各フィールドの最初に設置
name = "APP0_INITIALIZER" # Name
type = "uint32_t" # Var. Type
exp = "(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].initializer)" # Variable of Function Name
is_hex = true # HEXの場合
status = "6.1" # status.tomlで設定したキーを指定
desc = "" # Desc.
note = "" # Note
```

* bit圧縮がある場合は以下の例ような構成

```toml
[[tlm_field]] # 各フィールド最初に設置
type = "uint16_t" # type と exp はここに設置
[[tlm_field.comp]] # ビット圧縮をする各フィールドに設置
name = "PH.VER" # Name
bitlen = 3 # ビット長
desc = "" # Desc. と Noteはcomp内に設置
note = ""
[[tlm_field.comp]]
name = "PH.TYPE"
bitlen = 1
[[tlm_field.comp]]
name = "PH.SH_FLAG"
bitlen = 1
[[tlm_field.comp]]
name = "PH.APID"
bitlen = 11
```

### CMD_DBの場合

* 最初の行は以下のような設定を置く

```toml
obc = "MOBC"
```

* 各フィールドは以下のような構成
    * パラメタは6つまで設定可能

```toml
[[C2A_CORE]] # 各フィールドの名前
name = "Cmd_TMGR_UPDATE_UNIXTIME" # Name
desc = "MOBC UNIXTIME修正コマンド" # Desc.
note = "" # Note
[[C2A_CORE.params]] # 各パラメタの最初に設置
type = "double" # type
desc = "unixtime" # 説明
[[C2A_CORE.params]]
type = "uint32_t"
desc = "total_cycle"
[[C2A_CORE.params]]
type = "uint32_t"
desc = "step"
```

### 指定できる`Var. Type`

| type     | bit数 |
| -------- | ----- |
| int8_t   | 8     |
| int16_t  | 16    |
| int32_t  | 32    |
| uint8_t  | 8     |
| uint16_t | 16    |
| uint32_t | 32    |
| float    | 32    |
| double   | 64    |

## エラーチェック内容

### 共通

* `settings.json`の設定内容

### TLM_DB

* `obc,Target,PacketID,Enable/Disable,IsRestricted,Local Var`が設定されていること
* ビット圧縮している場合,ビット長の合計が型にあっていること
* `Var. Type`が適当であること
* 式の左カッコと右カッコの数が等しいこと
* PH,SHが既定のものと一致していること
* `HEX, STATUS, POLY`が排他であること
* `status.toml`にstatusが網羅されていること

## 自動コード生成(未実装)

- C2A のコードは [c2a-tlm-cmd-code-generator](https://github.com/ut-issl/c2a-tlm-cmd-code-generator) で自動生成できる．

## 開発者向け

ディレクトリ構成

* `modules`
    * `csv2toml.py`: csvファイルからtomlファイルを出力
    * `checktoml.py`: エラーチェック用
    * `toml2mdcsv.py`: tomlファイルからcsvファイルやmdファイルを出力
    * `utils.py`: 共通のデータ(settings.json, status.toml)や関数(パス取得, 引数チェック)など
* `check.py`
    * 実行部分
