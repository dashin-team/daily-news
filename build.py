#!/usr/bin/env python3
"""Data-driven builder: reads data.json (+ img/cards/<id>.png, img/poster-*.png) -> index.html + date-named ZIP.

Page chrome is an electronic-paper reader: date bar, section list, large page,
thumbnail strip, per-page download, and the day's ZIP. Historical news-*-all.zip
files are kept and listed in the calendar.
"""
import json,os,zipfile,datetime,html as H,re
W=os.path.dirname(os.path.abspath(__file__)); d=json.load(open(f'{W}/data.json'))
SITE="南恩新聞報報"; DATE=d['date']; D8=DATE.replace('.','')
WD="日一二三四五六"[datetime.date(*map(int,DATE.split('.'))).isoweekday()%7]
idx=[[n,v,dd,p,"up" if str(dd)[:1]=="+" else "dn" if str(dd)[:1]=="-" else "fl"] for n,v,dd,p in d['idx']]
rates=json.load(open(f'{W}/data/rates.json'))
def chg(v,p):
    v,p=str(v),str(p)
    x=float(v)-float(p)
    n=max(len(v.split('.')[1]) if '.' in v else 0, len(p.split('.')[1]) if '.' in p else 0)
    x=0.0 if abs(x)<1e-12 else x
    return ("up" if x>0 else "dn" if x<0 else "fl"),(f"{x:+.{n}f}" if x else f"{0:.{n}f}"),(f"{x/float(p)*100:+.2f}%" if x else "0.00%")
fx=[]; fx_cards=[]
for c in rates['currencies']:
    quotes=f'<div class=qq><span>即期買入 {c["spot_buy"]}</span><span>即期賣出 {c["spot_sell"]}</span><span>現金買入 {c["cash_buy"]}</span><span>現金賣出 {c["cash_sell"]}</span></div>'
    if c.get('prev_spot_sell'):
        u,a,b=chg(c['spot_sell'],c['prev_spot_sell'])
        arrow='▲' if u=='up' else '▼' if u=='dn' else '－'
        fx.append([c['name'],c['code'],str(c['spot_sell']),u,a,b])
        fx_cards.append(f'<div class=q><div class=qn>{c["name"]} <small>{c["code"]}</small></div><div class=qv>{c["spot_sell"]}</div><div class="{u} qd">{arrow} {a}（{b}）</div>{quotes}</div>')
    else:
        fx_cards.append(f'<div class=q><div class=qn>{c["name"]} <small>{c["code"]}</small></div><div class=qv>{c["spot_sell"]}</div>{quotes}</div>')
fxh=''.join(fx_cards)
assert [c[1] for c in fx]==['USD','AUD','JPY','CNY'], fx
src_js=d['sources'] if str(d['sources']).startswith('臺灣銀行牌告匯率') else '臺灣銀行牌告匯率、'+d['sources']
footer_src='臺灣銀行牌告匯率（rate.bot.com.tw）、'+d['sources']
items=d['items']
for it in items:
    it['img']=f"img/cards/{it['id']}.png"; it['dl']=f"{D8}-剪報-{it['short'].split('　')[0]}.png".replace('/','-').replace('?','').replace('？','')
    assert os.path.exists(f"{W}/{it['img']}"),it['id']
top=sorted([i for i in items if i.get('top')],key=lambda i:i['top'])
assert len(top)==5, [i['id'] for i in top]
e=H.escape
ixh="".join(f'<div class=q><div class=qn>{n}</div><div class=qv>{v}</div><div class="{u} qd">{"▲" if u=="up" else "▼" if u=="dn" else "－"} {a}（{p}）</div></div>' for n,v,a,p,u in idx)
ZIP=f"news-{D8}-all.zip"
with zipfile.ZipFile(f'{W}/{ZIP}','w') as z:
    for f,n in d['posters']: z.write(f'{W}/img/{f}',f'{D8}-每日報報-{n}.png')
    for k,i in enumerate(items): z.write(f"{W}/{i['img']}",f"{k+1:02d}-{i['dl']}")
