##########################################
#
# 不動産ページから情報を取得する(1ページのみ)
#
##########################################


# ライブラリインポート
from bs4 import BeautifulSoup
import requests
# pprintをインポートする
from pprint import pprint

# RequestsでURLにアクセスしてHTMLを解析
# 変数urlにSUUMOホームページのURLを格納する
url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'

# アクセスするためのURLをtarget_urlに格納する
target_url = url.format(1)

# print()してtarget_urlを確認する
# print(target_url)

# target_urlへのアクセス結果を、変数rに格納
r = requests.get(target_url)

# 取得結果を解析してsoupに格納
soup = BeautifulSoup(r.text)

# soupから情報を抽出する
# cassetteクラスを持ったdivタグをすべて取得して、変数contentsに格納
contents = soup.find_all('div', class_='cassetteitem')

# 初期値が20になっていることを確認
# print(len(contents))

# 変数contentにcontentsの最初の要素を格納する
content = contents[0]

# ほしい情報############################################
# 物件情報
# 物件名 => title
# 住所 => address
# アクセス => access
# 築年数 => age
# 部屋情報
# 物件の階数 => floor
# 物件の賃料/管理費 => price
# 物件の敷金・礼金  => first_fee
# 物件の間取り・面積 => capacity
#######################################################

# 物件情報と部屋情報が入ったブロックを取得する
# 物件・建物情報を変数detailに格納する
detail = content.find('div', class_='cassetteitem-detail')

# 各部屋の情報を変数tableに格納する
table = content.find('table', class_='cassetteitem_other')

# 物件情報を抽出する
# 変数titleに、物件名を格納する
title = detail.find('div', class_='cassetteitem_content-title').text

# 変数addressに住所を格納する
address = detail.find('li', class_='cassetteitem_detail-col1').text

# 変数accessにアクセス情報を格納する
access = detail.find('li', class_='cassetteitem_detail-col2').text

# 変数ageに築年数を格納する
age = detail.find('li', class_='cassetteitem_detail-col3').text

# 部屋情報を抽出する
# 変数tableからすべてのtrタグを取得して、変数tr_tagsに格納
tr_tags = table.find_all('tr', class_='js-cassette_link')

# tr_targsの中から最初の1つだけtr_tagに格納
tr_tag = tr_tags[0]

# 変数floor, price, first_fee, capacityに4つの情報を格納する
floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]

# 変数feeとmanagement_feeに、賃料と管理費を格納する
fee, management_fee = price.find_all('li')

# 変数depositとgratuityに、敷金と礼金を格納する
deposit, gratuity = first_fee.find_all('li')

# 変数madoriとmensekiに、間取りと面積を格納する
madori, menseki = capacity.find_all('li')

# 取得した情報を辞書に取得する
# title: 物件の名前
# address: 住所
# access: アクセス
# age: 築年数
# floor: 部屋の階数
# fee: 部屋の賃料
# management_fee: 管理費
# deposit: 敷金
# gratuity: 礼金
# madori: 間取り
# menseki: 専有面積

# 変数dに、これまで取得した11項目を格納する
d = {
    'title': title,
    'address': address,
    'access': access,
    'age': age,
    'floor': floor.text,
    'fee': fee.text,
    'management_fee': management_fee.text,
    'deposit': deposit.text,
    'gratuity': gratuity.text,
    'madori': madori.text,
    'menseki': menseki.text
}

# 1ページ目からすべての情報を取得する
# 変数d_listに空のリストを作成する
d_list = []


# すべての物件情報(20件)を取得する
contents = soup.find_all('div', class_='cassetteitem')


# 各物件情報をforループで取得する
for content in contents:
    # 物件情報と部屋情報を取得しておく
    detail = content.find('div', class_='cassetteitem_content')
    table = content.find('table', class_='cassetteitem_other')

    # 物件情報から必要な情報を取得する
    title = detail.find('div', class_='cassetteitem_content-title').text
    address = detail.find('li', class_='cassetteitem_detail-col1').text
    access = detail.find('li', class_='cassetteitem_detail-col2').text
    age = detail.find('li', class_='cassetteitem_detail-col3').text

    # 部屋情報のブロックから、各部屋情報を取得する
    tr_tags = table.find_all('tr', class_='js-cassette_link')

    # 各部屋情報をforループで取得する
    for tr_tag in tr_tags:

        # 部屋情報の行から、欲しい情報を取得する
        floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]

        # さらに細かい情報を取得する
        fee, management_fee = price.find_all('li')
        deposit, gratuity = first_fee.find_all('li')
        madori, menseki = capacity.find_all('li')

        # 取得したすべての情報を辞書に格納する
        d = {
            'title': title,
            'address': address,
            'access': access,
            'age': age,
            'floor': floor.text,
            'fee': fee.text,
            'management_fee': management_fee.text,
            'deposit': deposit.text,
            'gratuity': gratuity.text,
            'madori': madori.text,
            'menseki': menseki.text
        }

        # 取得した辞書をd_listに格納する
        d_list.append(d)

# d_listに入っているインデックスの0番目と1番目を確認する
pprint(d_list[0])
print()
pprint(d_list[1])
