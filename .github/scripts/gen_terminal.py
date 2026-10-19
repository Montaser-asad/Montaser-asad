import json, os, sys, urllib.request
USER="Montaser-asad"
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"terminal-gen"})
    tok=os.environ.get("GITHUB_TOKEN")
    if tok: req.add_header("Authorization",f"Bearer {tok}")
    return json.load(urllib.request.urlopen(req,timeout=20))
def live():
    try:
        u=get(f"https://api.github.com/users/{USER}")
        repos=get(f"https://api.github.com/users/{USER}/repos?per_page=100")
        return u["public_repos"],u["followers"],sum(r["stargazers_count"] for r in repos)
    except Exception as e:
        print("live data unavailable:",e,file=sys.stderr); return None
LIVE=live()
OUT=sys.argv[1] if len(sys.argv)>1 else "assets/hero.svg"

BG,PINK,GRN,CYN,YEL,TXT="#0f111a","#ff6ac1","#5af78e","#57d7ff","#fff06b","#ffffff"
FS=18; CW=10.84; W=880; STEP=26
PFX="montaser@github.com:~$ "
HID="inset(-6px 100% -6px 0)"; FULL="inset(-6px 0 -6px 0)"; FX="inset(-6px -30px -6px 0)"
o=[]; T=[0.4]; kf=[]
def tspan(c,t): return f'<tspan fill="{c}">{t}</tspan>'
def typed(x,y,inner,n,speed,fill=TXT):
    dur=max(n*speed,0.05)
    o.append(f'<text x="{x}" y="{y}" textLength="{n*CW:.2f}" lengthAdjust="spacing" fill="{fill}" class="ty" style="--n:{n};--d:{dur:.2f}s;--t:{T[0]:.2f}s">{inner}</text>')
    T[0]+=dur; return dur
def prefix(y):
    o.append(f'<text x="30" y="{y}" textLength="{len(PFX)*CW:.2f}" lengthAdjust="spacing" class="l" style="--t:{T[0]:.2f}s">{tspan(PINK,"montaser@github.com")}{tspan(TXT,":")}{tspan(CYN,"~")}{tspan(GRN,"$ ")}</text>')
def prompt(y,cmd):
    prefix(y); T[0]+=0.25
    x=30+len(PFX)*CW; n=len(cmd); t0=T[0]
    dur=typed(x,y,cmd,n,0.08)
    o.append(f'<rect x="{x:.2f}" y="{y-17}" width="{CW}" height="22" fill="{TXT}" class="cm" style="--n:{n};--d:{dur:.2f}s;--t:{t0:.2f}s;--w:{n*CW:.2f}px"/>')
    T[0]+=0.2
def out(y,parts,speed=0.02):
    n=sum(len(t) for c,t in parts)
    typed(30,y,"".join(tspan(c,t) for c,t in parts),n,speed); T[0]+=0.05

rows=[("OS","GitHub Profile"),("Focus","Systems, Networking, Cyber Security"),("Languages","C, C++, Java, Python")]
if LIVE: rows.append(("GitHub",f"{LIVE[0]} repos, {LIVE[1]} followers, {LIVE[2]} stars"))
about=[
 [(TXT,"I'm a "),(CYN,"cybersecurity"),(TXT," student based in Amman, Jordan.")],
 [(TXT,"I'm studying for a Bachelor's in "),(CYN,"Cybersecurity"),(TXT," at Applied")],
 [(TXT,"Science University (graduating 2029).")],
 [(TXT,"Alongside that I'm doing "),(YEL,"42 Amman"),(TXT,", where I write "),(GRN,"C"),(TXT," and")],
 [(TXT,"systems projects.")],
 [(TXT,"Outside of code: I have a diploma in "),(YEL,"Fine Arts"),(TXT," (guitar)")],
 [(TXT,"and I play chess.")],
]
Y1=70; Y2=Y1+STEP*1+30        # whoami out at Y1+26
YN=Y2                          # neofetch prompt
rows_y0=YN+30
YA=rows_y0+STEP*(len(rows)-1)+44   # cat about.txt prompt
ay0=YA+30
Y=ay0+STEP*(len(about)-1)+44       # loop prompt
H=Y+30
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="@@H@@" viewBox="0 0 {W} @@H@@" role="img" aria-label="Terminal session: whoami, neofetch, cat about.txt. Montaser Asad, a cybersecurity student in Amman, Jordan, studying at Applied Science University (graduating 2029), doing 42 Amman with C and systems projects, with a diploma in Fine Arts (guitar) who plays chess. A prompt keeps typing: Cyber Security student, 42 Amman student, Software Engineer, Systems and Networking enthusiast.">')
o.append('@@STYLE@@')
o.append(f'<rect width="{W}" height="@@H@@" rx="12" fill="{BG}" stroke="#2a2d3e" stroke-width="2"/>')
for i,c in enumerate(["#ff5555","#ffb86c","#5af78e"]): o.append(f'<circle cx="{30+i*28}" cy="26" r="8" fill="{c}"/>')
prompt(Y1,"whoami"); out(Y1+STEP,[(GRN,"MONTASER ASAD")],0.03)
T[0]+=0.15
prompt(YN,"neofetch")
for i,(k,v) in enumerate(rows): out(rows_y0+i*STEP,[(YEL,k+": "),(TXT,v)],0.014)
T[0]+=0.2
prompt(YA,"cat about.txt")
for i,l in enumerate(about): out(ay0+i*STEP,l,0.018)
T[0]+=0.25
prefix(Y); T[0]+=0.3
x0=30+len(PFX)*CW
phr=["Cyber Security student","42 Amman student","Software Engineer","Systems & Networking enthusiast"]
HOLD,GAP=1.4,0.35
sl=[]
for p in phr:
    n=len(p); tT=0.085*n; tD=0.04*n; sl.append((tT,tD,tT+HOLD+tD+GAP))
