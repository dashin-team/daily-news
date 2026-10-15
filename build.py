# Build /workspace/news-web/index.html
SITE_TITLE="南恩新聞報報"; DATE="2026.10.15"
fx=[("美元","USD","32.34","32.135"),("澳幣","AUD","22.44","22.57"),("日圓","JPY","0.207","0.2047"),("人民幣","CNY","4.854","4.818")]
idx=[("道瓊","51,621.48","-48.62","-0.09%"),("標普500","7,718.94","-86.51","-1.11%"),("那斯達克","26,692.87","-511.51","-1.88%"),("台股加權","46,969.87","-1,655.96","-3.41%")]
heads=[("台股挫跌1655點　失守月線創單日第6大跌點","中央社","2026/10/15 13:53","https://www.cna.com.tw/news/afe/202610150126.aspx"),
("美9月通膨升至3.7%　共和黨期中選舉再添變數","中央社","2026/10/15 10:02","https://www.cna.com.tw/news/afe/202610150034.aspx"),
("政府將普發萬元　全教總籲正視退休基金永續經營","中央社","2026/10/15 11:19","https://www.cna.com.tw/news/ahel/202610150057.aspx"),
("股市大跌景氣差？今年前八月總薪資年增4.55％ 創16年新高","工商時報","2026/10/15 20:20","https://www.ctee.com.tw/news/20261015702223-430503"),
("拚2035年達「失智友善台灣888」　衛福部研議用藥納健保","中央社","2026/10/15 16:24","https://www.cna.com.tw/news/ahel/202610150214.aspx")]
posters=[("poster-v4-studio.png","每日報報 2026.10.15（新聞棚版）","20261015-每日報報-新聞棚版.png"),
("poster-v3-bluegreen.png","每日報報 2026.10.15（藍綠版）","20261015-每日報報-藍綠版.png"),
("poster-v2-101.png","每日報報 2026.10.15（101版）","20261015-每日報報-101版.png"),
("poster-v1-navy.png","每日報報 2026.10.15（深藍版）","20261015-每日報報-深藍版.png")]
clips=[("clip-ctee-salary.png","前八月總薪資 創16年同期新高","工商時報 2026/10/15","https://www.ctee.com.tw/news/20261015702223-430503","20261015-剪報-前八月總薪資.png"),
("clip-cna-cpi.png","美9月通膨3.7% 升息壓力再起","中央社 2026/10/15","https://www.cna.com.tw/news/afe/202610150034.aspx","20261015-剪報-美國9月通膨.png"),
("clip-cna-dementia.png","失智照護3.0 研議用藥納健保","中央社 2026/10/15","https://www.cna.com.tw/news/ahel/202610150214.aspx","20261015-剪報-失智照護3.0.png"),
("clip-cna-pension.png","普發萬元之際 全教總籲撥補退休基金","中央社 2026/10/15","https://www.cna.com.tw/news/ahel/202610150057.aspx","20261015-剪報-全教總退休基金.png")]
def chg(v,p):
    d=float(v)-float(p);dec=max(len(v.split('.')[1]),len(p.split('.')[1]));return ("up" if d>0 else "dn"),f"{d:+.{dec}f}",f"{d/float(p)*100:+.2f}%"
fxh="".join(f'<div class=card><div class=cn>{n}<small>{c}</small></div><div class=cv>{v}</div><div class="{chg(v,p)[0]} cd">{chg(v,p)[1]}<br>({chg(v,p)[2]})</div></div>' for n,c,v,p in fx)
ixh="".join(f'<div class=card><div class=cn>{n}</div><div class=iv>{v}</div><div class="{"up" if d[0]=="+" else "dn"} cd">{d}<br>({p})</div></div>' for n,v,d,p in idx)
hh="".join(f'<a class=hl href="{u}" target=_blank rel=noopener><span class=no>{i+1}</span><span class=ht>{h}<small>{s}｜{t}</small></span></a>' for i,(h,s,t,u) in enumerate(heads))
def fig(f,cap,dl,extra=""):
    return f'<figure><img src="img/{f}" alt="{cap}" loading=lazy><figcaption>{cap}{extra}</figcaption><a class=btn href="img/{f}" download="{dl}">下載圖片</a></figure>'
