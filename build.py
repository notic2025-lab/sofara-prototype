"""そふぁら サイトプロトタイプの静的ページを docs/ に書き出す。

使い方: python3 build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
SITE_URL = "https://notic2025-lab.github.io/sofara-prototype/"

ICON = {
    "cart": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M2.5 3.5h2.2l2.3 10.3c.15.7.78 1.2 1.5 1.2h8.4c.7 0 1.3-.47 1.48-1.15L20.6 7.5H5.6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="9.2" cy="19.2" r="1.5" fill="currentColor"/><circle cx="17" cy="19.2" r="1.5" fill="currentColor"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h13M13 6.5l5.5 5.5-5.5 5.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 5.5v13M5.5 12h13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "minus": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5.5 12h13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6.6 3.8h2.6l1.3 3.6-1.8 1.2a11 11 0 0 0 5 5l1.2-1.8 3.6 1.3v2.6a2 2 0 0 1-2.1 2A15.2 15.2 0 0 1 4.6 5.9a2 2 0 0 1 2-2.1z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="10" r="2.4" stroke="currentColor" stroke-width="1.7"/></svg>',
    "snow": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9M9.5 4.5 12 7l2.5-2.5M9.5 19.5 12 17l2.5 2.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="4.5" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="12" r="3.6" stroke="currentColor" stroke-width="1.7"/><circle cx="16.6" cy="7.4" r="1.1" fill="currentColor"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 20v-7h2.4l.4-2.8h-2.8V8.5c0-.8.3-1.4 1.4-1.4h1.5V4.6c-.3 0-1.2-.1-2.2-.1-2.2 0-3.6 1.3-3.6 3.7v2h-2.4V13h2.4v7" fill="currentColor"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 6.5h11v9H3zM14 9.5h3.6l3 3.2v2.8H14" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="7" cy="17.5" r="1.7" stroke="currentColor" stroke-width="1.6"/><circle cx="17" cy="17.5" r="1.7" stroke="currentColor" stroke-width="1.6"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="8.2" stroke="currentColor" stroke-width="1.7"/><path d="M12 7.5V12l3 2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
    "car": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 16.5V12l1.8-4.6A2 2 0 0 1 8.7 6h6.6a2 2 0 0 1 1.9 1.4L19 12v4.5M5 12h14M5 16.5h14" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="8" cy="16.5" r="1.6" stroke="currentColor" stroke-width="1.6"/><circle cx="16" cy="16.5" r="1.6" stroke="currentColor" stroke-width="1.6"/></svg>',
}
DOTS = '<span class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>'
WAVE_TOP = '<svg class="wave wave--mint" viewBox="0 0 390 24" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 24V14c35-8 70 8 110 0 50-10 90 8 140-2 50-10 90 14 140-2v14z"/></svg>'
WAVE_BOTTOM = '<svg class="wave wave--mint" viewBox="0 0 390 24" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 0h390v10c-50 16-90-8-140 2-50 10-90-8-140 2-40 8-75-8-110 0z"/></svg>'

TAGS = {
    "frozen": ("tag--frozen", ICON["snow"] + "冷凍・クール便"),
    "normal": ("tag--normal", "常温"),
    "bread": ("tag--bread", "冷凍パン"),
    "new": ("tag--new", "新商品"),
}

# cat: frozen = 冷凍食品, bread = 冷凍パン（冷凍食品の一部）, rice = お米・豆・お茶
PRODUCTS = [
    dict(id="koji", name="ビワマスと麹", en="BIWAMASU KOJI", cat="frozen", tag="frozen", sub="1パック115g", price=1782, img="koji.jpg",
         summary="琵琶湖のビワマスのお刺身を、そふぁらのお米でつくった自家製塩麹に漬け込みました。",
         desc="自然農法で育てたそふぁらのお米の米麹に、天日・平釜仕立ての海塩を混ぜ、地下天然水を入れて発酵させた自家製塩麹に、びわマスのお刺身を付け込みました。",
         spec=[("内容量", "1パック 115g"), ("保存方法", "冷凍で保存してください"), ("原材料", "ビワマス、米麹、海塩（正式な表示を入れます）")]),
    dict(id="oiled", name="ビワマスとオイル", en="BIWAMASU OILED", cat="frozen", tag="frozen", sub="1パック95g", price=1782, img="oiled.jpg",
         summary="ハーブと山椒の香るオイルで、びわマスを仕上げました。",
         desc="オリーブオイルにハーブ（セージ、タイムなど）と粒胡椒、山椒などを入れてあたため、塩をしたびわマスを入れました。",
         spec=[("内容量", "1パック 95g"), ("保存方法", "冷凍で保存してください"), ("原材料", "ビワマス、オリーブオイル、ハーブ、粒胡椒、山椒、塩（正式な表示を入れます）")]),
    dict(id="miso", name="ビワマスとみそ", en="BIWAMASU MISO", cat="frozen", tag="frozen", sub="1パック115g", price=1512, img="miso.jpg",
         summary="びわマスのあらを、3年熟成の自家製黒豆味噌で煮込みました。",
         desc="びわマスのあら（頭、骨、皮、身少々）を圧力鍋で丁寧にやわらかくなるまで煮込み、自家製黒豆味噌（3年熟成）と酒、砂糖で調味しました。味噌に使う黒豆も麹に使うお米も、そふぁらが自然農法で育てています。",
         spec=[("内容量", "1パック 115g"), ("保存方法", "冷凍で保存してください"), ("原材料", "ビワマス、黒豆味噌、酒、砂糖（正式な表示を入れます）")]),
    dict(id="koayu", name="山椒とこあゆ", en="SANSYO KOAYU", cat="frozen", tag="frozen", sub="子持ちアユ3匹／雄アユ4匹", price=1242, img="koayu.jpg",
         summary="ごはんに合う、山椒のきいた小鮎の甘露煮です。",
         desc="鮎は子持ちアユで、さとう・醤油・酒に山椒粒を加え、ごはんに合う味に仕上げています。",
         options=["子持ちアユ3匹", "雄アユ4匹"],
         spec=[("内容量", "子持ちアユ3匹／雄アユ4匹"), ("保存方法", "冷凍で保存してください"), ("原材料", "アユ、砂糖、醤油、酒、山椒（正式な表示を入れます）")]),
    dict(id="yuzu", name="ゆずマーマレード", en="MARMALADE YUZU", cat="frozen", tag="frozen", sub="1個", price=756, img="yuzu.jpg",
         summary="そふぁらのゆずマーマレードです。",
         desc="商品の説明文は、そふぁら様にうかがって入れます。",
         spec=[("内容量", "1個（容量を入れます）"), ("保存方法", "冷凍で保存してください"), ("原材料", "（正式な表示を入れます）")]),
    dict(id="shokupan", name="食パン（冷凍）", en="SHOKUPAN", cat="bread", tag="bread", sub="1.5斤のハーフ", price=378, img="shokupan.jpg",
         summary="外はパリッと、中はふんわり、もっちり、しっとり。",
         desc="国産小麦（北海道産）100%、トランス脂肪酸を含まない有機ショートニングを使用。オーブンは遠赤外線輻射窯で、備長炭に匹敵する焼き上がりが特徴です。外側パリッと中身は、ふんわり、もっちり、しっとり。",
         spec=[("内容量", "1.5斤のハーフ"), ("保存方法", "冷凍で保存してください"), ("原材料", "小麦粉（北海道産）ほか（正式な表示を入れます）")]),
    dict(id="halfhalf", name="食パン ハーフ＆ハーフ（冷凍）", en="HALF & HALF", cat="bread", tag="bread", sub="1.5斤のハーフ", price=399, img="halfhalf.jpg",
         summary="山ふたつで生地が違う、二度おいしい食パン。",
         desc="食パンの山二つの生地が違うハーフ＆ハーフは、黒豆きな粉、米粉、ライ麦全粒粉などから二種類を組み合わせて焼いています。",
         spec=[("内容量", "1.5斤のハーフ"), ("保存方法", "冷凍で保存してください"), ("原材料", "（正式な表示を入れます）")]),
    dict(id="baguette", name="スペルト小麦のバケット（冷凍）", en="SPELT BAGUETTE", cat="bread", tag="bread", sub="1本", price=486, img="baguette.jpg",
         summary="古代小麦・スペルト小麦の全粒粉100%。油脂・砂糖は使っていません。",
         desc="スペルト小麦は、いま広く使われているパン用小麦（普通小麦）の原種にあたる古代穀物です。滋賀県長浜市産、自然栽培のスペルト小麦全粒粉を100%使用し、油脂・砂糖は使っていません。栄養価が高く、香り豊かで、噛めば噛むほど味わい深いパンが焼きあがりました。",
         spec=[("内容量", "1本"), ("保存方法", "冷凍で保存してください"), ("原材料", "スペルト小麦全粒粉（長浜市産）ほか（正式な表示を入れます）")]),
    dict(id="koshihikari", name="コシヒカリ（無農薬）", en="KOSHIHIKARI", cat="rice", tag="normal", sub="5kg", price=None, img="koshihikari.png",
         summary="香りがよく、ツヤやかな炊きあがり。冷めてもおいしいお米です。",
         desc="ひかえめな粘りで上品な味わいが魅力のコシヒカリは、米本来の旨味を楽しんでいただける人気の品種です。冷めてもおいしく、その豊かな風味はおにぎりにすると一層際立ちます。",
         spec=[("内容量", "5kg（量と価格を入れます）"), ("栽培", "無農薬・れんげ緑肥"), ("産地", "滋賀県長浜市")]),
    dict(id="kiramizuki", name="きらみずき（無農薬）", en="KIRAMIZUKI", cat="rice", tag="normal", sub="5kg", price=None, img="kiramizuki.png",
         summary="自然な甘みがスーッと広がり、後味さわやか。",
         desc="そふぁらの風土を感じる、清らかで凛とした味わい。粒が大きく噛みごたえがあり、炊きあがりのツヤが食欲をそそります。粘りは控えめで、さっぱりとした口当たりが料理の味を引き立てます。",
         spec=[("内容量", "5kg（量と価格を入れます）"), ("栽培", "無農薬・れんげ緑肥"), ("産地", "滋賀県長浜市")]),
    dict(id="mochigome", name="滋賀羽二重糯（もち米）", en="HABUTAE MOCHI", cat="rice", tag="normal", sub="1kg", price=None, img="mochigome.png",
         summary="“幻のもち米”を、除草剤や農薬を使わずに育てました。",
         desc="収穫量が少なく“幻のもち米”とも言われる滋賀羽二重糯を、除草剤や農薬を使わず育てました。お餅にするとのびが良く、甘みと旨みがはっきりわかります。",
         spec=[("内容量", "1kg（量と価格を入れます）"), ("栽培", "無農薬"), ("産地", "滋賀県長浜市")]),
    dict(id="okowa", name="黒豆おこわ", en="KUROMAME OKOWA", cat="rice", tag="normal", sub="300g", price=1188, img="okowa.jpg",
         summary="自然農法で育てたお米と黒豆のおこわです。",
         desc="伊吹山から流れ出る雪どけ水と、5月の大地を真っ赤に染めるれんげを使い、農薬や化学肥料を使わない自然農法を17年。土が変わり、ようやく本来の姿に戻った大地で育ったお米と黒豆です。",
         spec=[("内容量", "300g"), ("保存方法", "常温（直射日光・高温多湿を避けて）"), ("産地", "滋賀県長浜市")]),
    dict(id="genmai", name="乾煎玄米", en="KANSEN GENMAI", cat="rice", tag="normal", sub="300g", price=1188, img="genmai.jpg",
         summary="いつもの白米に混ぜるだけ。玄米の栄養を手軽に。",
         desc="伊吹山の雪解け水と春に花咲くれんげで育てた、大自然を吸収した伸びやかな味と香り。いつもの白米に混ぜるだけで、玄米の栄養素を手軽にとることができます。",
         spec=[("内容量", "300g"), ("保存方法", "常温（直射日光・高温多湿を避けて）"), ("産地", "滋賀県長浜市")]),
    dict(id="kuromame", name="煎黒豆（黒豆茶）", en="IRI KUROMAME", cat="rice", tag="normal", sub="240g", price=1188, img="kuromame.jpg",
         summary="じっくり煎った黒豆。香ばしい黒豆茶で、ほっと一息。",
         desc="除草剤や農薬を使わず育てた黒豆を、じっくり煎りました。煮出すと黒豆の香ばしいかおりが広がる、ほんのり甘く口あたりもなめらかなお茶です。煮出した後の黒豆も、もちろんお召し上がりいただけます。",
         spec=[("内容量", "240g"), ("保存方法", "常温（直射日光・高温多湿を避けて）"), ("産地", "滋賀県長浜市")]),
]
BY_ID = {p["id"]: p for p in PRODUCTS}

NAV = [
    ("index.html#story", "そふぁらについて"),
    ("shop.html", "オンラインショップ"),
    ("shop.html#frozen", "冷凍食品"),
    ("index.html#bread", "そふぁらパン"),
    ("news.html", "お知らせ"),
    ("index.html#access", "アクセス"),
]


def esc(s):
    return html.escape(s, quote=True)


def yen(n):
    return f"{n:,}円"


def price_html(p, cls="price"):
    if p["price"] is None:
        return f'<span class="{cls} price--tbd">価格を準備中</span>'
    return f'<span class="{cls}">{yen(p["price"])}</span>'


def tag_html(key):
    cls, label = TAGS[key]
    return f'<span class="tag {cls}">{label}</span>'


def add_button(p):
    if p["price"] is None:
        return f'<button class="add-btn" type="button" disabled aria-label="{esc(p["name"])}は価格を準備中です">{ICON["cart"]}</button>'
    return f'<button class="add-btn" type="button" data-add="{p["id"]}" aria-label="{esc(p["name"])}をカートに入れる">{ICON["cart"]}</button>'


def card(p, pre=""):
    return f"""<article class="card">
  <a class="card-media" href="{pre}items/{p['id']}.html" tabindex="-1" aria-hidden="true"><img src="{pre}assets/img/{p['img']}" alt="" loading="lazy"></a>
  <div class="card-body">
    {tag_html(p['tag'])}
    <h3 class="card-name"><a href="{pre}items/{p['id']}.html">{esc(p['name'])}</a></h3>
    <p class="card-sub">{esc(p['sub'])}</p>
    <div class="card-foot">{price_html(p)}{add_button(p)}</div>
  </div>
