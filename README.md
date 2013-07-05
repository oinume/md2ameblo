# md2ameblo
Markdownのテキストをアメブロのエディタで貼り付け可能なHTMLに変換するヤツ

# サンプル
http://md2ameblo.herokuapp.com/

# ローカルで動かす
必要なもの

* Python 2.7
* pip

```sh
$ pip install -r requirements.txt
$ ./run.sh
```

ブラウザから http://localhost:5000/ にアクセスする

# 仕様
* #, ##はは全て h3 タグに変換される(アメブロが h2 まで使ってるので)
* \`\`\`code\`\`\` は pre タグになる
* アメブロでは、ul タグなどの中のリストであっても改行を入れると br に変換してくれるので、この辺の改行の調整が入っている
