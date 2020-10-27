# Go To Eat を地図に出してみた

Go To Eatの店舗を地図に出してみました。
現在は埼玉県川口市、さいたま市浦和区 の情報のみを表示しています。

https://inajob.github.io/go-to-eat-map/

これは埼玉県のGo To Eatの食事券が使える店舗です。
これ以外に予約サイトのポイントがたまるというのもGo To Eatの施策がありますが、そちらに対応している店舗はもっとあるはずです。

## データ取得方法のメモ

[埼玉県のGo To Eatの対象店舗一覧ページ](https://saitama-goto-eat.com/store.html)にて下記スクリプトをChromeのコンソールに入力することで、生データが取得できます。
7行ごとに1レコードとして取り込むことで、Go To Eatの対象店舗データをコンピュータで扱いやすい形式に変換できます。

```
Array.prototype.slice.bind($(".storebox span"))().map((e) => {return e.firstChild?e.firstChild.nodeValue:""}).join("\n")
```

このデータは `data/{pref}-raw.txt` というファイル名でUTF8で保存します。

その後 `bat/parse-raw.py {pref}` を実行することで `data/{pref}.js` が出力されます。

`index.html`の中で各データを読み込んでいる箇所があるので、新しいものを追加すれば追加完了です。