</article>"""


def f_row(p, pre=""):
    return f"""<li class="f-row">
  <a href="{pre}items/{p['id']}.html" tabindex="-1" aria-hidden="true"><img src="{pre}assets/img/{p['img']}" alt="" loading="lazy"></a>
  <div>
    <h3 class="card-name"><a href="{pre}items/{p['id']}.html">{esc(p['name'])}</a></h3>
    <p class="card-sub">{esc(p['sub'])}</p>
    {price_html(p)}
  </div>
  {add_button(p)}
</li>"""


def layout(title, body, pre="", current="", description="そふぁら（滋賀県長浜市）のお米・パン・冷凍食品。サイトリニューアルのデザイン試作です。"):
    nav = "".join(
        f'<a href="{pre}{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>' for href, label in NAV
    )
    menu = "".join(f'<li><a href="{pre}{href}">{label}{ICON["arrow"]}</a></li>' for href, label in NAV)
    full_title = f"{title}｜そふぁら（サイト試作）" if title else "そふぁら｜田んぼから、元気と笑顔と健康を（サイト試作）"
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{SITE_URL}assets/img/hero.jpg">
<meta name="theme-color" content="#f7f1e5">
<link rel="icon" href="{pre}assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/style.css">
</head>
<body>
<div class="proto-bar">これは、NOTICがそふぁら様向けに作ったサイトの試作です。実際のご購入はできません。<a href="{pre}proposal.html">ご提案のポイントを見る</a></div>
<header class="site-header">
  <div class="container">
    <a class="brand" href="{pre}index.html"><img src="{pre}assets/img/logo.png" alt=""><span><span class="brand-name">そふぁら</span><span class="brand-sub">お米・パン・冷凍食品｜滋賀 長浜</span></span></a>
    <nav class="gnav" aria-label="メインメニュー">{nav}</nav>
    <div class="header-actions">
      <button class="icon-btn" type="button" data-open="cart" aria-label="カートを見る">{ICON['cart']}<span class="badge" data-count="0">0</span></button>
      <button class="icon-btn menu-btn" type="button" data-open="menu" aria-label="メニューを開く">{ICON['menu']}</button>
      <a class="btn btn--primary header-shop" href="{pre}shop.html">ショップへ</a>
    </div>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div style="display:grid;gap:18px">
      <div class="footer-brand"><span class="footer-logo"><img src="{pre}assets/img/logo.png" alt=""></span><span><b>そふぁら（農業生産・販売）</b><span>〒526-0234 滋賀県長浜市相撲庭町861-2<br>TEL 080-4495-3345</span></span></div>
      <div class="sns"><a href="https://www.instagram.com/sofaratei/" aria-label="Instagram">{ICON['insta']}</a><a href="https://www.facebook.com/" aria-label="Facebook">{ICON['fb']}</a></div>
    </div>
    <nav class="footer-links" aria-label="サイトマップ">{"".join(f'<a href="{pre}{h}">{l}</a>' for h, l in [("index.html", "ホーム")] + NAV)}</nav>
    <div style="display:grid;gap:14px;align-content:start">
      <div class="footer-legal"><a href="{pre}legal.html">特定商取引法に基づく表記</a><a href="{pre}legal.html#privacy">プライバシーポリシー</a><a href="{pre}index.html#access">お問い合わせ</a></div>
      <p class="copy">© そふぁら sofara natural　／　サイト試作：NOTIC</p>
    </div>
  </div>
</footer>

<div class="overlay" data-close></div>
<aside class="drawer" id="menu" aria-label="メニュー" aria-hidden="true">
  <div class="drawer-head"><b>メニュー</b><button class="icon-btn" type="button" data-close aria-label="閉じる">{ICON['close']}</button></div>
  <div class="drawer-body">
    <ul class="menu-list"><li><a href="{pre}index.html">ホーム{ICON['arrow']}</a></li>{menu}</ul>
    <div class="menu-info"><b>パン小屋「そふぁらてい」</b><br>毎週 土・日　10:00〜13:00<br>TEL 080-4495-3345</div>
  </div>
</aside>
<aside class="drawer" id="cart" aria-label="カート" aria-hidden="true">
  <div class="drawer-head"><b>カート</b><button class="icon-btn" type="button" data-close aria-label="閉じる">{ICON['close']}</button></div>
  <div class="drawer-body"><ul class="cart-items" data-cart-items></ul></div>
  <div class="drawer-foot">
    <div class="cart-total"><span>合計（税込）</span><span class="price" data-cart-total>0円</span></div>
    <p class="note">冷凍食品と冷凍パンはクール便、お米・豆・お茶は常温便でお届けします。送料はご注文画面で表示します。</p>
    <button class="btn btn--primary btn--block" type="button" aria-disabled="true">ご購入手続きへ（試作のため進めません）</button>
  </div>
</aside>
<div class="toast" role="status" aria-live="polite" data-toast></div>
<script src="{pre}assets/js/products.js"></script>
<script src="{pre}assets/js/app.js"></script>
</body>
</html>
"""


