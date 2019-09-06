# clang_parse

* google coding ruleの命名規則に準拠していないコードを検出する
* 検出した結果のrenameは`git sed`や`clang-rename`を利用する

## how to download sample cpp files
```
git clone https://github.com/c42f/tinyformat
```

## TODO
* pip installの対応
* vprint libraryの切り出し
* 検出範囲の制御
  * 指定repo以外を除外
* 実際のコードに適用し，不足部分の洗い出し

## how to test
```
./simple_test.sh sample.cpp
```

前提条件
* `bad`や`good`を含んだ名称でテスト対象のcppコードを記述する
