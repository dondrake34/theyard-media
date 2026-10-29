"""Ep01 scenes: The School That Started With $1.50 (Mary McLeod Bethune / Bethune-Cookman).
Worked example: one function per narration paragraph, timed with beat(i, "phrase")."""
from lib import *


# ================= SCENES
def s0(cr, t):  # hook
    i = 0
    a, b = scene_bounds(i)
    bg(cr, SKY, BG)
    # sun
    cr.arc(1500, 330, 120, 0, 2 * math.pi); cr.set_source_rgba(1, 0.75, 0.35, 0.8); cr.fill()
    ground(cr, 860)
    dump_pile(cr, 1450, 862, 1.0, t)
    house(cr, 760, 862, 1.15, door_open=ease(prog(t, beat(i, "unlocks the door"), 0.8)))
    tw = beat(i, "A young woman")
    pw = prog(t, tw - 0.6, 2.2)
    if pw > 0:
        mary(cr, 120 + 555 * ease(pw), 862, 0.95, t, pose="rest", pose_to="knock",
             pose_t=prog(t, beat(i, "unlocks the door") - 0.2, 0.4) - prog(t, beat(i, "unlocks the door") + 0.9, 0.4))
    text(cr, "OCTOBER 3, 1904", 96, 150, 78, MAROON, align="left", alpha=clamp(t / 0.6))
    text(cr, "DAYTONA BEACH, FLORIDA", 100, 210, 38, TEXT, align="left", alpha=clamp((t - 0.6) / 0.6))
    tb = beat(i, "right next to the city dump")
    p = prog(t, tb, 0.6)
    if p > 0:
        cr.save(); cr.set_source_rgba(*MAROON, p); cr.set_line_width(7); cr.set_dash([18, 12])
        cr.move_to(1000, 600); cr.curve_to(1120, 520, 1250, 560, 1300, 640); cr.stroke(); cr.restore()
        text(cr, "next door", 1150, 520, 40, MAROON, alpha=p * (1 - prog(t, beat(i, "the desks are old wooden crates"), 0.3)))
    # crates inside: overlay inset panel
    tc = beat(i, "the desks are old wooden crates")
    tm = beat(i, "in her pocket")
    pc = prog(t, tc, 0.4) * (1 - prog(t, tm, 0.3))
    if pc > 0:
        panel(cr, 1220, 300, 560, 380, (0.93, 0.86, 0.74), alpha=pc)
        cr.save(); cr.push_group()
        crate(cr, 1370, 620, 160, 110); crate(cr, 1550, 620, 160, 110); crate(cr, 1460, 510, 130, 90)
        cr.pop_group_to_source(); cr.paint_with_alpha(pc); cr.restore()
        text(cr, "DESKS = CRATES", 1500, 360, 44, MAROON, alpha=pc)
    pm = prog(t, tm, 0.5)
    if pm > 0:
        cr.set_source_rgba(0, 0, 0, 0.35 * pm); cr.paint()
        r = 260 * back_out(pm)
        coin(cr, W / 2, 520, r, spin=max(0, (t - tm) * 4.5) if t < tm + 1.4 else 0)
        pop_text(cr, "ONE DOLLAR AND FIFTY CENTS", W / 2, 900, 64, t, beat(i, "One dollar"), color=(1, 1, 1),
                 outline=INK)
    fade_edges(cr, t, a, b)