def sec_title(en, jp, left=False):
    return f'<div class="sec-title{" sec-title--left" if left else ""}">{DOTS}<span class="eyebrow">{en}</span><h2>{jp}</h2></div>'


def index_page():
    p = BY_ID
    popular = "".join(card(p[i]) for i in ["koji", "koayu", "okowa", "baguette"])
    frozen_rows = "".join(f_row(p[i]) for i in ["koji", "oiled", "miso", "koayu", "yuzu"])
    rice = [("koshihikari", "koshihikari.png", "コシヒカリ", "香りよく、冷めてもおいしい"),
            ("kiramizuki", "kiramizuki.png", "きらみずき", "自然な甘みで後味さわやか"),
            (None, "kiramizuki.png", "にじのきらめき", "もちもち食感と強い甘み"),
            ("mochigome", "mochigome.png", "滋賀羽二重糯", "“幻のもち米”。お餅にぜひ")]
    rice_html = "".join(
        f'<a class="rice-card" href="{"items/" + rid + ".html" if rid else "shop.html#rice"}"><img src="assets/img/{img}" alt="" loading="lazy"><div><span class="card-name">{name}</span><span class="card-sub">{d}</span><span class="from">価格を準備中</span></div></a>'
        for rid, img, name, d in rice)
    breads = [("b_komeko.png", "米粉パン"), ("b_kinako.png", "きな粉パン"), ("b_shokupan.png", "食パン"), ("b_coffee.png", "コーヒーパン"), ("b_danish.png", "デニッシュ"), ("b_chiffon.png", "シィフォン")]
    bread_html = "".join(f'<li><img src="assets/img/{img}" alt="" loading="lazy">{name}</li>' for img, name in breads)
    cats = [("shop.html#rice", "koshihikari.png", "--r-yellow", "お米・豆・お茶", "無農薬のコシヒカリやきらみずき、黒豆おこわ、煎黒豆など。"),
            ("index.html#bread", "b_shokupan.png", "--r-magenta", "そふぁらパン", "米粉や自家製きな粉のパン。冷凍の食パン・バケットもお届け。"),
            ("shop.html#frozen", "koji.jpg", "--r-cyan", "冷凍食品", "ビワマスと麹、山椒とこあゆなど。クール便でお届けします。")]
    cat_html = "".join(
        f'<a class="cat-card" href="{href}" style="--ring:var({ring})"><span class="cat-media"><img src="assets/img/{img}" alt="" loading="lazy"></span><span class="cat-body"><span class="cat-name">{name}{ICON["arrow"]}</span><span class="cat-desc">{d}</span></span></a>'
        for href, img, ring, name, d in cats)
    body = f"""
<section class="hero">
  <div class="container">
    <div class="hero-visual">
      <img src="assets/img/hero.jpg" alt="水を張った田んぼで田植えをする筧さん" width="600" height="330">
      <span class="hero-badge"><img src="assets/img/logo.png" alt="そふぁら"></span>
    </div>
    <div class="hero-copy">
      <p class="kicker">{DOTS}滋賀県長浜市・伊吹山のふもとから</p>
      <h1>田んぼから、<br>元気と笑顔と健康を<br>とどけたい。</h1>
      <p class="lead">無農薬・れんげ緑肥で育てたお米と、土日だけ開くパン小屋。そふぁらの恵みを、このサイトからそのままお取り寄せいただけます。</p>
      <div class="btn-row">
        <a class="btn btn--primary btn--block" href="shop.html">オンラインショップへ{ICON['arrow']}</a>
        <a class="btn btn--secondary btn--block" href="shop.html#frozen">冷凍食品を見る{ICON['arrow']}</a>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="営業日とお知らせ">
  <div class="container">
    <div class="info-card">
      <div style="display:grid;gap:8px">
        <p class="info-hours-label">{ICON['clock']}パン小屋「そふぁらてい」の営業日</p>
        <p class="info-hours">毎週 土・日　10:00〜13:00</p>
        <p class="note">焼きたてパンは店頭のみ。冷凍の食パン・バケットは、オンラインショップでも買えます。</p>
      </div>
      <hr class="info-divider">
      <div style="display:grid;gap:10px">
        <div class="news-head">お知らせ<a class="link-more" href="news.html">一覧へ{ICON['arrow']}</a></div>
        <ul class="news-list">
          <li class="news-item"><span class="news-meta">2026.02.07 {tag_html('new')}</span><p>びわマスライスバーガー、そふぁらていで販売開始！</p></li>
          <li class="news-item news-item--muted"><span class="news-meta">お知らせの例</span><p>臨時休業や新米のご案内も、スマホからすぐに更新できます。</p></li>
        </ul>
      </div>
      <a class="link-more info-more" href="news.html">お知らせ一覧{ICON['arrow']}</a>
    </div>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="container">
    {sec_title('ONLINE SHOP', 'お買いものはこちら')}
    <div class="cat-list">{cat_html}</div>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="container">
    <div class="rail-head">
      <div><span class="eyebrow">PICK UP</span><h2 class="h2">人気の商品</h2></div>
      <a class="link-more" href="shop.html">すべて見る{ICON['arrow']}</a>
    </div>
    <div class="rail">{popular}</div>
    <p class="note" style="margin-top:8px">※表示価格はすべて税込です</p>
  </div>
</section>

<div id="frozen-sec">{WAVE_TOP}
<section class="section section--mint" style="padding-top:20px">
  <div class="container frozen-grid">
    <div class="frozen-copy">
      {sec_title('FROZEN FOOD', '安全と安心、<br>そふぁらの冷凍食品', left=False)}
      <p class="lead fz-lead" style="color:var(--ink)">自然農法で育てたお米の麹や、3年熟成の自家製黒豆味噌。琵琶湖のビワマスや子持ちアユを、手間をかけて仕上げました。ご注文いただいた商品は、クール便でお届けします。</p>
      <p class="cool-note">{ICON['truck']}冷凍食品と冷凍パンは、同じクール便でまとめてお届けします。</p>
      <a class="btn btn--secondary btn--block fz-btn" href="shop.html#frozen">冷凍食品をすべて見る{ICON['arrow']}</a>
    </div>
    <ul class="frozen-list">{frozen_rows}</ul>
  </div>
</section>
{WAVE_BOTTOM}</div>

<section class="section" id="story">
  <div class="container">
    <div class="story-grid">
      <div class="collage" aria-hidden="true">
        <img class="c1" src="assets/img/renge.jpg" alt="" loading="lazy">
        <img class="c2" src="assets/img/anegawa.jpg" alt="" loading="lazy">
        <img class="c3" src="assets/img/ibuki.jpg" alt="" loading="lazy">
        <span class="cap cap1">春、田んぼ一面のれんげ</span>
        <span class="cap cap2">伊吹山の雪どけ水が流れる姉川</span>
      </div>
      <div class="story-copy" style="display:grid;gap:22px">
        {sec_title('OUR STORY', '無農薬、だから<br>本物の味がする。')}
        <p>伊吹山の清らかな雪どけ水が流れ込む姉川のほとりで、2007年からすべての稲を無農薬で育てています。春に咲くれんげが田んぼの栄養になり、虫やカエルの声を聴きながら育ったお米は、味わいが濃く、旨味がまるで違います。</p>
        <figure class="voice" style="margin:0">
          <blockquote>「誰もが安心して食べられる米づくりで、たくさんの人に元気と笑顔と健康を。それが、そふぁらの想いです。」<cite>そふぁら　筧 太津郎</cite></blockquote>
          <img src="assets/img/tatsuro.png" alt="お米の袋を抱える筧 太津郎さん" loading="lazy">
        </figure>
      </div>
    </div>
    <div style="display:grid;gap:16px;margin-top:40px">
      <div class="rail-head" style="margin-bottom:0"><h3 class="h3">そふぁらのお米</h3><a class="link-more" href="shop.html#rice">お米・豆・お茶を見る{ICON['arrow']}</a></div>
      <div class="rice-grid">{rice_html}</div>
    </div>
  </div>
</section>

<section class="section section--kraft" id="bread">
  <div class="container bread-grid-wrap">
    <div class="bread-left">
      <div class="bread-head"><span class="eyebrow">SOFARA BREAD</span><img src="assets/img/panlogo.jpg" alt="そふぁらパン"><p>ほおばると、素材の甘みが口いっぱいに広がる</p></div>
      <figure class="voice voice--plain bread-voice" style="margin:0">
        <blockquote>パン生地には、国産の小麦や自家製粉したそふぁらの米粉を。1日に焼き上げるのは7〜8種類。土日だけの小さなパン小屋ですが、お近くまでお越しの際は、ぜひお寄りくださいね。<cite>そふぁら　筧 茂代</cite></blockquote>
        <img src="assets/img/shigeyo.png" alt="パンを持つ筧 茂代さん" loading="lazy" style="width:100px">
      </figure>
      <a class="btn btn--primary btn--block bread-btn" href="shop.html#frozen">冷凍パンをオンラインで買う{ICON['arrow']}</a>
    </div>
    <div class="bread-right">
      <img class="bread-photo" src="assets/img/bread.png" alt="焼きたてのパンが並ぶかご" loading="lazy">
      <ul class="bread-items">{bread_html}</ul>
    </div>
  </div>
</section>

<section class="section" id="access">
  <div class="container access-grid">
    <iframe class="map" title="そふぁらていの地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=%E6%BB%8B%E8%B3%80%E7%9C%8C%E9%95%B7%E6%B5%9C%E5%B8%82%E7%9B%B8%E6%92%B2%E5%BA%AD%E7%94%BA861-2&amp;output=embed"></iframe>
    <div class="access-copy" style="display:grid;gap:22px">
      {sec_title('ACCESS', 'そふぁらていへの<br>アクセス')}
      <ul class="info-rows">
        <li>{ICON['pin']}<b>住所</b><span>〒526-0234<br>滋賀県長浜市相撲庭町861-2</span></li>
        <li>{ICON['clock']}<b>営業日</b><span>土・日のみ　10:00〜13:00</span></li>
        <li>{ICON['car']}<b>駐車場</b><span>あり</span></li>
        <li>{ICON['phone']}<b>電話</b><span>080-4495-3345</span></li>
      </ul>
      <div class="btn-row">
        <a class="btn btn--primary btn--block" href="tel:08044953345">電話する{ICON['arrow']}</a>
        <a class="btn btn--secondary btn--block" href="https://www.google.com/maps/search/?api=1&amp;query=%E6%BB%8B%E8%B3%80%E7%9C%8C%E9%95%B7%E6%B5%9C%E5%B8%82%E7%9B%B8%E6%92%B2%E5%BA%AD%E7%94%BA861-2" target="_blank" rel="noopener">地図アプリで開く{ICON['arrow']}</a>
      </div>
    </div>
  </div>
</section>
"""
    return layout("", body, current="index.html")


