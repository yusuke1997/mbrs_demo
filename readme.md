# 的川君のデモ環境構築



## Installation

- `git clone git@github.com:dmort27/epitran.git`
- `git clone git@github.com:lart-rt/rule_kana_to_ipa.git`

`rule_kana_to_ipa`中にある`rules/*.csv`を`epitran/epitran/data/map`へコピー。

`rules/*.txt`を`epitran/epitran/data/post`にコピー。

そして`eritran`内部で`pip install -e .`でインストール

次に

```bash
pip install streamlit
pip install watchdog
pip install python-Levenshtein
pip install pykakasi
pip install fastapi
pip install uvicorn
pip install httpx
```

を行う。

```
python analyse_dif_for_website.py
```

を実行して`analyzed_wordlist.json`を得る。これはエラー分析をone hot表現で保存している。



## 実行

```bash
python backend.py
streamlit run api.py
```

これでたぶん`localhost:8091`に本番のapi, `localhost:8081`にフロント側が立っているはず。



## 工夫点

- そのまま実行したらpandasの設定から結構重くなったので、あくまで最小限にするためにpickleファイルから読み込みに変更。
- fastapiをあらかじめ立ち上げておいて、それとの通信で行うことにした。

# mbrs_web
