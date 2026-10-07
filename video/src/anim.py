exec(open('/tmp/claude-0/-home-user-my-first-web/8891a5da-addd-5ba1-85e5-1a0c00e5c0f4/scratchpad/bl/scene.py').read())
FPS_R = 10
PLUG = rbox('plug', (0.022, 0.008, 0.008), 0.0025, M_WHITE); ALL.append(PLUG)
# mannequin base
base = cyl('mbase', 0.12, 0.02, M_GREY, 64); base.location = (0, 0, -0.26); parent(base, MAN)
MANX = -0.14; MANC = V(MANX, 0.0, 0.27)

def orient(n, up=V(0, 0, 1)):
    n = n.normalized(); y = up - n * up.dot(n)
    if y.length < 1e-4: y = V(0, 1, 0)
    y.normalize(); x = y.cross(n).normalized(); y = n.cross(x)
    m = Matrix(((x.x, y.x, n.x), (x.y, y.y, n.y), (x.z, y.z, n.z))); return m.to_euler()
def chest_pt(xr, zr):
    y = chest_y(xr, zr); p = V(MANC.x + xr, MANC.y + y, MANC.z + zr)
    n = V(xr / CH[0] ** 2, y / CH[1] ** 2, zr / CH[2] ** 2).normalized(); return p, n
def pop(o, t, t0, loc, rot=None, dur=0.7, rise=0.12):
    k = ease((t - t0) / dur); vis(o, t >= t0)
    if t >= t0:
        o.location = V(loc.x, loc.y, loc.z + (1 - k) * rise); o.scale = (max(k, 0.01),) * 3
        if rot is not None: o.rotation_euler = rot
def cable_pts(P, F, i, sag=0.012):
    d = F - P; side = V(0, 0.0, 1)
    a = P + d * 0.0 + V(0, (i - 1.5) * 0.004, 0.003)
    b = P + d * 0.33 + V(0, (i - 1.5) * 0.006, sag * 1.0)
    c = P + d * 0.66 + V(0, (i - 1.5) * 0.003, sag * 0.8)
    return [a, b, c, F]
TABLET_POS = V(0.20, 0.06, 0)
def tablet_pose(flat=False):
    th = math.radians(65)
    if flat: return V(0, 0.03, 0.0047), Euler((0, 0, 0))
    z = 0.0975 * math.sin(th) + 0.003; return V(TABLET_POS.x, TABLET_POS.y + 0.0975 * math.cos(th) * 0.0, z), Euler((th, 0, 0))
def tablet_screen_pt(u, v, flat=False):
    loc, rot = tablet_pose(flat); m = Matrix.Translation(loc) @ rot.to_matrix().to_4x4()
    return m @ V(u * 0.282, v * 0.168, 0.0062)