def s1(cr, t):
    i = 1
    a, b = scene_bounds(i)
    bg(cr)
    ground(cr, 880)
    house(cr, 1350, 882, 1.0, door_open=1.0)
    tq = beat(i, "So how do you build")
    tk = beat(i, "five little girls")
    # Mary at her door, welcoming the children
    pin = back_out(prog(t, a + 0.1, 0.5))
    mary(cr, 1120, 882, 1.15 * pin, t, pose="rest", pose_to="welcome", pose_t=prog(t, tk - 0.3, 0.6))
    text(cr, "MARY McLEOD BETHUNE", W / 2, 150, 76, MAROON, alpha=prog(t, a + 0.2, 0.5))
    # kids walk in from the left toward her
    cols = [MAROON, GOLDC, (0.30, 0.45, 0.60), GREEN, (0.75, 0.40, 0.50)]
    for k in range(6):
        st = tk + k * 0.3
        p = prog(t, st, 2.8)
        if p <= 0:
            continue
        x = -120 + (890 - k * 115 + 120) * ease(p)
        kid(cr, x, 880, 0.85 if k < 5 else 0.75, cols[k] if k < 5 else (0.25, 0.30, 0.45), girl=k < 5, t=t, walking=p < 1)
    pc = prog(t, tk + 0.5, 0.4)
    if pc > 0:
        text(cr, "5 girls + her son, Albert", W / 2, 240, 48, TEXT, alpha=pc)
    th = beat(i, "an H. B. C. U.")
    ph = prog(t, th, 0.5) * (1 - prog(t, tq - 0.3, 0.4))
    if ph > 0:
        cr.set_source_rgba(*MAROON, 0.97 * ph); cr.paint()
        text(cr, "H B C U", W / 2, 520, 200, GOLDC, alpha=ph, scale=back_out(prog(t, th, 0.5)))
        text(cr, "Historically Black Colleges & Universities", W / 2, 640, 52, (1, 1, 1), alpha=ph)
    pq = prog(t, tq, 0.5)
    if pq > 0:
        cr.set_source_rgba(*MAROON, 0.97 * pq); cr.paint()
        text(cr, "How do you build a college", W / 2, 430, 84, (1, 1, 1), alpha=pq)
        text(cr, "out of $1.50?", W / 2, 560, 120, GOLDC, alpha=pq, scale=back_out(prog(t, tq + 0.6, 0.5)))
    fade_edges(cr, t, a, b)


def s2(cr, t):
    i = 2
    a, b = scene_bounds(i)
    bg(cr, (0.95, 0.90, 0.80), (0.90, 0.84, 0.72))
    kicker(cr, "1875 · MAYESVILLE, SOUTH CAROLINA", t, a + 0.1)
    # 17 children dots
    t15 = beat(i, "fifteenth of seventeen")
    for k in range(17):
        p = prog(t, t15 + k * 0.06, 0.3)
        if p <= 0:
            continue
        x = 300 + k * 78; y = 330
        hl = k == 14
        r = 28 * back_out(p) * (1.35 if hl and t > t15 + 1.3 else 1)
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.set_source_rgb(*(GOLDC if hl and t > t15 + 1.3 else BLACK)); cr.fill()
    if t > t15 + 1.3:
        text(cr, "#15 of 17 children", 300 + 14 * 78, 420, 40, MAROON, alpha=prog(t, t15 + 1.3, 0.4))
    te = beat(i, "Her parents had been enslaved")
    pe = prog(t, te, 0.5) * (1 - prog(t, beat(i, "She was the only child"), 0.4))
    if pe > 0:
        text(cr, "Her parents had been enslaved.", W / 2, 520, 56, TEXT, alpha=pe)
    # walking 5 miles
    tw = beat(i, "she walked five miles")
    pw = prog(t, beat(i, "She was the only child"), 0.5)
    if pw > 0:
        ground(cr, 900)
        # path
        cr.set_source_rgba(*MAROON, pw); cr.set_line_width(6); cr.set_dash([20, 14])
        cr.move_to(260, 880); cr.line_to(1660, 880); cr.stroke(); cr.set_dash([])
        # cabin + school
        building(cr, 1700, 898, 220, 240, (0.95, 0.92, 0.85), cols=2)
        text(cr, "SCHOOL", 1700, 960, 34, TEXT, alpha=pw)
        pk = prog(t, tw - 0.5, 6.0)
        kid(cr, 280 + 1250 * pk, 898, 0.95, MAROON, True, t, walking=0 < pk < 1)
        pop_text(cr, "5 MILES A DAY", 960, 560, 90, t, tw, color=MAROON)
        pop_text(cr, "the only one of her siblings in school", 960, 630, 44, t, beat(i, "She was the only child") + 0.6)
    tm = beat(i, "Teaching wasn't her job yet")
    pm = prog(t, tm, 0.5)
    if pm > 0:
        cr.set_source_rgba(*BG, pm); cr.paint()
        text(cr, "Teaching wasn't her job yet.", W / 2, 470, 70, TEXT, alpha=pm)
        pop_text(cr, "It was her MISSION.", W / 2, 600, 96, t, beat(i, "It was already"), color=MAROON)
    fade_edges(cr, t, a, b)