def shop_page():
    frozen = [p for p in PRODUCTS if p["cat"] in ("frozen", "bread")]
    rice = [p for p in PRODUCTS if p["cat"] == "rice"]
    body = f"""
<div class="container">
  <p class="crumb"><a href="index.html">ホーム</a> ＞ オンラインショップ</p>
  <div class="page-head">
    <span class="eyebrow">ONLINE SHOP</span>
    <h1>オンラインショップ</h1>
    <p class="lead">そふぁらのお米・パン・冷凍食品を、ご自宅へお届けします。</p>
    <div class="chips" role="group" aria-label="商品の種類で絞り込む">
      <button class="chip" type="button" data-filter="all" aria-pressed="true">すべて</button>
      <button class="chip" type="button" data-filter="frozen" aria-pressed="false">冷凍食品</button>
      <button class="chip" type="button" data-filter="bread" aria-pressed="false">冷凍パン</button>
      <button class="chip" type="button" data-filter="rice" aria-pressed="false">お米・豆・お茶</button>
    </div>
  </div>
</div>
<section class="group section--mint" id="frozen" data-group="frozen bread">
  <div class="container">
    <div class="group-head">{ICON['snow']}<h2 class="h3">冷凍食品</h2><small>クール便でお届け・{len(frozen)}商品</small></div>
    <p class="cool-note">{ICON['truck']}冷凍食品と冷凍パンは、同じクール便でまとめてお届けします。</p>
    <div class="product-grid">{"".join(f'<div data-cat="{p["cat"]}">' + card(p) + '</div>' for p in frozen)}</div>
  </div>
</section>
<section class="group" id="rice" data-group="rice">
  <div class="container">
    <div class="group-head"><h2 class="h3">お米・豆・お茶</h2><small>常温でお届け・{len(rice)}商品</small></div>
    <div class="product-grid">{"".join(f'<div data-cat="{p["cat"]}">' + card(p) + '</div>' for p in rice)}</div>
  </div>
</section>
<div class="container" style="padding-bottom:40px"><p class="note">※表示価格はすべて税込です。「価格を準備中」の商品は、価格が決まりしだい表示します。</p></div>
"""
    return layout("オンラインショップ", body, current="shop.html")