ph="".join(fig(f,c,d) for f,c,d in posters)
ch="".join(fig(f,c,d,f'<br><a href="{u}" target=_blank rel=noopener>原文：{s}</a>') for f,c,s,u,d in clips)
html=f"""<!doctype html><html lang=zh-Hant><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>{SITE_TITLE} {DATE}</title>
<link rel=preconnect href=https://fonts.googleapis.com><link rel=preconnect href=https://fonts.gstatic.com crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel=stylesheet>
<style>
*{{box-sizing:border-box}}
body{{margin:0;font-family:'Noto Sans TC','Noto Sans CJK TC',sans-serif;color:#fff;background:linear-gradient(180deg,#123a8c 0%,#105c96 40%,#168c8c 75%,#3bb54a 100%) fixed;}}
.wrap{{max-width:560px;margin:0 auto;padding:22px 14px 30px}}
h1{{margin:6px 0 0;text-align:center;font-weight:900;font-size:clamp(40px,12vw,64px);letter-spacing:2px;background:linear-gradient(180deg,#fff1b0,#f2b632 55%,#c98a12);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 3px 4px rgba(0,0,0,.45))}}
.date{{text-align:center;font-weight:900;font-size:26px;margin:2px 0 16px;text-shadow:0 2px 6px rgba(0,0,0,.5)}}
h2{{font-weight:900;font-size:22px;margin:22px 0 10px;text-align:center}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}
.card{{background:linear-gradient(180deg,#ffe17a,#f7c531);color:#111;border-radius:14px;text-align:center;padding:10px 6px;box-shadow:0 4px 10px rgba(0,0,0,.3)}}
.cn{{font-weight:900;font-size:18px}} .cn small{{font-size:12px;color:#555;margin-left:4px}}
.cv{{font-weight:900;font-size:30px;margin:2px 0}} .iv{{font-weight:900;font-size:22px;margin:4px 0}}
.cd{{font-weight:700;font-size:15px;line-height:1.3}} .up{{color:#c4001a}} .dn{{color:#05762a}}
.note{{font-size:12px;color:#dfe8ff;text-align:center;margin-top:8px;background:rgba(6,22,60,.45);border-radius:8px;padding:5px}}
.hl{{display:flex;gap:10px;align-items:flex-start;text-decoration:none;color:#fff;border:2px solid rgba(255,255,255,.9);border-radius:14px;padding:10px 12px;margin-bottom:9px;background:rgba(6,22,60,.6)}}
.no{{flex:none;width:28px;height:28px;border-radius:50%;background:#f2b632;color:#0a1a3a;font-weight:900;text-align:center;line-height:28px}}
.ht{{font-weight:700;font-size:16px;line-height:1.45}} .ht small{{display:block;font-weight:400;font-size:12px;color:#cfe0ff;margin-top:2px}}
figure{{margin:0 0 18px;background:rgba(6,22,60,.55);border-radius:14px;padding:10px;text-align:center}}
figure img{{width:100%;height:auto;display:block;border-radius:8px}}
figcaption{{font-size:14px;margin:8px 0;line-height:1.5}} figcaption a{{color:#ffe17a}}
.btn{{display:inline-block;background:#f2b632;color:#0a1a3a;font-weight:900;text-decoration:none;border-radius:999px;padding:9px 22px;font-size:15px}}
.all{{display:block;text-align:center;margin:8px auto 18px;width:max-content}}
.tip{{font-size:12px;color:#dfe8ff;text-align:center;margin-bottom:10px}}
footer{{font-size:12px;line-height:1.6;color:#e6eeff;background:rgba(6,22,60,.6);border-radius:12px;padding:10px 12px;display:flex;gap:10px;align-items:center;margin-top:20px}}
footer img{{width:56px;height:auto;flex:none}}
</style></head><body><div class=wrap>
<h1>{SITE_TITLE}</h1><div class=date>{DATE}</div>
<h2>匯率（臺銀即期賣出）</h2><div class=grid>{fxh}</div>
<div class=note>新台幣／1外幣，2026/10/15 21:02 掛牌；漲跌較 10/14 16:01 末次掛牌</div>
<h2>五大重點財經頭條</h2>{hh}
<h2>重要指數</h2><div class=grid>{ixh}</div>
<div class=note>美股為美東 10/14 收盤；台股加權為 10/15 收盤；紅漲綠跌</div>
<h2>今日海報</h2><div class=tip>點「下載圖片」儲存，或在手機上長按圖片另存。</div>
<a class="btn all" href="news-20261015-all.zip" download="南恩新聞報報-20261015-全部圖片.zip">全部下載（ZIP）</a>
{ph}
<h2>新聞剪報</h2>{ch}
<footer><img src="img/logo.png" alt="大心團隊"><div>資料來源：臺灣銀行牌告匯率（rate.bot.com.tw）、臺灣證券交易所、Reuters／Investing.com、中央社、工商時報。<br>資料截至 2026/10/15 21:02（台北時間）。內容僅供參考，不構成投資建議。</div></footer>
</div></body></html>"""
open('/workspace/news-web/index.html','w').write(html)
