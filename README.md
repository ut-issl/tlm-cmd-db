# TlmCmd DB
- C2A を搭載した OBC 以外を含めたすべてのコンポーネント（コンポ）についてのテレメトリ・コマンド（テレコマ）を，統一的に管理するための Database のマスターファイル．
    - これによって，統一的な C2A の自動コード生成や，各コンポ試験時の WINGS 連携が可能となる．
- これまで Excel マクロブックの単体ファイルであったため，コンフリクトや他 SW との連携がいまいちだった．そこで，以下の点を改修した．
    - データ本体はすべて CSV として保存することで，データはテキスト化（git 管理しやすさの向上）
    - Excel マクロブック（xlsm）は純粋なビュアー，エディターとすることで， xlsm は一般ユーザーは上書き保存しなくていいように（できないように）．
- 一方で，以下の理由より，今後は脱 Excel をしていきたい．
    - Excel に埋め込まれる VBA が git 管理しづらい．
    - Windows 以外で使いづらい．

## Tlm DB のカラムの説明
- `Comment`
    - 適当な文字列（慣習的に `*` ）がある行は無視される
- `TLM Field`: テレメトリのフィールド
    - `Name`: テレメトリのフィールド名．以下の要件を満たす
        - `[A-Z_][0-9A-Z_]*` を満たす文字列
        - `.` で区切ることで階層を表現することが可能
- `Onboard Software Info.`: C2A などの FSW 側の情報（自動コード生成に用いる）
    - `Var. Type`: テレメトリの型
    - `Variable or Function Name`: FSW 上での変数名
- `Extraction Info.`: GS SW などでテレメトリを抽出するための情報
    - `Field Type`: GS の DB などに保存されるときの型． `Var. Type` と異なる型でも可能（おもにテレメ圧縮のときに有用）
    - `Pos. Designator`: パケット内のテレメトリの位置
- `Conversion Info.`: テレメトリ変換の情報
    - `Conv. Type`: 変換方式
        - `NONE`: 変換なし
        - `POLY`: 多項式変換．変換後の型はすべて `double`
        - `STATUS`: ステータス変換
        - `HEX`: 16進数変換（`Display Info.` の新設に伴い， deprecated）
- `Display Info.`: GS SW などでテレメトリを表示するときの情報
    - `Label`: ラベル．UTF-8 で表現可能な文字列が可能．空欄の場合は `TLM Field` の `Name` が使われる．
    - `Unit`: 単位．空欄可能
    - `Format`: フォーマット指定子．空欄可能．表現は GS SW 依存
- `Description`: GS SW などで表示される説明
- `Note`: この DB 上だけにある補足情報． FSW 開発者向け情報


## 値


## 使い方
### Cmd DB
- DB 読み込み
    - xlsm を開くと自動的に読み込まれる．
    - 手動で読み込む場合は，「Utility」→「CSV 読み込み」
- DB 編集
    - 通常の Excel 操作．
- DB 書き出し
    - 「Utility」→「CSV 書き出し」

### Tlm DB
- DB 読み込み
    - xlsm を開くと自動的に読み込まれる．
    - 手動で読み込む場合は，「Check」→「CSV 読み込み」
- DB 編集
    - 通常の Excel 操作．数式もそのまま保存されるため，使用可能．
- DB 書き出し
    - 「Check」→「CSV 書き出し」
- テレメトリシートの追加
    - 適当に csv をコピーしてファイル名を変更したものを同じディレクトリに配置すれば，次回以降自動で読み込まれる．

## 自動コード生成
- C2A のコードは [c2a-tlm-cmd-code-generator](https://github.com/ut-issl/c2a-tlm-cmd-code-generator) で自動生成できる．

## その他の注意
- 「開発」→「Visual Basic」→「ツール」→「参照設定」→「Microsoft HTML Object Library」にチェックを入れる必要があるかもしれない．
- 古いOffice (Office 2016など) では動かないこともあるらしい．
    - `Workbooks.Open` がクラッシュすることがある．