def frame(t):
    hide_all(); vis(floor, True); vis(wall, True); RING.hide_render = True
    set_led(MOD, '#777777', 0.0)
    if t < 3:  # A title
        vis(MOD, True); setxf(MOD, V(0, 0, 0.085 + 0.006 * math.sin(t * 2)), Euler((math.radians(70), 0, math.radians(-25 + t * 18))), 1.0)
        set_led(MOD, '#3CB7FF', 3.0); look(V(0.0, -0.38, 0.11), V(0, 0, 0.08), 55)
    elif t < 12:  # B components
        lt = t - 3
        pop(MOD, t, 3.3, V(-0.20, 0.0, 0.00625), Euler((0, 0, math.radians(-8))))
        pop(CRA, t, 4.8, V(-0.08, 0.0, 0.007), Euler((0, 0, 0)))
        pop(HOL, t, 6.2, V(0.03, 0.06, 0.0035), Euler((0, 0, 0)))
        pop(PAT, t, 6.8, V(0.07, -0.05, 0.0006), Euler((0, 0, 0)))
        if t >= 8.2:
            for i, e in enumerate(ELS):
                t0 = 8.2 + i * 0.25; pop(e, t, t0, V(-0.22 + i * 0.065, -0.14, 0.0006), Euler((0, 0, 0)), 0.5, 0.08)
                vis(CAB[i], t >= t0 + 0.4)
                set_cable(CAB[i], cable_pts(V(-0.01, -0.095, 0.004), V(-0.22 + i * 0.065, -0.14, 0.006 + 0.0025), i, 0.01))
            vis(PLUG, True); setxf(PLUG, V(-0.01, -0.095, 0.0045), Euler((0, 0, 0)), 1.0)
        if t >= 10.0:
            vis(CHG, True); set_cable(CHG, [V(-0.08, -0.058, 0.0035), V(-0.06, -0.10, 0.003), V(0.0, -0.20, 0.003), V(0.1, -0.2, 0.003), V(0.18, -0.15, 0.003)])
            vis(CRA, True)
        ang = lt / 9; look(V(0.0 + math.sin(ang * 0.6) * 0.1, -0.52 + 0.04 * ang, 0.36), V(-0.04, -0.03, 0.0), 44)
    elif t < 19:  # C charging
        lt = t - 12; vis(CRA, True); vis(MOD, True); vis(CHG, True)
        setxf(CRA, V(0, 0, 0.007), Euler((0, 0, 0)), 1.0)
        set_cable(CHG, [V(0, -0.0565, 0.0035), V(0.0, -0.1, 0.003), V(0.07, -0.14, 0.003), V(0.15, -0.12, 0.003)])
        mz = kf(lt, [(0.8, 0.14), (2.6, 0.0225), (3.0, 0.0165), (3.3, 0.0175), (3.6, 0.0165)])
        setxf(MOD, V(0, 0.012, mz), Euler((0, 0, 0)), 1.0)
        set_led(MOD, '#FF9A1F' if 3.6 <= lt < 5.8 else ('#34C76B' if lt >= 5.8 else '#777777'), 4.0 if lt >= 3.6 else 0.0)
        look(kf(lt, [(0, V(0.12, -0.30, 0.17)), (7, V(-0.04, -0.26, 0.13))]), V(0.0, 0.0, 0.02), 50)
    elif t < 23:  # D app
        lt = t - 19; vis(TAB, True); loc, rot = tablet_pose(True); setxf(TAB, loc + V(0, 0, (1 - ease(lt / 0.8)) * 0.1), rot, max(ease(lt / 0.8), 0.01)); set_screen(TAB, 'login')
        look(V(0.0, -0.40, 0.36), V(0, 0.03, 0), 48)
    elif t < 35:  # E assembly
        lt = t - 23; PO = V(0.07, 0, 0.0006)
        vis(PAT, True); setxf(PAT, PO, Euler((0, 0, 0)), 1.0)
        liner = bpy.data.objects[PAT['liner']]
        pk = ease((lt - 4.0) / 2.5); lp = lt < 7.0
        liner.hide_render = not (lp and lt < 7.0)
        if lt >= 4.0: liner.location = (0.0 + pk * 0.05, 0, 0.0006 + pk * 0.09); liner.rotation_euler = (0, -pk * 1.0, 0)
        else: liner.location = (0, 0, 0.0006); liner.rotation_euler = (0, 0, 0)
        F = [V(-0.13, 0.09, 0.0006), V(-0.13, 0.03, 0.0006), V(-0.13, -0.03, 0.0006), V(-0.13, -0.09, 0.0006)]
        S0 = [V(0.12, -0.12, 0.0006), V(0.17, -0.1, 0.0006), V(0.22, -0.09, 0.0006), V(0.27, -0.1, 0.0006)]
        P0 = V(-0.06, 0.035, 0.005); PE = V(0.0095, 0.026, 0.0078)
        pp = kf(lt, [(7.2, P0), (7.8, P0 + V(0, 0, 0.03)), (8.9, PE + V(-0.05, 0, 0.03)), (9.7, PE + V(-0.012, 0, 0.0)), (10.2, PE)])
        for i, e in enumerate(ELS):
            vis(e, True); ts = 0.4 + i * 0.9
            pos = kf(lt, [(ts, S0[i]), (ts + 0.4, S0[i] + V(0, 0, 0.05)), (ts + 1.0, F[i] + V(0, 0, 0.05)), (ts + 1.3, F[i])])
            setxf(e, pos, Euler((0, 0, 0)), 1.0); vis(CAB[i], True)
            tip = F[i] + V(0, 0, 0.0045 + 0.0035)
            set_cable(CAB[i], cable_pts(pp, tip, i, 0.014))
        vis(PLUG, True); setxf(PLUG, pp, Euler((0, 0, 0)), 1.0)
        # holder
        vis(HOL, True); hz = kf(lt, [(5.4, 0.07), (6.6, 0.0047 + 0.0006 + 0.0012)])
        hp = V(0.07, 0, hz) if lt >= 5.4 else V(0.07, 0, 0.08)
        if lt < 5.4: vis(HOL, False)
        else: setxf(HOL, hp, Euler((0, 0, 0)), 1.0)
        if lt >= 11.0:
            vis(MOD, True); mp = V(0.07, 0, 0.075 + 0.004 * math.sin(lt * 3)); setxf(MOD, mp, Euler((0, 0, 0)), 1.0); set_led(MOD, '#777777', 0)
        look(kf(lt, [(0, V(0.0, -0.30, 0.42)), (12, V(0.03, -0.24, 0.34))]), V(0.0, 0.0, 0.0), 44)
    elif t < 46:  # F attach
        lt = t - 35; vis(MAN, True); setxf(MAN, MANC, Euler((0, 0, 0)), 1.0)
        pc, pn = chest_pt(-0.01, -0.01); prot = orient(pn, V(0, 0, 1))
        k = ease((lt - 0.3) / 2.4)
        hover = V(MANX + 0.12, -0.34, 0.14)
        ppos = lerpV(hover, pc + pn * 0.0008, k); vis(PAT, True); setxf(PAT, ppos, prot if k > 0.01 else Euler((math.pi / 2, 0, 0)), 1.0)
        PAT['liner'] and (bpy.data.objects[PAT['liner']].__setattr__('hide_render', True))
        # holder rides on patch
        pm = Matrix.Translation(ppos) @ prot.to_matrix().to_4x4(); vis(HOL, True)
        hm = pm @ Matrix.Translation(V(0, 0, 0.0047 + 0.0012)); HOL.matrix_world = hm
        jack = pm @ V(-0.0505 + 0.0, 0.026, 0.0083)
        PL = pm @ V(-0.0505 - 0.010, 0.026, 0.0083); vis(PLUG, True)
        PLUG.matrix_world = pm @ Matrix.Translation(V(-0.0605, 0.026, 0.0083))
        targets = [chest_pt(-0.125, 0.13), chest_pt(0.125, 0.13), chest_pt(-0.10, -0.16), chest_pt(0.10, -0.16)]
        for i, e in enumerate(ELS):
            ts = 3.2 + i * 1.1; kk = ease((lt - ts) / 0.9)
            tp, tn = targets[i]; start = pm @ V(0.06 + i * 0.03, -0.01, 0.05)
            mid = lerpV(start, tp + tn * 0.0012, kk) + V(0, -0.04 * math.sin(kk * math.pi), 0.03 * math.sin(kk * math.pi))
            vis(e, True); e.location = mid if lt >= ts else start; e.rotation_euler = orient(tn if kk > 0.5 else tn.lerp(V(0, -1, 0), 0.0))
            e.scale = (1, 1, 1); vis(CAB[i], True)
            tip = (mid if lt >= ts else start) + tn * 0.0062 if kk > 0 else start + V(0, -0.005, 0.003)
            PLp = PLUG.matrix_world.translation
            pts = cable_pts(PLp, tip, i, 0.02)
            # make cable bow outward from chest
            pts = [pts[0], pts[1] + pn * 0.012, pts[2] + pn * 0.012, pts[3]]
            set_cable(CAB[i], pts)
        # module snap
        vis(MOD, lt >= 8.2)
        if lt >= 8.2:
            mk = ease((lt - 8.2) / 1.2); seat = pm @ V(0, 0, 0.0083 + 0.00625 + 0.0012 - 0.0012)
            mp = lerpV(pm @ V(0.02, 0.0, 0.09), seat, mk)
            if lt > 9.5: mp = seat + (pm.to_3x3() @ V(0, 0, -0.0012 * math.sin(clamp((lt - 9.5) / 0.4) * math.pi)))
            MOD.location = mp; MOD.rotation_euler = prot; MOD.scale = (1, 1, 1)
            set_led(MOD, '#2D9CDB' if int(lt * 3) % 2 else '#1A6FA5', 4.0) if lt > 9.6 else set_led(MOD, '#777777', 0)
        look(kf(lt, [(0, V(MANX + 0.10, -0.95, 0.34)), (6, V(MANX + 0.04, -0.82, 0.32)), (11, V(MANX, -0.70, 0.31))]), V(MANX, 0, 0.27), 50)
    else:
        # shared kit on mannequin for G/H/I
        vis(MAN, True); setxf(MAN, MANC, Euler((0, 0, 0)), 1.0)
        pc, pn = chest_pt(-0.01, -0.01); prot = orient(pn, V(0, 0, 1)); pm = Matrix.Translation(pc + pn * 0.0008) @ prot.to_matrix().to_4x4()
        vis(PAT, True); setxf(PAT, pc + pn * 0.0008, prot, 1.0); bpy.data.objects[PAT['liner']].hide_render = True
        vis(HOL, True); HOL.matrix_world = pm @ Matrix.Translation(V(0, 0, 0.0059)); vis(PLUG, True); PLUG.matrix_world = pm @ Matrix.Translation(V(-0.0605, 0.026, 0.0083))
        targets = [chest_pt(-0.125, 0.13), chest_pt(0.125, 0.13), chest_pt(-0.10, -0.16), chest_pt(0.10, -0.16)]
        for i, e in enumerate(ELS):
            tp, tn = targets[i]; vis(e, True); e.location = tp + tn * 0.0012; e.rotation_euler = orient(tn); e.scale = (1, 1, 1); vis(CAB[i], True)
            PLp = PLUG.matrix_world.translation; pts = cable_pts(PLp, tp + tn * 0.0062, i, 0.02); set_cable(CAB[i], [pts[0], pts[1] + pn * 0.012, pts[2] + pn * 0.012, pts[3]])
        seat = pm @ V(0, 0, 0.0083 + 0.00625)
        vis(TAB, True); tloc, trot = tablet_pose(False); setxf(TAB, tloc, trot, 1.0)
        if t < 60:  # G
            lt = t - 46; vis(MOD, True); MOD.location = seat; MOD.rotation_euler = prot; MOD.scale = (1, 1, 1)
            scr = 'login' if lt < 2.5 else ('connect' if lt < 6 else ('electrode-check' if lt < 8.5 else 'live')); set_screen(TAB, scr)
            blink = '#2D9CDB' if int(lt * 3) % 2 else '#1A6FA5'
            set_led(MOD, blink if lt < 8.5 else '#34C76B', 4.0)
            taps = [(1.5, 0.0, -0.18), (3.6, 0.37, 0.36), (5.4, 0.46, 0.36)]
            RING.hide_render = True
            for tt, u, v in taps:
                d = lt - tt
                if 0 < d < 0.8:
                    RING.hide_render = False; RING.location = tablet_screen_pt(u, v) + V(0, -0.002, 0.0); RING.rotation_euler = Euler((math.radians(90) - tloc.z * 0 + (math.radians(-65) + math.radians(90)) * 0, 0, 0))
                    RING.rotation_euler = trot; RING.scale = (1 + d * 3,) * 3
            look(kf(lt, [(0, V(-0.02, -1.15, 0.34)), (14, V(0.02, -1.0, 0.28))]), V(0.03, 0.0, 0.2), 40)
        elif t < 70:  # H
            lt = t - 60; vis(MOD, True); MOD.location = seat; MOD.rotation_euler = prot; MOD.scale = (1, 1, 1); set_led(MOD, '#34C76B', 4.0)
            scr = 'beats' if lt < 2.8 else ('trend' if lt < 5.4 else ('review' if lt < 7.6 else 'pdf')); set_screen(TAB, scr)
            look(kf(lt, [(0, V(0.02, -1.0, 0.28)), (10, V(0.19, -0.50, 0.17))]), V(0.17, 0.05, 0.1), 40)
        else:  # I
            lt = t - 70
            vis(CRA, True); setxf(CRA, V(0.0, -0.20, 0.007), Euler((0, 0, 0)), 1.0); vis(CHG, True)
            set_cable(CHG, [V(0.0, -0.2605, 0.0035), V(0.0, -0.3, 0.003), V(0.07, -0.34, 0.003), V(0.15, -0.32, 0.003)])
            dock = V(0.0, -0.20 + 0.012, 0.0165)
            if lt < 0.8: mp = seat; mr = prot
            else:
                a = seat; b = dock
                kk = ease((lt - 0.8) / 3.4); mp = lerpV(a, b, kk) + V(0, -0.06 * math.sin(kk * math.pi), 0.10 * math.sin(kk * math.pi)); mr = Euler((lerp(prot.x, 0, kk), lerp(prot.y, 0, kk), lerp(prot.z, 0, kk)))
            vis(MOD, True); MOD.location = mp; MOD.rotation_euler = mr; MOD.scale = (1, 1, 1)
            set_led(MOD, '#FF9A1F' if lt > 4.4 else '#34C76B', 4.0)
            set_screen(TAB, 'pdf')
            look(kf(lt, [(0, V(0.19, -0.5, 0.17)), (3, V(0.05, -0.8, 0.28)), (8, V(0.0, -1.1, 0.38))]), kf(lt, [(0, V(0.17, 0.05, 0.1)), (3, V(0.0, -0.1, 0.12)), (8, V(0.0, -0.12, 0.12))]), 42)

if __name__ == '__main__':
    import time
    idxs = [int(a) for a in sys.argv[sys.argv.index('--') + 1:]] if '--' in sys.argv else []
    os.makedirs(os.environ.get('OUT', '/tmp/blf'), exist_ok=True)
    for i in idxs:
        t = i / FPS_R; frame(t); scn.render.filepath = f"{os.environ.get('OUT', '/tmp/blf')}/f_{i:05d}.png"
        t0 = time.time(); bpy.ops.render.render(write_still=True); print('FRAME', i, round(time.time() - t0, 1), flush=True)