def s3(cr, t):
    i = 3
    a, b = scene_bounds(i)
    bg(cr)
    kicker(cr, "NO MONEY FOR SUPPLIES", t, a + 0.1)
    tpie = beat(i, "And when the school")
    mary(cr, 1700, 1000, 1.45, t, pose="think", pose_to="welcome", pose_t=prog(t, tpie, 0.6))
    items = [("Ink?", "elderberries", beat(i, "Ink?"), 360),
             ("Pencils?", "burned wood", beat(i, "Pencils?"), 820),
             ("Desks?", "thrown-out crates", beat(i, "Desks?"), 1280)]
    tp = beat(i, "she baked sweet potato pies")
    fade_items = prog(t, tp - 0.3, 0.4)
    for lab, sub, st, x in items:
        p = prog(t, st, 0.45)
        if p <= 0:
            continue
        al = 1 - fade_items
        if al <= 0:
            continue
        cr.save(); cr.push_group()
        panel(cr, x - 200, 300, 400, 460, (1, 1, 1))
        text(cr, lab, x, 380, 60, MAROON)
        cy = 560
        if lab == "Ink?":
            for k in range(9):
                cr.arc(x - 50 + (k % 3) * 45, cy - 40 + (k // 3) * 40, 22, 0, 2 * math.pi)
                cr.set_source_rgb(*PURPLE); cr.fill()
            cr.rectangle(x + 60, cy - 10, 60, 80); cr.set_source_rgb(*PURPLE); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
        elif lab == "Pencils?":
            for k in range(3):
                cr.save(); cr.translate(x - 60 + k * 60, cy); cr.rotate(-0.3 + k * 0.3)
                cr.rectangle(-12, -90, 24, 180); cr.set_source_rgb(0.22, 0.18, 0.15); cr.fill(); cr.restore()
        else:
            crate(cr, x, cy + 80, 220, 150)
        text(cr, sub, x, 720, 40, TEXT)
        cr.pop_group_to_source()
        cr.save(); cr.translate(x, 530); cr.scale(back_out(p), back_out(p)); cr.translate(-x, -530)
        cr.paint_with_alpha(al * clamp(p * 2)); cr.restore()
        cr.restore()
    pp = prog(t, tp, 0.5)
    if pp > 0:
        for k in range(3):
            pie(cr, 520 + k * 260, 640, 100 * back_out(prog(t, tp + k * 0.25, 0.4)))
        text(cr, "Sweet potato pies,", 780, 400, 72, MAROON, alpha=pp)
        text(cr, "sold to keep the doors open", 780, 480, 46, TEXT, alpha=pp)
    tg = beat(i, "And the girls kept coming")
    pg = prog(t, tg, 0.5)
    if pg > 0:
        cr.set_source_rgba(*BG, pg); cr.paint()
        text(cr, "...and the girls kept coming.", W / 2, 300, 72, MAROON, alpha=pg)
        for k in range(8):
            st = tg + 0.2 + k * 0.18
            pk = prog(t, st, 2.5)
            if pk > 0:
                kid(cr, -100 + 1200 * ease(pk) + k * 110, 900, 0.8,
                    [MAROON, GOLDC, (0.30, 0.45, 0.60), GREEN][k % 4], True, t, walking=pk < 1)
    fade_edges(cr, t, a, b)


def s4(cr, t):
    i = 4
    a, b = scene_bounds(i)
    bg(cr)
    kicker(cr, "WITHIN TWO YEARS", t, a + 0.1)
    t6 = a + 0.4
    tg = beat(i, "two hundred and fifty")
    p = prog(t, tg - 1.5, 2.5)
    n = int(6 + 244 * ease(p))
    text(cr, str(n), 520, 600, 260, MAROON)
    text(cr, "students", 520, 700, 56, TEXT)
    # dot grid of students
    for k in range(n):
        cx = 900 + (k % 25) * 36; cy = 220 + (k // 25) * 50
        cr.arc(cx, cy, 13, 0, 2 * math.pi)
        cr.set_source_rgb(*(GOLDC if k < 6 else BLACK)); cr.fill()
    td = beat(i, "So she knocked on doors")
    pd = prog(t, td, 0.5)
    if pd > 0:
        cr.set_source_rgba(*BG, pd); cr.paint()
        tl = beat(i, "She wrote letters")
        pdoor = 1 - prog(t, tl - 0.2, 0.4)
        if pdoor > 0:  # a door she knocks on
            cr.save(); cr.push_group()
            cr.rectangle(470, 470, 170, 530); cr.set_source_rgb(*BROWN); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
            cr.rectangle(495, 500, 120, 200); cr.rectangle(495, 740, 120, 220); cr.set_line_width(4); cr.stroke()
            cr.arc(615, 740, 9, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill()
            cr.pop_group_to_source(); cr.paint_with_alpha(pdoor); cr.restore()
        knocking = t < tl - 0.2
        mary(cr, 300, 1000, 1.35, t, pose="knock" if knocking else "hold", knock=knocking, letter=not knocking)
        # flying letters
        for k in range(6):
            pk = prog(t, tl + k * 0.3, 1.6)
            if 0 < pk < 1:
                envelope(cr, 500 + 1300 * pk, 600 - 300 * math.sin(pk * math.pi) - k * 25, 0.9, rot=pk * 0.6)
        tgm = beat(i, "James Gamble")
        pg = prog(t, tgm, 0.5)
        if pg > 0:
            panel(cr, 760, 230, 1000, 260, (1, 1, 1), alpha=pg)
            text(cr, "Asked wealthy winter visitors", 1260, 320, 50, TEXT, alpha=pg)
            text(cr, "to invest in her girls,", 1260, 385, 50, TEXT, alpha=pg)
            text(cr, "including James Gamble of Procter & Gamble", 1260, 450, 38, MAROON, alpha=pg)
        tn = beat(i, "Some said no")
        pn = prog(t, tn, 0.35)
        if pn > 0:
            cr.save(); cr.translate(1250, 700); cr.rotate(-0.12); s = 1.6 - 0.6 * ease(pn); cr.scale(s, s)
            rounded_rect(cr, -170, -70, 340, 130, 16)
            cr.set_source_rgba(0.80, 0.15, 0.15, pn); cr.set_line_width(10); cr.stroke()
            text(cr, "NO.", 0, 30, 96, (0.80, 0.15, 0.15), alpha=pn)
            cr.restore()
        tk = beat(i, "She kept asking")
        pk = prog(t, tk, 0.4)
        if pk > 0:
            text(cr, "She kept asking.", 1250, 940, 80, MAROON, alpha=pk, scale=back_out(pk))
    fade_edges(cr, t, a, b)


def s5(cr, t):
    i = 5
    a, b = scene_bounds(i)
    bg(cr, (0.95, 0.91, 0.84), BG2)
    ground(cr, 880)
    kicker(cr, "1923 · THE MERGER", t, a + 0.1)
    tm = beat(i, "merged with the Cookman")
    pm = ease(prog(t, tm + 0.8, 1.6))
    xl = 560 + 260 * pm; xr = 1360 - 260 * pm
    building(cr, xl, 882, 360, 260, (0.95, 0.92, 0.85))
    building(cr, xr, 882, 360, 260, (0.92, 0.88, 0.82))
    if pm < 0.6:
        text(cr, "Daytona school", xl, 940, 38, TEXT, alpha=1 - pm / 0.6)
        text(cr, "girls · 1904", xl, 985, 32, MAROON, alpha=1 - pm / 0.6)
        text(cr, "Cookman Institute", xr, 940, 38, TEXT, alpha=prog(t, tm, 0.4) * (1 - pm / 0.6))
        text(cr, "boys · Jacksonville · 1872", xr, 985, 32, MAROON, alpha=prog(t, tm, 0.4) * (1 - pm / 0.6))
    tg = beat(i, "Girls and boys")
    pg = prog(t, tg, 0.4)
    if pg > 0:
        for k in range(6):
            kid(cr, 700 + k * 100, 880, 0.6, [MAROON, GOLDC][k % 2], girl=k % 2 == 0, t=t)
        text(cr, "Girls and boys, side by side", 960, 300, 60, TEXT, alpha=pg * (1 - prog(t, beat(i, "And in nineteen thirty-one"), 0.4)))
    tn = beat(i, "Bethune-Cookman College")
    t31 = beat(i, "And in nineteen thirty-one")
    p31 = prog(t, t31, 0.4)
    if p31 > 0:
        text(cr, "1931", 960, 260, 110, MAROON, alpha=p31)
    pn = prog(t, tn - 0.4, 0.6)
    if pn > 0:
        cr.save(); cr.translate(960, 420); cr.scale(back_out(pn), back_out(pn))
        rounded_rect(cr, -560, -70, 1120, 120, 20)
        cr.set_source_rgb(*MAROON); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
        text(cr, "BETHUNE-COOKMAN COLLEGE", 0, 22, 68, GOLDC)
        cr.restore()
    fade_edges(cr, t, a, b)


def s6(cr, t):
    i = 6
    a, b = scene_bounds(i)
    bg(cr, (0.90, 0.92, 0.95), (0.95, 0.93, 0.90))
    th = a + 0.1
    ph = prog(t, th, 0.4) * (1 - prog(t, beat(i, "She advised"), 0.4))
    if ph > 0:
        bo(cr, 960, 1000, 0.55, t, pose="shrug", wide=0.7, brow=0.9)
        text(cr, "The part most people never hear...", W / 2, 180, 70, MAROON, alpha=ph)
    tf = beat(i, "She advised")
    tc = beat(i, "She founded the National")
    ts = beat(i, "And in July")
    cards = [("Advised President", "Franklin D. Roosevelt", tf), ("Founded the National", "Council of Negro Women", tc)]
    pcards_out = prog(t, ts - 0.2, 0.4)
    for k, (l1, l2, st) in enumerate(cards):
        p = prog(t, st, 0.5)
        if p <= 0 or pcards_out >= 1:
            continue
        y = 300 + k * 300
        cr.save(); cr.translate(-(1 - ease(p)) * 300, 0)
        panel(cr, 360, y, 1200, 230, (1, 1, 1), alpha=clamp(p * 2) * (1 - pcards_out))
        text(cr, l1, 960, y + 100, 56, TEXT, alpha=clamp(p * 2) * (1 - pcards_out))
        text(cr, l2, 960, y + 175, 64, MAROON, alpha=clamp(p * 2) * (1 - pcards_out))
        cr.restore()
    ps = prog(t, ts, 0.6)
    if ps > 0:
        cr.set_source_rgba(0.90, 0.92, 0.95, ps); cr.paint()
        capitol(cr, 1300, 960, 1.05 * (0.9 + 0.1 * ease(ps)))
        statue(cr, 520, 960, 1.15 * back_out(prog(t, beat(i, "a marble statue"), 0.6)))
        ground(cr, 960, (0.82, 0.80, 0.76))
        text(cr, "JULY 2022 · U.S. CAPITOL", 960, 140, 64, MAROON, alpha=ps)
        tfst = beat(i, "She became the first")
        pf = prog(t, tfst, 0.5)
        if pf > 0:
            panel(cr, 980, 180, 860, 160, (1, 1, 1), alpha=pf)
            text(cr, "First Black American in the", 1410, 250, 46, TEXT, alpha=pf)
            text(cr, "National Statuary Hall Collection", 1410, 310, 46, MAROON, alpha=pf)
        tr = beat(i, "Her statue replaced")
        pr = prog(t, tr, 0.5)
        if pr > 0:
            text(cr, "...replacing a Confederate general.", 960, 1040, 48, TEXT, alpha=pr)
    fade_edges(cr, t, a, b)


def s7(cr, t):
    i = 7
    a, b = scene_bounds(i)
    bg(cr)
    ground(cr, 860)
    house(cr, 330, 862, 0.7)
    capitol(cr, 1550, 862, 0.75)
    p = ease(prog(t, a + 0.3, (b - a) * 0.55))
    cr.set_source_rgb(*GOLDC); cr.set_line_width(12); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    N = 60
    cr.move_to(450, 700)
    for k in range(1, int(N * p) + 1):
        u = k / N
        cr.line_to(450 + 800 * u, 700 - 380 * math.sin(u * math.pi))
    cr.stroke()
    if p > 0:
        u = p
        coin(cr, 450 + 800 * u, 700 - 380 * math.sin(u * math.pi), 70, spin=t * 3)
    tl = beat(i, "And all of it started")
    pl = prog(t, tl, 0.5)
    if pl > 0:
        text(cr, "It all started with", W / 2, 160, 64, TEXT, alpha=pl)
        text(cr, "$1.50", W / 2, 290, 140, MAROON, alpha=pl, scale=back_out(pl))
    fade_edges(cr, t, a, b)


def s8(cr, t):
    i = 8
    a, b = scene_bounds(i)
    bg(cr, SKY, BG)
    ground(cr, 880, (0.62, 0.74, 0.50))
    building(cr, 1050, 882, 700, 300, (0.95, 0.92, 0.85), cols=5)
    text(cr, "BETHUNE-COOKMAN UNIVERSITY", 1050, 180, 60, MAROON, alpha=prog(t, a + 0.2, 0.5))
    for k in range(4):
        kid(cr, 600 + k * 260 + math.sin(t + k) * 20, 1010, 0.75, [MAROON, GOLDC][k % 2], girl=k % 2 == 0, t=t)
    bo(cr, 260, 1040, 0.5, t, pose="point" if t < beat(i, "So the next time") else "pockets", talk=True)
    tm = beat(i, "Enter to learn")
    pm = prog(t, tm, 0.5)
    pd = prog(t, beat(i, "Depart to serve"), 0.5)
    tn = beat(i, "So the next time")
    pn = prog(t, tn, 0.5)
    if pm > 0:
        a1 = 1 - pn
        panel(cr, 560, 250, 980, 150, MAROON, alpha=pm * a1)
        text(cr, "ENTER TO LEARN.", 1050, 345, 64, GOLDC, alpha=pm * a1, align="center")
    if pd > 0:
        text(cr, "DEPART TO SERVE.", 1050, 470, 64, MAROON, alpha=pd * (1 - pn), outline=(1, 1, 1))
    if pn > 0:
        cr.set_source_rgba(*MAROON, 0.92 * pn); cr.paint()
        text(cr, "Don't have enough to start?", W / 2, 440, 76, (1, 1, 1), alpha=pn)
        pop_text(cr, "Remember Mary.", W / 2, 600, 130, t, beat(i, "remember Mary"), color=GOLDC)
    fade_edges(cr, t, a, b)


def s9(cr, t):
    i = 9
    a, b = scene_bounds(i)
    bg(cr)
    bo(cr, 420, 1020, 0.6, t, pose="pockets", pose_to="wave", pose_t=prog(t, a + 0.2, 0.5), talk=t < P[i][1])
    text(cr, "Which H-B-C-U founder", 1220, 330, 70, TEXT, alpha=prog(t, a + 0.2, 0.5))
    text(cr, "should we cover next?", 1220, 420, 70, MAROON, alpha=prog(t, a + 0.4, 0.5))
    pop_text(cr, "Tell us in the comments", 1220, 540, 48, t, beat(i, "Tell us"))
    subscribe_btn(cr, 1220, 720, t, beat(i, "subscribe"))
    pop_text(cr, "THE YARD", 1220, 900, 64, t, beat(i, "The Yard"), color=GOLDC, outline=INK)
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()


SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]