def item_page(p):
    pre = "../"
    cat_label, cat_href = ("お米・豆・お茶", "shop.html#rice") if p["cat"] == "rice" else ("冷凍食品", "shop.html#frozen")
    is_cool = p["cat"] != "rice"
    options = ""
    if p.get("options"):
        options = '<div class="options" role="radiogroup" aria-label="種類">' + "".join(
            f'<label><input type="radio" name="opt" value="{esc(o)}"{" checked" if i == 0 else ""}><span>{esc(o)}</span></label>'
            for i, o in enumerate(p["options"])) + "</div>"
    if p["price"] is None:
        buy = '<button class="btn btn--primary" type="button" disabled>価格を準備中</button>'
    else:
        buy = f'<button class="btn btn--primary" type="button" data-add="{p["id"]}" data-qty-from="qty">{ICON["cart"]}カートに入れる</button>'
    delivery = [("truck", "クール便（冷凍）でお届けします" if is_cool else "常温便でお届けします"),
                ("snow" if is_cool else "clock", "冷凍食品と冷凍パンは、同じ箱にまとめて送れます" if is_cool else "精米してからお届けします（予定）"),
                ("clock", "ご注文から ◯営業日以内に発送（日数を入れます）")]
    spec = p["spec"] + [("お届け", "クール便（冷凍）" if is_cool else "常温便"), ("製造・販売", "そふぁら（滋賀県長浜市）")]
    spec_rows = "".join(
        f'<tr><th scope="row">{esc(k)}</th><td{" class=\"placeholder\"" if "入れます" in v else ""}>{esc(v)}</td></tr>' for k, v in spec)
    related_ids = [x["id"] for x in PRODUCTS if x["cat"] == p["cat"] and x["id"] != p["id"]][:3]
    if len(related_ids) < 3:
        related_ids += [x["id"] for x in PRODUCTS if x["id"] not in related_ids and x["id"] != p["id"]][: 3 - len(related_ids)]
    related = "".join(card(BY_ID[i], pre) for i in related_ids)
    desc_cls = ' class="placeholder"' if "うかがって" in p["desc"] else ""
    price_line = (f'<div class="pd-price"><span class="price">{yen(p["price"])}</span><span>（税込）／{esc(p["sub"])}</span></div>'
                  if p["price"] is not None else f'<div class="pd-price"><span class="price price--tbd">価格を準備中</span><span>{esc(p["sub"])}</span></div>')
    body = f"""
<div class="container">
  <p class="crumb"><a href="{pre}index.html">ホーム</a> ＞ <a href="{pre}{cat_href}">{cat_label}</a> ＞ {esc(p['name'])}</p>
  <div class="pd-grid">
    <div class="pd-media"><img src="{pre}assets/img/{p['img']}" alt="{esc(p['name'])}"></div>
    <div class="pd-info">
      <div class="pd-tags">{tag_html(p['tag'])}<span class="eyebrow">{esc(p['en'])}</span></div>
      <h1>{esc(p['name'])}</h1>
      <p class="lead">{esc(p['summary'])}</p>
      {price_line}
      {options}
      <div class="buy-row">
        <div class="qty"><button type="button" data-qty="-1" aria-label="1つ減らす">{ICON['minus']}</button><output id="qty" aria-live="polite">1</output><button type="button" data-qty="1" aria-label="1つ増やす">{ICON['plus']}</button></div>
        {buy}
      </div>
      <ul class="delivery">{"".join(f'<li>{ICON[i]}{esc(t)}</li>' for i, t in delivery)}</ul>
    </div>
  </div>
</div>
<section class="section section--white" style="padding:32px 0">
  <div class="container" style="display:grid;gap:16px;max-width:820px">
    <h2 class="h3">こんな商品です</h2>
    <p{desc_cls}>{esc(p['desc'])}</p>
    <table class="spec"><tbody>{spec_rows}</tbody></table>
  </div>
</section>
<section class="section" style="padding:32px 0 48px">
  <div class="container">
    <div class="rail-head"><h2 class="h3">一緒にいかがですか</h2><a class="link-more" href="{pre}shop.html">ショップへ{ICON['arrow']}</a></div>
    <div class="rail">{related}</div>
  </div>
</section>
"""
    return layout(p["name"], body, pre=pre, description=f"{p['name']}｜{p['summary']}")


