# TlmCmd DB

- C2A を搭載した OBC 以外を含めたすべてのコンポーネント(コンポ)についてのテレメトリ・コマンド(テレコマ)を，統一的に管理するための Database のマスターファイル.
    - これによって, 統一的な C2A の自動コード生成や, 各コンポ試験時の WINGS 連携が可能となる.

## 想定しているディレクトリ構成

```txt
data
├─ tlm-cmd-db: このレポジトリ
├─ settings.json: tlm-cmd/settings_example.jsonをコピーして適切に書き換えた設定ファイル
├─ DataBase
│  ├─ TLM_DB
│  │  ├─status.toml: statusを記述したtomlファイル
│  │  ├─csv: calced_dataにあたるdata
│  │  ├─md: 一覧表示用
│  │  └─toml: 編集するファイル群
│  │  　  ├─<db_prefix>_TLM_DB.toml: 共通部分をまとめたファイル
│  │  　  ├─<db_prefix>_TLM_DB_<tlm_name1>.toml
│  │  　  ├─<db_prefix>_TLM_DB_<tlm_name2>.toml
│  │  　  └─...
│  └─ CMD_DB
│  　  ├─csv: calced_dataにあたるdata
│  　  ├─md: 一覧表示用
│  　  └─toml: 編集するファイル群
│  　  　  ├─<db_prefix>_CMD_DB_BCT.toml
│  　  　  └─<db_prefix>_CMD_DB_CMD_DB.toml
├─ DataBaseAobc(optional)
│  ├─ TLM_DB
│  └─ CMD_DB
└─ DataBaseAobc(optional)
　  ├─ TLM_DB
　  └─ CMD_DB
```

## 使い始めるまで

```bash
# 依存パッケージ(toml)のインストール
pip install -r requirements.txt

# 導入したいディレクトリ(`data`など)に移動
cd <path_to_root_dir>

# 導入したいディレクトリ(`data`など)にクローン
git clone git@github.com:ut-issl/tlm-cmd-db.git
# git clone https://github.com/ut-issl/tlm-cmd-db.git
cd tlm-cmd-db
git pull origin feature/excel2toml

# tlm-cmd-dbと同じ階層(tlm-cmd-db内ではない)に`tlm-cmd-db/settings_example.json`を`settings.json`としてコピペ
cd ..
cp tlm-cmd-db/settings_example.json settings.json

# 出力先のディレクトリを作成する(`DataBase`など)
mkdir <output_dir>

# ===================
# `settings.json`内の設定を適切に書き換える(設定項目は後述)
# ===================

# 元となるデータベースからtomlファイルを生成
# 以下で引数に元となるデータベースの`TLM_DB`, `CMD_DB`の親ディレクトリのパスを指定
python tlm-cmd-db/convert2toml.py <path_to_input_db_root_path>

# ===================
# C2Aでコード生成する場合を考えて
# dest_pathにあたるディレクトリが存在することを確認する.
# ===================

# ===================
# TLM_DBのtomlファイルの共通部分を
# <db_prefix>_TLM_DB.tomlに記述する
# 少なくともファイルの作成は必須としている
# ===================

# 以下でエラーチェックをした上でcsvファイル/mdファイル/c2a関連プログラムを生成
python tlm-cmd-db/check.py

# ===================
# 以降`<output_dir>/TLM_DB/toml/*.toml`, `<output_dir>/CMD_DB/toml/*.toml`を編集して
# python tlm-cmd-db/check.py
# を実行
# ===================
```

## 使い方

tomlファイルをチェックしてmdファイル/csvファイル/c2a関連プログラムを生成

```bash
python check.py
```

既存のDBをtomlファイルベースのDBに変換(`settings.json`の`db_path`に出力)

```bash
python convert2toml.py <path_to_input_db_root_path>
```

### 実行例

以下は特に設定せずとも実行可能

```bash
# 既存のDBをtomlファイルベースのDBに変換(Examples/TLM_DB/toml_exampleとExacmples/CMD_DB/toml_exampleに出力)
python convert2toml.py Examples/csv_input

# tomlファイルをチェックしてmd/csv/c2aを出力
python check.py
```

## settings.jsonの書き方

```jsonc
{
    "is_main_obc": true, // MOBCかどうか
    "is_c2a_enable": true, // C2A関連プログラムを生成するか

    "db_prefix": "SAMPLE_MOBC", // ファイル名のプレフィックス
    "db_path": "Examples", // TLM_DB, CMD_DBが含まれるディレクトリのsettings.jsonからの相対パス
    "dest_path": "Examples/C2A", // C2Aコードの出力先, settings.jsonからの相対パス
    "max_tlm_num": 432, // 許容最大パケット

    "other_obc_data": [ // "is_main_obc": true の場合のみ必要
        {
            "name": "AOBC", // DBの名前
            "is_enable": true, // コード生成するか

            "db_prefix": "SAMPLE_AOBC", // ファイル名のプレフィックス
            "db_path": "Examples/AOBC", // TLM_DB, CMD_DBが含まれるディレクトリのsettings.jsonからの相対パス
            "dest_path": "Examples/C2A/AOBC", // C2Aコードの出力先, settings.jsonからの相対パス
            "max_tlm_num": 1000, // 許容最大パケット

            // tlm-buffer.c, tlm-buffer.h生成に必要な設定
            "driver_name": "aobc_driver",
            "driver_type": "AOBC_Driver",
            "code_when_tlm_not_found": "aobc_driver->info.comm.rx_err_code = AOBC_RX_ERR_CODE_TLM_NOT_FOUND;"
        }
    ]
}
```

## status.tomlの書き方

* statusを下のように一つ一つ記述する
* キー`[status.x.x]`を被らないように設定する
    * デフォルトでは`[status.<enumの取る値の数>.<index>]`としている
* 実行時に同じ階層に`status.md`が生成される

```toml
[status.2.1]
0 = "SUCCESS"
1 = "ERROR"

[status.2.2]
0 = "FINISHED"
1 = "PROGRESS"
"*" = "N/A"
```

## tomlの書き方

`Examples/README.md`を参照

## エラーチェック内容

* `settings.json`の設定内容
* `status.toml`の設定内容
* seq, block周りの文法ミス
* max_tlm_numを超えないこと
* TLM_DB
    * `Target,PacketID,Enable/Disable,IsRestricted,Local Var`が設定されていること
    * ビット圧縮している場合,ビット長の合計が型にあっていること
    * `Type`が適当であること
    * 式の左カッコと右カッコの数が等しいこと
    * `HEX, STATUS, POLY`が排他であること
* その他様々
