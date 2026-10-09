import re, sys, pathlib
P = pathlib.Path(sys.argv[1])
A = P / "assets"

def lucide(name, cls="ic"):
    t = (A / f"icons/lucide-{name}.svg").read_text()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", t, re.S).group(1)
    inner = re.sub(r"<!--.*?-->", "", inner, flags=re.S).strip()
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

def si(name, cls="si"):
    d = re.search(r'<path d="([^"]+)"', (A / f"icons/si-{name}.svg").read_text()).group(1)
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{d}" /></svg>'

def logo(name, cls):
    t = (A / f"zentury-{name}.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', t).group(1)
    g = re.search(r"(<g transform=.*</g>)", t, re.S).group(1)
    g = g.replace('fill="#000000"', 'fill="currentColor"')
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true">{g}</svg>'

T = (pathlib.Path(sys.argv[2])).read_text()
T = re.sub(r"\{\{lucide:([a-z-]+)(?::([a-z-]+))?\}\}", lambda m: lucide(m.group(1), m.group(2) or "ic"), T)
T = re.sub(r"\{\{si:([a-z-]+)(?::([a-z-]+))?\}\}", lambda m: si(m.group(1), m.group(2) or "si"), T)
T = re.sub(r"\{\{logo:([a-z]+):([a-z-]+)\}\}", lambda m: logo(m.group(1), m.group(2)), T)
(P / "index.html").write_text(T)
print("ok", len(T.splitlines()))