def proposal_page():
    points = [
        ("1", "var(--r-cyan)", "冷凍食品が、その場で買える",
         "冷凍食品のページに購入ボタンがなく、ネットショップの冷凍食品にも商品が入っていない",
         "商品ページから、そのままカートへ。冷凍食品と冷凍パンは、クール便でまとめてお届け",
         '<a href="shop.html#frozen">オンラインショップ</a>・<a href="items/koji.html">商品ページ</a>で見る'),
        ("2", "var(--r-magenta)", "ホームページとお店を、ひとつに",
         "ホームページ、ネットショップ、冷凍食品のページが別々の場所にあり、行き来しづらい",
         "そふぁらの想い → 商品 → ご購入までが、ひとつのサイトでつながる",
         '<a href="index.html">トップページ</a>で見る'),
        ("3", "var(--r-yellow)", "営業日とお知らせが、ひと目で分かる",
         "パン小屋の営業日や、新商品・臨時休業のお知らせを探しにくい",
         "トップに営業日とお知らせ。臨時休業や新米の案内も、スマホから更新できる",
         '<a href="index.html">トップページ</a>（営業日・お知らせ）で見る'),
        ("4", "var(--r-green)", "QRの行き先が、ひとつに決まる",
         "QRを載せても、どこに案内すればいいかが決まらない",
         "パンの袋や冷凍食品に可変QRを1つ。行き先はこのサイトの好きなページへ、あとから変えられる",
         "可変QR × このサイト"),
    ]
    pts = "".join(f"""<article class="point">
  <div class="point-head"><span class="point-no" style="background:{c}{';color:var(--ink)' if n == '3' else ''}">{n}</span><h2>{t}</h2></div>
  <p class="ba ba--before"><b>いま</b>{b}</p>
  <p class="ba ba--after"><b>これから</b>{a}</p>
  <p class="note">{ref}</p>
</article>""" for n, c, t, b, a, ref in points)
    asks = ["パン小屋の営業時間（10:00〜13:00 と 10時〜12時の、どちらが正しいか）",
            "サイトに載せる電話番号・メールアドレス（お米用・パン用を分けるか）",
            "お米の量と価格（コシヒカリ・きらみずき・にじのきらめき・もち米）",
            "冷凍食品の発送日数・送料、冷凍食品と冷凍パンを同じ箱で送れるか",
            "各商品の原材料・内容量の正式な表示",
            "今も扱っている商品（酵素ジュース、野草・野菜、加工品、ギフトなど）",
            "今のホームページ・ネットショップを作った方と、今の更新・管理の状況",
            "冷凍食品ページの写真と文章（ADBENTOBOY 様の制作）を、新しいサイトで使ってよいか"]
    body = f"""
<section class="section section--kraft">
  <div class="container" style="display:grid;gap:32px">
    <div class="proposal-hero"><span class="footer-logo"><img src="assets/img/logo.png" alt=""></span><div><span class="eyebrow">SITE RENEWAL PROTOTYPE</span><h1 class="h2">そふぁら様　サイトリニューアルのご提案</h1></div></div>
    <p>今のホームページ・ネットショップ・冷凍食品ページの雰囲気（虹色のロゴ、クラフト紙、ミントグリーン、丸みのある文字）はそのままに、ひとつのサイトにまとめた試作です。スマホでもパソコンでも見やすいように作っています。</p>
    <div class="points">{pts}</div>
    <div class="btn-row"><a class="btn btn--primary btn--block" href="index.html">試作のサイトを見る{ICON['arrow']}</a><a class="btn btn--secondary btn--block" href="shop.html">オンラインショップを見る{ICON['arrow']}</a></div>
  </div>
</section>
<section class="section">
  <div class="container" style="display:grid;gap:18px;max-width:820px">
    <h2 class="h2">ご確認いただきたいこと</h2>
    <p class="lead">試作では、次の点を仮で入れています。わかる範囲で教えていただければ、本番のサイトに反映します。</p>
    <ul class="checklist">{"".join(f'<li>{esc(a)}</li>' for a in asks)}</ul>
  </div>
</section>
"""
    return layout("ご提案のポイント", body, current="proposal.html")


