#!/usr/bin/env python3
"""Data-driven builder: reads data.json (+ img/cards/<id>.png, img/poster-*.png) -> index.html + date-named ZIP.

Page chrome matches the public 南恩新聞報報 edition (masthead, five headlines,
indices, clip switcher, poster tabs, ZIP). Historical news-*-all.zip files are kept.
"""
import json,os,zipfile,datetime,html as H
W=os.path.dirname(os.path.abspath(__file__)); d=json.load(open(f'{W}/data.json'))
SITE="南恩新聞報報"; DATE=d['date']; D8=DATE.replace('.','')
WD="日一二三四五六"[datetime.date(*map(int,DATE.split('.'))).isoweekday()%7]
idx=[[n,v,dd,p,"up" if str(dd)[:1]=="+" else "dn" if str(dd)[:1]=="-" else "fl"] for n,v,dd,p in d['idx']]
items=d['items']
for it in items:
    it['img']=f"img/cards/{it['id']}.png"; it['dl']=f"{D8}-剪報-{it['short'].split('　')[0]}.png".replace('/','-').replace('?','').replace('？','')
    assert os.path.exists(f"{W}/{it['img']}"),it['id']
top=sorted([i for i in items if i.get('top')],key=lambda i:i['top'])
assert len(top)==5, [i['id'] for i in top]
e=H.escape
ixh="".join(f'<div class=q><div class=qn>{n}</div><div class=qv>{v}</div><div class="{u} qd">{"▲" if u=="up" else "▼" if u=="dn" else "－"} {a}（{p}）</div></div>' for n,v,a,p,u in idx)
hh="".join(f'<a class=hl href="{i["url"]}" target=_blank rel=noopener><span class=no>{k+1}</span><span class=ht>{e(i["title"])}<small>{i["src"]}｜{i["time"]}</small></span></a>' for k,i in enumerate(top))
tabs='<button class="tab on" data-c="全部">全部</button>'+"".join(f'<button class=tab data-c="{c}">{c}</button>' for c in d['cats'])
ptabs="".join(f'<button class="ptab{" on" if k==0 else ""}" data-k="{k}">{n}</button>' for k,(f,n) in enumerate(d['posters']))+'<button class=ptab data-k="custom">自選頭條</button>'
ZIP=f"news-{D8}-all.zip"
with zipfile.ZipFile(f'{W}/{ZIP}','w') as z:
    for f,n in d['posters']: z.write(f'{W}/img/{f}',f'{D8}-每日報報-{n}.png')
    for k,i in enumerate(items): z.write(f"{W}/{i['img']}",f"{k+1:02d}-{i['dl']}")