C=sum(s[2] for s in sl); off=0; E=0.001
def P(v): return f"{v/C*100:.3f}%"
for i,p in enumerate(phr):
    n=len(p); tT,tD,slot=sl[i]
    a,b,c,d,e=off,off+tT,off+tT+HOLD,off+tT+HOLD+tD,off+slot
    esc=p.replace("&","&amp;")
    kf.append(f"@keyframes pt{i}{{0%,{P(a)}{{clip-path:{HID};animation-timing-function:steps({n},end)}}{P(b)}{{clip-path:{FULL}}}{P(b+E*C)}{{clip-path:{FX}}}{P(c)}{{clip-path:{FX}}}{P(c+E*C)}{{clip-path:{FULL};animation-timing-function:steps({n},end)}}{P(d)}{{clip-path:{HID}}}100%{{clip-path:{HID}}}}}")
    w=n*CW
    pre=f"0%,{P(max(a-E*C,0))}{{opacity:0}}" if a>0 else ""
    first=f"{P(a)}{{opacity:1;transform:translateX(0);animation-timing-function:steps({n},end)}}"
    tail=(f"{P(e)}{{opacity:1}}{P(e+E*C)}{{opacity:0}}100%{{opacity:0}}" if e<C-1e-9 else "100%{opacity:1}")
    kf.append(f"@keyframes pc{i}{{{pre}{first}{P(b)}{{transform:translateX({w:.2f}px)}}{P(c)}{{transform:translateX({w:.2f}px);animation-timing-function:steps({n},end)}}{P(d)}{{transform:translateX(0)}}{tail}}}")
    o.append(f'<text x="{x0:.2f}" y="{Y}" textLength="{w:.2f}" lengthAdjust="spacing" fill="{TXT}" class="ph" style="animation:pt{i} {C:.2f}s linear {T[0]:.2f}s infinite">{esc}</text>')
    o.append(f'<rect x="{x0:.2f}" y="{Y-17}" width="{CW}" height="22" fill="{TXT}" class="pc" style="animation:pc{i} {C:.2f}s linear {T[0]:.2f}s infinite"/>')
    off+=slot
style=f'''<style>
text{{font-family:'JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,monospace;font-size:{FS}px;font-weight:700;white-space:pre}}
.l{{opacity:0;animation:s .01s steps(1) var(--t) forwards}}@keyframes s{{to{{opacity:1}}}}
.ty{{clip-path:{HID};animation:ty var(--d) steps(var(--n),end) var(--t) forwards}}
@keyframes ty{{0%{{clip-path:{HID}}}99.99%{{clip-path:{FULL}}}100%{{clip-path:{FX}}}}}
.cm{{opacity:0;animation:vis var(--d) linear var(--t) both,mv var(--d) steps(var(--n),end) var(--t) both}}
@keyframes vis{{0%{{opacity:0}}1%{{opacity:1}}99%{{opacity:1}}100%{{opacity:0}}}}
@keyframes mv{{from{{transform:translateX(0)}}to{{transform:translateX(var(--w))}}}}
.ph{{clip-path:{HID}}}.pc{{opacity:0}}
{chr(10).join(kf)}
</style>'''
o=[x.replace('@@STYLE@@',style).replace('@@H@@',str(H)) for x in o]
o.append('</svg>')
open(OUT,'w').write("\n".join(o))
print("H",H,"intro",round(T[0],1),"loop",round(C,1))