P0=d['posters'][0]
arcs=[]
for fn in sorted(os.listdir(W)):
    m=re.fullmatch(r'news-(\d{8})-all\.zip', fn)
    if not m: continue
    d8=m.group(1); dt=datetime.date(int(d8[:4]),int(d8[4:6]),int(d8[6:]))
    arcs.append({"d8":d8,"date":f"{dt:%Y.%m.%d}","wd":"日一二三四五六"[dt.isoweekday()%7],"file":fn})
js_data=json.dumps(dict(date=DATE,D8=D8,wd=WD,fx=fx,idx=idx,items=items,cats=d['cats'],posters=d['posters'],bg_auto=d.get('bg_auto','newsroom'),bg_pool=d.get('bg_pool',[]),fxnote=rates['poster_note'],idxnote=d['idx_note'],sources=src_js,asof=d['asof'],archives=arcs),ensure_ascii=False)
import hashlib,time
VER=hashlib.md5(open(f'{W}/app.js','rb').read()).hexdigest()[:8]+'-'+time.strftime('%m%d%H%M')
html=f"""<!doctype html><html lang=zh-Hant><head><meta charset=utf-8><meta http-equiv=Cache-Control content="no-cache, no-store, must-revalidate"><meta http-equiv=Pragma content=no-cache><meta http-equiv=Expires content=0>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>A1 要聞 | {DATE} | {SITE}</title>
<link rel=preconnect href=https://fonts.googleapis.com><link rel=preconnect href=https://fonts.gstatic.com crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@400;600;700&display=swap" rel=stylesheet>
<style>
*{{box-sizing:border-box}}
body{{--fT:'Noto Sans TC','Noto Sans CJK TC',sans-serif;--fH:'Noto Serif TC','Noto Serif CJK TC',serif;--fB:'Noto Serif TC','Noto Serif CJK TC',serif;--fS:'Noto Sans TC','Noto Sans CJK TC',sans-serif;--fN:'Inter';margin:0;background:#e9e9e9;color:#333;font-family:var(--fN),var(--fS);font-weight:500;font-variant-numeric:tabular-nums;-webkit-text-size-adjust:none}}
button,a{{font-family:inherit}}
.topbar{{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid #e4e4e4;height:60px}}
.topbar .inner{{max-width:1180px;margin:0 auto;height:100%;display:flex;align-items:center;gap:12px;padding:0 14px}}
.icon{{border:0;background:none;font-size:22px;line-height:1;padding:6px 8px;cursor:pointer;color:#222}}
.brand{{font-family:var(--fH);font-weight:700;font-size:26px;letter-spacing:2px;color:#1a1a1a;white-space:nowrap}}
.datebox{{margin-left:auto;position:relative;display:flex;align-items:center;color:#e60012;font-weight:700}}
.datebox>button{{border:0;background:none;color:#e60012;cursor:pointer;font-weight:700}}
#day-prev,#day-next{{font-size:22px;padding:4px 8px}}
#date-btn{{font-size:18px;letter-spacing:.5px;min-width:11em}}
.zipbtn{{border:1px solid #e60012;color:#e60012;text-decoration:none;font-weight:700;font-size:14px;padding:6px 12px;border-radius:2px;white-space:nowrap}}
.zipbtn:hover{{background:#e60012;color:#fff}}
.cal{{position:absolute;top:46px;right:0;width:280px;background:#fff;border:1px solid #ddd;box-shadow:0 10px 28px rgba(0,0,0,.14);padding:10px 12px 12px;z-index:50;color:#333;font-weight:500}}
.calhead{{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}}
.calhead b{{color:#222;font-size:16px}}
.calhead button{{border:0;background:#f3f3f3;width:32px;height:32px;cursor:pointer;font-size:18px}}
.wk,.days{{display:grid;grid-template-columns:repeat(7,1fr);text-align:center}}
.wk{{color:#888;font-size:12px;margin-bottom:4px}}
.days button,.days span{{height:34px}}
.days button{{border:0;background:#fff;cursor:pointer;font-size:14px}}
.days button.has{{color:#e60012;font-weight:700}}
.days button.on{{background:#e60012;color:#fff;border-radius:2px}}
.days button:disabled{{color:#ccc;cursor:default;font-weight:400}}
.shell{{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:272px minmax(0,1fr) 300px;background:#fff;min-height:calc(100vh - 60px)}}
.secnav{{border-right:1px solid #eee;background:#fafafa;overflow:auto;max-height:calc(100vh - 60px);position:sticky;top:60px}}
.sec{{display:flex;width:100%;gap:8px;align-items:baseline;text-align:left;border:0;border-bottom:1px solid #eee;background:transparent;padding:12px 14px;cursor:pointer;font-size:16px;color:#333}}
.sec b{{color:#e60012;font-family:var(--fN);min-width:2.2em}}
.sec.on{{background:#fff;box-shadow:inset 3px 0 0 #e60012;font-weight:700}}
.plist{{background:#fff}}
.prow{{display:flex;align-items:center;gap:6px;border-bottom:1px solid #f0f0f0;padding:0 8px 0 14px}}
.prow.on{{background:#fff5f5}}
.jump{{flex:1;text-align:left;border:0;background:none;padding:8px 0;cursor:pointer;font-size:14px;line-height:1.4;color:#222}}
.mini{{flex:none;font-size:12px;font-weight:700;color:#e60012;text-decoration:none;border:1px solid #e60012;padding:2px 6px;border-radius:2px}}
.hl{{display:block;text-decoration:none;color:#222;padding:8px 14px;border-bottom:1px solid #f0f0f0;font-size:14px;line-height:1.4}}
.hl small{{display:block;color:#888;font-size:12px;margin-top:2px}}
.stage{{background:#f3f3f3;min-width:0;display:flex;flex-direction:column}}
.viewer{{position:relative;display:flex;align-items:center;justify-content:center;background:#ececec;min-height:280px;padding:12px 48px}}
.viewer img{{max-width:100%;max-height:min(74vh,860px);width:auto;height:auto;object-fit:contain;display:block;background:#fff;box-shadow:0 2px 16px rgba(0,0,0,.18)}}
.pg{{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:64px;border:0;background:rgba(0,0,0,.45);color:#fff;font-size:30px;cursor:pointer;z-index:2}}
.pg.l{{left:0}} .pg.r{{right:0}}
.vmeta{{display:flex;gap:12px;align-items:flex-start;justify-content:space-between;padding:10px 14px;background:#fff;border-top:1px solid #eee;flex-wrap:wrap}}
.kicker{{color:#e60012;font-weight:800;font-size:13px;letter-spacing:1px}}
.vtitle{{font-size:16px;font-weight:700;line-height:1.4;margin-top:2px}}
.vsrc{{font-size:13px;margin-top:4px}} .vsrc a{{color:#e60012;text-decoration:none}}
.vactions{{display:flex;gap:8px;flex-wrap:wrap}}
.strip{{display:flex;gap:8px;overflow-x:auto;padding:10px 12px;background:#fff;border-top:1px solid #eee}}
.strip button{{flex:none;width:84px;height:64px;border:2px solid transparent;background:#f6f6f6;padding:2px;cursor:pointer;position:relative}}
.strip button.on{{border-color:#e60012}}
.strip img{{width:100%;height:100%;object-fit:contain;display:block}}
.strip span{{position:absolute;left:0;top:0;background:rgba(0,0,0,.55);color:#fff;font-size:10px;padding:0 4px}}
.arch{{padding:48px 20px;text-align:center;background:#fff;margin:24px;border:1px solid #eee}}
.arch h2{{border:0;padding:0;margin:8px 0}}
.market{{border-left:1px solid #eee;padding:8px 12px 24px;overflow:auto;max-height:calc(100vh - 60px);position:sticky;top:60px;background:#fff}}
.market h2{{font-family:var(--fT);font-weight:900;font-size:18px;margin:16px 0 8px;padding:0 0 5px 10px;border-left:5px solid #e60012;border-bottom:1px solid #ccc;line-height:1.3}}
.market h2 small{{font-weight:400;font-size:12px;color:#777;margin-left:6px}}
.qs{{display:grid;grid-template-columns:1fr;border-top:1px solid #ddd;border-left:1px solid #ddd}}
.q{{border-right:1px solid #ddd;border-bottom:1px solid #ddd;padding:8px 10px}}
.qn{{font-family:var(--fN),var(--fT);font-weight:700;font-size:14px;color:#333}} .qn small{{color:#888;font-weight:400}}
.qv{{font-family:var(--fN);font-weight:700;font-size:22px;font-variant-numeric:tabular-nums;color:#111}}
.qd{{font-family:var(--fN);font-size:13px;font-weight:600}} .up{{color:#e60012}} .dn{{color:#008a3a}} .fl{{color:#555}}
.qq{{display:flex;flex-wrap:wrap;gap:2px 8px;font-family:var(--fN);font-size:11px;font-weight:500;color:#555;line-height:1.4;margin-top:4px}}
.note{{font-family:var(--fN),var(--fS);font-weight:500;font-size:11.5px;color:#777;margin-top:5px;line-height:1.5}}
.btn{{display:inline-block;border:1px solid #e60012;color:#e60012;background:#fff;font:700 14px var(--fT);text-decoration:none;border-radius:2px;padding:7px 14px;cursor:pointer}}
.btn.red{{background:#e60012;color:#fff}}
.tip{{font-family:var(--fS);font-weight:500;font-size:12px;color:#777;margin:6px 0}}
.tool{{background:#fff;border-top:1px solid #eee;padding:8px 12px 16px}}
.pick{{border-top:1px solid #222;margin-top:6px}}
.pk{{display:flex;align-items:center;gap:6px;padding:7px 2px;border-bottom:1px solid #eee;font-size:14px}}
.pk input{{width:20px;height:20px;flex:none}} .pk .n{{flex:none;width:22px;font-weight:900;color:#e60012;text-align:center}}
.pk .tx{{flex:1;line-height:1.35}} .pk button{{flex:none;width:30px;height:30px;border:1px solid #bbb;background:#fff;font-size:14px}}
.pk.sel{{background:#fff8e5}}
.fp{{display:flex;align-items:center;gap:6px;font-size:13px;color:#555;flex-wrap:wrap}}
.fbtn{{border:1px solid #bbb;background:#fff;padding:4px 10px;font:700 13px 'Noto Sans TC',sans-serif;cursor:pointer;border-radius:3px}} .fbtn small{{font-weight:400;font-size:10px;color:#888;margin-left:3px}}
.fbtn.on{{border-color:#e60012;color:#e60012}}
.bgs{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:6px 0 10px}}
.bg{{position:relative;border:2px solid transparent;padding:0;background:none;cursor:pointer}} .bg img{{width:100%;display:block}}
.bg.on{{border-color:#e60012}} .bg span{{position:absolute;left:0;right:0;bottom:0;background:rgba(0,0,0,.6);color:#fff;font-size:11px;padding:2px 0;text-align:center}}
.bg i{{position:absolute;top:2px;left:2px;background:#e60012;color:#fff;font:700 10px sans-serif;font-style:normal;padding:1px 4px}}
.cr2{{display:flex;align-items:center;gap:5px;flex-wrap:wrap;padding:5px 0;border-bottom:1px solid #eee;font:500 13px var(--fS)}} .cn2{{width:100%;color:#444}}
.sw{{width:28px;height:28px;border:1px solid #999;border-radius:50%;cursor:pointer;padding:0}} .sw.on{{outline:3px solid #e60012;outline-offset:1px}}
#cols input[type=color]{{width:36px;height:30px;border:1px solid #bbb;padding:0;background:#fff}}
.tbox{{border:1px solid #222;background:#fff;padding:8px 10px;margin:8px 0}}
.trow{{display:flex;align-items:center;gap:8px;margin:4px 0}} .trow label{{flex:none;width:4.5em;font:700 14px var(--fT)}}
.trow input,.trow select{{flex:1;min-width:0;font:500 16px 'Noto Sans TC',sans-serif;padding:6px 8px;border:1px solid #999;border-radius:4px;background:#fff;color:#222;-webkit-appearance:menulist}}
.trow .btn{{flex:none;padding:5px 8px;font-size:12px}}
.pv{{text-align:center}} .pv img{{width:100%;max-width:440px;height:auto;border:1px solid #ccc}}
.vbar{{display:flex;align-items:center;gap:8px;padding:8px 0;font-size:13px;color:#555}} .vbar .cnt{{font-weight:700;color:#222}}
footer{{background:#333;color:#fff;padding:14px 16px}}
footer .inner{{max-width:1180px;margin:0 auto;display:flex;gap:12px;align-items:center;font-size:12px;line-height:1.7}}
footer img{{width:48px;height:auto;flex:none;background:#fff;border-radius:4px}}
.dock{{display:none}}
.navmask{{display:none}}
@media (max-width:900px){{
  .brand{{font-size:20px;letter-spacing:1px}}
  #date-btn{{font-size:16px;min-width:0}}
  .zipbtn{{display:none}}
  .shell{{grid-template-columns:1fr;min-height:0}}
  .secnav{{display:none;position:fixed;z-index:45;top:60px;left:0;right:0;bottom:58px;max-height:none;border-right:0}}
  body.nav-open .secnav{{display:block}}
  body.nav-open .navmask{{display:block;position:fixed;inset:60px 0 58px 0;background:rgba(0,0,0,.35);z-index:44}}
  .market{{display:none;position:static;max-height:none;border-left:0;border-top:8px solid #e9e9e9}}
  body.mkt-open .market{{display:block}}
  body.mkt-open #read,body.mkt-open #archive{{display:none}}
  .viewer{{padding:8px 36px;min-height:200px}}
  .viewer img{{max-height:min(62vh,720px)}}
  .qs{{grid-template-columns:1fr 1fr}}
  .dock{{display:grid;grid-template-columns:repeat(5,1fr);position:fixed;left:0;right:0;bottom:0;height:58px;background:#fff;border-top:1px solid #ddd;z-index:50}}
  .dock button,.dock a{{border:0;background:none;color:#333;font-size:12px;font-weight:700;text-decoration:none;display:flex;align-items:center;justify-content:center;cursor:pointer}}
  body{{padding-bottom:58px}}
  footer .fp{{display:none}}
}}
</style></head><body>
<header class=topbar><div class=inner>
<button class=icon id=menu-btn aria-label=目錄>☰</button>
<div class=brand>{SITE}</div>
<div class=datebox>
  <button id=day-prev aria-label=前一日>‹</button>
  <button id=date-btn aria-haspopup=dialog>{DATE}（{WD}）</button>
  <button id=day-next aria-label=後一日>›</button>
  <div id=cal class=cal hidden></div>
</div>
<a class=zipbtn href="{ZIP}" download="{SITE}-{D8}-全部圖片.zip">下載當日</a>
</div></header>
<div class=navmask id=navmask></div>
<div class=shell>
<nav class=secnav id=secnav></nav>
<main class=stage>
<div id=read>
<div class=viewer id=viewer><button class="pg l" id=prev aria-label=上一頁>‹</button><img id=vimg src="img/{P0[0]}" alt="五大重點財經頭條"><button class="pg r" id=next aria-label=下一頁>›</button></div>
<div class=vmeta>
  <div><div class=kicker id=vkicker>A1 要聞</div><div class=vtitle id=vtitle>五大重點財經頭條</div><div class=vsrc id=vsrc></div></div>
  <div class=vactions><a class="btn red" id=vdl href="img/{P0[0]}" download="{D8}-每日報報-{P0[1]}.png">下載本頁</a><button class=btn id=custom-open type=button>自選頭條</button></div>
</div>
<div class=strip id=strip></div>
<div id=pcustom class=tool hidden>
<div class=tip style="color:#e60012;font-weight:700">自訂標題、字體、顏色或背景，勾選 5 則後按「產生海報」。</div>
<div class=tbox><div class=trow><label for=ptitle>海報標題</label><input id=ptitle maxlength=12><button class=btn id=ptreset type=button>還原每日報報</button></div>
<div class=trow><label for=tfont>標題字體</label><select id=tfont><option value="">預設（每日報報＝金色字圖）</option><option value=heavy>思源黑體 Heavy</option><option value=bold>思源黑體 Bold</option><option value=medium>思源黑體 Medium</option><option value=serif600>思源宋體 SemiBold</option><option value=serif400>思源宋體 Regular</option><option value=inter>Inter</option></select></div>
<div id=cols></div></div>
<div class=pick id=pick></div>
<div class=tip style="margin-top:12px">背景（預設「自動」＝今日依新聞類別自動挑選）：<button class=btn id=bgreset type=button style="padding:3px 10px;font-size:12px">重設為自動</button></div>
<div class=bgs id=bgs></div>
<div class=vbar><span class=cnt id=pcnt></span><button class="btn red" id=gen type=button style="margin-left:auto">產生海報</button></div>
<div class=pv id=pout></div>
</div>
</div>
<div id=archive class=arch hidden>
  <div class=kicker>存檔</div>
  <h2 id=arch-title></h2>
  <p>此日以全版圖片 ZIP 保存，內含海報與全部剪報。</p>
  <p><a class="btn red" id=arch-dl>下載此日 ZIP</a> <button class=btn id=back-today type=button>回到本日</button></p>
</div>
</main>
<aside class=market id=market>
<h2>匯率<small>臺銀即期賣出・新台幣／1外幣</small></h2><div class=qs>{fxh}</div>
<div class=note>{e(rates['page_note'])}</div>
<h2>重要指數</h2><div class=qs>{ixh}</div>
<div class=note>{e(d['idx_note'])}。紅漲綠跌。</div>
</aside>
</div>
<nav class=dock>
  <button type=button id=dock-menu>目錄</button>
  <button type=button id=dock-thumbs>縮圖</button>
  <a id=dock-dl href="img/{P0[0]}" download="{D8}-每日報報-{P0[1]}.png">下載</a>
  <button type=button id=dock-prev>上一頁</button>
  <button type=button id=dock-next>下一頁</button>
</nav>
<footer><div class=inner><img src="img/logo.png" alt="大心團隊"><div><div class=fp><span>字體</span><button class=fbtn data-f=sys type=button>預設配置</button><button class=fbtn data-f=sans type=button>思源黑體</button><button class=fbtn data-f=serif type=button>思源宋體</button><button class=fbtn data-f=jh type=button>微軟正黑體<small>Windows 限定</small></button></div>資料來源：{e(footer_src)}。<br>資料截至 {e(d['asof'])}（台北時間）。內容僅供參考，不構成投資建議。</div></div></footer>
<script>const D={js_data};</script>
<script src="app.js?v={VER}"></script>
</body></html>"""
open(f'{W}/index.html','w').write(html)
print("built",len(items),"items",ZIP)