P0=d['posters'][0]
js_data=json.dumps(dict(date=DATE,D8=D8,idx=idx,items=items,posters=d['posters'],bg_auto=d.get('bg_auto','newsroom'),bg_pool=d.get('bg_pool',[]),idxnote=d['idx_note'],sources=d['sources'],asof=d['asof']),ensure_ascii=False)
import hashlib,time
VER=hashlib.md5(open(f'{W}/app.js','rb').read()).hexdigest()[:8]+'-'+time.strftime('%m%d%H%M')
html=f"""<!doctype html><html lang=zh-Hant><head><meta charset=utf-8><meta http-equiv=Cache-Control content="no-cache, no-store, must-revalidate"><meta http-equiv=Pragma content=no-cache><meta http-equiv=Expires content=0>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>A1 要聞 | {DATE} | {SITE}</title>
<link rel=preconnect href=https://fonts.googleapis.com><link rel=preconnect href=https://fonts.gstatic.com crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@400;600;700&display=swap" rel=stylesheet>
<style>
*{{box-sizing:border-box}}
body{{--fT:'Noto Sans TC','Noto Sans CJK TC',sans-serif;--fH:'Noto Serif TC','Noto Serif CJK TC',serif;--fB:'Noto Serif TC','Noto Serif CJK TC',serif;--fS:'Noto Sans TC','Noto Sans CJK TC',sans-serif;--fN:'Inter';margin:0;background:#f4f2ec;color:#222;font-family:var(--fN),var(--fS);font-weight:500;font-variant-numeric:tabular-nums;-webkit-text-size-adjust:none}}
.paper{{max-width:640px;margin:0 auto;background:#fffefa;padding:14px 16px 28px;min-height:100vh}}
.top{{display:flex;justify-content:space-between;font-size:12px;color:#666;border-bottom:1px solid #222;padding-bottom:5px}}
.mast{{text-align:center;padding:12px 0 8px;border-bottom:4px double #222}}
.mast h1{{margin:0;font-family:var(--fH);font-weight:600;font-size:clamp(42px,13vw,72px);letter-spacing:6px;line-height:1.1;color:#111}}
.ed{{display:flex;align-items:center;gap:10px;border-bottom:1px solid #222;padding:7px 0;font-size:14px}}
.ed .pg{{background:#e60012;color:#fff;font-family:var(--fN),var(--fT);font-weight:800;padding:2px 8px}} .ed b{{font-family:var(--fT);font-weight:900}} .ed .d{{margin-left:auto;color:#444}}
h2{{font-family:var(--fT);font-weight:900;font-size:19px;margin:22px 0 8px;padding:0 0 5px 10px;border-left:5px solid #e60012;border-bottom:1px solid #ccc;line-height:1.3}}
h2 small{{font-weight:400;font-size:12px;color:#777;margin-left:6px}}
.qs{{display:grid;grid-template-columns:repeat(2,1fr);border-top:1px solid #ddd;border-left:1px solid #ddd}}
.q{{border-right:1px solid #ddd;border-bottom:1px solid #ddd;padding:9px 10px}}
.qn{{font-family:var(--fN),var(--fT);font-weight:700;font-size:14px;color:#333}} .qn small{{color:#888;font-weight:400}}
.qv{{font-family:var(--fN);font-weight:700;font-size:24px;font-variant-numeric:tabular-nums;color:#111}}
.qd{{font-family:var(--fN);font-size:13px;font-weight:600}} .up{{color:#e60012}} .dn{{color:#008a3a}} .fl{{color:#555}}
.note{{font-family:var(--fN),var(--fS);font-weight:500;font-size:11.5px;color:#777;margin-top:5px;line-height:1.5}}
.hl{{display:flex;gap:10px;text-decoration:none;color:#111;border-bottom:1px solid #ddd;padding:11px 0}}
.no{{flex:none;font-family:var(--fN);font-weight:800;font-size:22px;color:#e60012;width:20px;line-height:1.2}}
.ht{{font-family:var(--fN),var(--fH);font-weight:600;font-size:17px;line-height:1.45}}
.ht small{{display:block;font-family:var(--fN),var(--fS);font-weight:500;font-size:12px;color:#888;margin-top:3px}}
.tabs{{display:flex;gap:0;border-bottom:2px solid #222;margin-bottom:10px;overflow-x:auto}}
.tab,.ptab{{flex:1;background:none;border:0;padding:8px 6px;font:700 15px var(--fT);color:#666;white-space:nowrap;cursor:pointer}}
.tab.on,.ptab.on{{background:#222;color:#fff}}
.viewer{{position:relative;border:1px solid #ccc;background:#fff}}
.viewer img{{width:100%;height:auto;display:block}}
.arw{{position:absolute;top:50%;transform:translateY(-50%);width:36px;height:52px;border:0;background:rgba(0,0,0,.35);color:#fff;font-size:24px;cursor:pointer}}
.arw.l{{left:0}} .arw.r{{right:0}}
.vbar{{display:flex;align-items:center;gap:8px;padding:8px 0;font-size:13px;color:#555}} .vbar .cnt{{font-weight:700;color:#222}}
.vbar .btn{{margin-left:auto}} .vsrc{{font-size:13px;margin:0 0 6px}} .vsrc a{{color:#e60012;text-decoration:none}}
.list{{border-top:1px solid #222}}
.it{{display:flex;gap:8px;padding:9px 4px;border-bottom:1px solid #ddd;cursor:pointer}}
.it.cur{{background:#fdf0f0}} .it .c{{flex:none;font-family:var(--fT);font-weight:700;font-size:11px;border:1px solid #e60012;color:#e60012;padding:0 4px;height:18px;line-height:16px;margin-top:3px}}
.it .t{{font-family:var(--fN),var(--fH);font-weight:600;font-size:15.5px;line-height:1.45}} .it small{{display:block;font:500 12px var(--fN),var(--fS);color:#888}}
.pv{{text-align:center}} .pv img{{width:100%;max-width:440px;height:auto;border:1px solid #ccc}}
.btn{{display:inline-block;border:1px solid #e60012;color:#e60012;background:#fff;font:700 14px var(--fT);text-decoration:none;border-radius:4px;padding:7px 18px;cursor:pointer}}
.btn.red{{background:#e60012;color:#fff}} .all{{display:block;text-align:center;margin:6px 0 14px}}
.tip{{font-family:var(--fS);font-weight:500;font-size:12px;color:#777;margin:6px 0}}
.pick{{border-top:1px solid #222;margin-top:6px}}
.pk{{display:flex;align-items:center;gap:6px;padding:7px 2px;border-bottom:1px solid #eee;font-size:14px}}
.pk input{{width:20px;height:20px;flex:none}} .pk .n{{flex:none;width:22px;font-weight:900;color:#e60012;text-align:center}}
.pk .tx{{flex:1;line-height:1.35}} .pk button{{flex:none;width:30px;height:30px;border:1px solid #bbb;background:#fff;font-size:14px}}
.pk.sel{{background:#fff8e5}}
.fp{{display:flex;align-items:center;gap:6px;margin-top:10px;font-size:13px;color:#555;flex-wrap:wrap}}
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
footer{{font-family:var(--fN),var(--fS);font-weight:500;margin-top:22px;border-top:4px double #222;padding-top:10px;font-size:12px;line-height:1.7;color:#555;display:flex;gap:10px;align-items:center}}
footer img{{width:52px;height:auto;flex:none}}
.nn-back{{display:block;max-width:640px;margin:0 auto;padding:10px 16px 0;font:600 13px/1.4 'Noto Sans TC',sans-serif;color:#1565c0;text-decoration:none}}.nn-back:hover{{color:#0e9f9a}}
</style></head><body><a class="nn-back" href="./">← 回南恩官網・每日財經</a><div class=paper>
<div class=top><span>{DATE}（{WD}）</span><span>財經・保險・理財</span></div>
<div class=mast><h1>{SITE}</h1></div>
<div class=ed><span class=pg>A1</span><b>要聞</b><span class=d>{DATE}</span></div>
<div class=fp><span>字體</span><button class=fbtn data-f=sys>預設配置</button><button class=fbtn data-f=sans>思源黑體</button><button class=fbtn data-f=serif>思源宋體</button><button class=fbtn data-f=jh>微軟正黑體<small>Windows 限定</small></button></div>
<h2>五大重點財經頭條</h2>{hh}
<h2>重要指數</h2><div class=qs>{ixh}</div>
<div class=note>{d['idx_note']}。紅漲綠跌。</div>

<h2>今日新聞剪報<small>點新聞、左右箭頭或滑動切換</small></h2>
<div class=tabs id=ctabs>{tabs}</div>
<div class=viewer id=viewer><img id=vimg src="{items[0]['img']}" alt="{e(items[0]['title'])}"><button class="arw l" id=prev aria-label=上一則>‹</button><button class="arw r" id=next aria-label=下一則>›</button></div>
<div class=vbar><span class=cnt id=vcnt></span><a class="btn red" id=vdl href="{items[0]['img']}" download="{items[0]['dl']}">下載圖片</a></div>
<div class=vsrc id=vsrc></div>
<div class=tip>可在手機上長按圖片另存。</div>
<div class=list id=list></div>

<h2>今日海報<small>五大重點頭條</small></h2>
<div class=tabs id=ptabs>{ptabs}</div>
<div class=tip style="color:#e60012;font-weight:700">想自訂標題、標題字體、顏色或背景？請點上方「自選頭條」。</div>
<div id=pstatic class=pv><img id=pimg src="img/{P0[0]}" alt="每日報報 {P0[1]}"><div class=vbar style="justify-content:center"><a class="btn red" id=pdl href="img/{P0[0]}" download="{D8}-每日報報-{P0[1]}.png" style="margin:0">下載圖片</a></div></div>
<div id=pcustom style="display:none">
<div class=tbox><div class=trow><label for=ptitle>海報標題</label><input id=ptitle maxlength=12><button class=btn id=ptreset>還原每日報報</button></div>
<div class=trow><label for=tfont>標題字體</label><select id=tfont><option value="">預設（每日報報＝金色字圖）</option><option value=heavy>思源黑體 Heavy</option><option value=bold>思源黑體 Bold</option><option value=medium>思源黑體 Medium</option><option value=serif600>思源宋體 SemiBold</option><option value=serif400>思源宋體 Regular</option><option value=inter>Inter</option></select></div>
<div id=cols></div></div>
<div class=tip>勾選 5 則頭條（預設為今日五大重點），用 ▲▼ 調整順序，再按「產生海報」。</div>
<div class=pick id=pick></div>
<div class=tip style="margin-top:12px">背景（預設「自動」＝今日依新聞類別自動挑選）：<button class=btn id=bgreset style="padding:3px 10px;font-size:12px">重設為自動</button></div>
<div class=bgs id=bgs></div>
<div class=vbar><span class=cnt id=pcnt></span><button class="btn red" id=gen style="margin-left:auto">產生海報</button></div>
<div class=pv id=pout></div>
</div>
<a class="btn all" href="{ZIP}" download="{SITE}-{D8}-全部圖片.zip">全部下載（ZIP，海報＋全部剪報）</a>
<footer><img src="img/logo.png" alt="大心團隊"><div>資料來源：{e(d['sources'])}。<br>資料截至 {e(d['asof'])}（台北時間）。內容僅供參考，不構成投資建議。</div></footer>
</div>
<script>const D={js_data};</script>
<script src="app.js?v={VER}"></script>
</body></html>"""
open(f'{W}/index.html','w').write(html)
print("built",len(items),"items",ZIP)