def news_page():
    body = f"""
<div class="container" style="padding-bottom:56px">
  <p class="crumb"><a href="index.html">ホーム</a> ＞ お知らせ</p>
  <div class="page-head"><span class="eyebrow">NEWS</span><h1>お知らせ</h1></div>
  <ul class="news-list info-card" style="display:grid">
    <li class="news-item"><span class="news-meta">2026.02.07 {tag_html('new')}</span><p>びわマスライスバーガー、そふぁらていで販売開始！琵琶湖の宝石・びわマスと、そふぁらのお米「きらみずき」でつくりました。</p></li>
    <li class="news-item news-item--muted"><span class="news-meta">お知らせの例</span><p>臨時休業、新米の予約、イベント出店などを、スマホからかんたんに載せられるようにします。</p></li>
  </ul>
</div>
"""
    return layout("お知らせ", body, current="news.html")


def legal_page():
    rows = [("販売事業者", "そふぁら（正式な名称を入れます）"), ("運営責任者", "筧 太津郎"), ("所在地", "〒526-0234 滋賀県長浜市相撲庭町861-2"),
            ("電話番号", "080-4495-3345"), ("メールアドレス", "（入れます）"), ("販売価格", "各商品ページに税込で表示"),
            ("送料", "（入れます）"), ("お支払い方法", "（入れます）"), ("お届け時期", "ご注文から ◯営業日以内に発送（入れます）"),
            ("返品・交換", "食品のため、お客様都合の返品はお受けできません（内容を確認して入れます）")]
    tr = "".join(f'<tr><th scope="row">{k}</th><td{" class=\"placeholder\"" if "入れます" in v else ""}>{v}</td></tr>' for k, v in rows)
    body = f"""
<div class="container" style="padding-bottom:56px;max-width:860px">
  <p class="crumb"><a href="index.html">ホーム</a> ＞ 特定商取引法に基づく表記</p>
  <div class="page-head"><h1 style="font-size:24px">特定商取引法に基づく表記</h1><p class="note">試作のため、一部は仮の内容です。</p></div>
  <table class="spec legal-table"><tbody>{tr}</tbody></table>
  <h2 class="h3" id="privacy" style="margin-top:40px">プライバシーポリシー</h2>
  <p class="placeholder" style="margin-top:10px">お預かりした個人情報は、商品のお届けとご連絡のためにだけ使います。（正式な文面を入れます）</p>
</div>
"""
    return layout("特定商取引法に基づく表記", body)


def main():
    (DOCS / "items").mkdir(parents=True, exist_ok=True)
    pages = {"index.html": index_page(), "shop.html": shop_page(), "proposal.html": proposal_page(),
             "news.html": news_page(), "legal.html": legal_page()}
    for p in PRODUCTS:
        pages[f"items/{p['id']}.html"] = item_page(p)
    for name, content in pages.items():
        (DOCS / name).write_text(content, encoding="utf-8")
    data = {p["id"]: {"name": p["name"], "price": p["price"], "img": p["img"], "cool": p["cat"] != "rice"} for p in PRODUCTS}
    (DOCS / "assets/js/products.js").write_text("window.PRODUCTS = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    (DOCS / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"wrote {len(pages)} pages")


if __name__ == "__main__":
    main()
