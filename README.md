# Django Sample App
[株式会社フンザ](http://hunza.jp/)のDjangoアプリケーションのコーディング例を示したレポジトリです。

## テストの実行方法
特定のモジュールのユニットテストを実行。

```
./manage.py test sample
```

ユニットテストのサブモジュールを指定してユニットテストを実行。

```
./manage.py test sample.tests.test_views
```

特定のテストケースのみ実行。

```
./manage.py test sample.tests.test_views.TopViewTestCase
```

カバレッジを計測しつつテストを実行。

```
coverage run --source=sample ./manage.py test sample
```

カバレッジレポートを出力。

```
coverage report
```

カバレッジレポートをHTMLで`cover`ディレクトリに出力。

```
coverage html --directory=cover
```
