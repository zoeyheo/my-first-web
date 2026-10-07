import bpy, bmesh, math, sys, os, json
import numpy as np
from mathutils import Vector, Euler, Matrix, Quaternion

IMG = '/tmp/claude-0/-home-user-my-first-web/8891a5da-addd-5ba1-85e5-1a0c00e5c0f4/scratchpad/img/'
W, H = 1280, 720
V = lambda x=0, y=0, z=0: Vector((x, y, z))
def clamp(x, a=0.0, b=1.0): return min(b, max(a, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def lerp(a, b, t): return a + (b - a) * t
def lerpV(a, b, t): return a.lerp(b, t)
def kf(t, frames):
    if t <= frames[0][0]: return frames[0][1].copy() if hasattr(frames[0][1], 'copy') else frames[0][1]
    for i in range(1, len(frames)):
        if t <= frames[i][0]:
            t0, a = frames[i - 1]; t1, b = frames[i]; k = ease((t - t0) / (t1 - t0))
            return a.lerp(b, k) if hasattr(a, 'lerp') else lerp(a, b, k)
    l = frames[-1][1]; return l.copy() if hasattr(l, 'copy') else l

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
scn.render.engine = os.environ.get('ENGINE','CYCLES')
cy = scn.cycles
cy.device = 'CPU'; cy.samples = int(os.environ.get('SAMPLES', 24)); cy.use_denoising = True
cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 3; cy.transmission_bounces = 2
scn.render.resolution_x = W; scn.render.resolution_y = H; scn.render.resolution_percentage = int(os.environ.get('PCT', 100))
scn.render.image_settings.file_format = 'PNG'; scn.render.image_settings.color_mode = 'RGB'
scn.render.threads_mode = 'FIXED'; scn.render.threads = int(os.environ.get('THREADS', 1))
scn.view_settings.view_transform = 'Filmic' if 'Filmic' in [i.identifier for i in scn.view_settings.bl_rna.properties['view_transform'].enum_items] else 'AgX'
try: scn.view_settings.look = 'None'
except Exception: pass

def mat(name, color, rough=0.4, metal=0.0, emit=None, es=1.0, alpha=1.0, spec=0.5, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; n = m.node_tree.nodes; b = n['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if 'Coat Weight' in b.inputs: b.inputs['Coat Weight'].default_value = coat
    if emit is not None:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = es
    if alpha < 1: b.inputs['Alpha'].default_value = alpha
    return m
def hexc(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92
    return (f(r), f(g), f(b))

def link(o): scn.collection.objects.link(o); return o
def smooth(o, ang=35):
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    try: bpy.ops.object.shade_smooth_by_angle(angle=math.radians(ang))
    except Exception:
        for p in o.data.polygons: p.use_smooth = True
    o.select_set(False)
def rbox(name, size, r, material):
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.active_object; o.name = name; o.scale = Vector(size)
    bpy.ops.object.transform_apply(scale=True)
    m = o.modifiers.new('bv', 'BEVEL'); m.width = r; m.segments = 5; m.limit_method = 'ANGLE'
    bpy.ops.object.modifier_apply(modifier='bv'); smooth(o); o.data.materials.append(material); return o
def cyl(name, r, h, material, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=verts); o = bpy.context.active_object; o.name = name
    smooth(o, 40); o.data.materials.append(material); return o
def parent(child, par): child.parent = par; child.matrix_parent_inverse = par.matrix_world.inverted()
def empty(name): o = bpy.data.objects.new(name, None); link(o); return o

M_WHITE = mat('white', hexc('#F4F7FA'), 0.28, coat=0.3); M_GREY = mat('grey', hexc('#E3E9EF'), 0.4); M_DARK = mat('dark', hexc('#1E242B'), 0.4)
M_BLUE = mat('cradle', hexc('#9FCFEC'), 0.35, coat=0.2); M_BLUE2 = mat('cradle2', hexc('#7FB8DE'), 0.4); M_TXT = mat('txt', hexc('#3C9FD9'), 0.3, emit=hexc('#3C9FD9'), es=0.4)
M_CABLE = mat('cable', hexc('#F2F4F6'), 0.45); M_PATCH = mat('patch', hexc('#F5F7F9'), 0.5); M_PAD = mat('pad', hexc('#EEF1F4'), 0.7)
M_FLOOR = mat('floor', hexc('#9FB6CC'), 0.5, spec=0.4); M_MAN = mat('mannequin', hexc('#AEBBC8'), 0.5)
LEDM = mat('led', hexc('#888888'), 0.3, emit=hexc('#888888'), es=3.0)
SNAP = {n: mat('snap' + n, hexc(c), 0.35) for n, c in {'RA': '#F6F6F6', 'LA': '#1D2128', 'RL': '#2F9E68', 'LL': '#D8453D'}.items()}

# ---------- world / lights / floor ----------
w = bpy.data.worlds.new('w'); scn.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.74, 0.84, 0.95, 1); bg.inputs['Strength'].default_value = 0.85
bpy.ops.mesh.primitive_plane_add(size=14); floor = bpy.context.active_object; floor.data.materials.append(M_FLOOR)
bpy.ops.mesh.primitive_plane_add(size=14); wall = bpy.context.active_object; wall.rotation_euler = (math.radians(90), 0, 0); wall.location = (0, 1.0, 3.0); wall.data.materials.append(M_FLOOR)
def area(name, loc, target, size, energy, color=(1, 1, 1)):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.size = size; l.color = color; o = bpy.data.objects.new(name, l); link(o); o.location = loc
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o
area('key', (-0.9, -1.0, 1.5), (0, 0, 0), 1.6, 100, (1.0, 0.98, 0.95))
area('fill', (1.4, -0.8, 0.9), (0, 0, 0), 2.0, 40, (0.9, 0.95, 1.0))
area('rim', (0.2, 1.4, 1.2), (0, 0, 0), 1.2, 70, (0.85, 0.93, 1.0))
camd = bpy.data.cameras.new('cam'); camd.lens = 50; camd.sensor_width = 36; camd.dof.use_dof = False
cam = bpy.data.objects.new('cam', camd); link(cam); scn.camera = cam
def look(loc, tgt, lens=50, roll=0):
    cam.location = loc; d = Vector(tgt) - Vector(loc); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens

# ---------- product models ----------
def make_module():
    root = empty('module')
    b = rbox('mbody', (0.060, 0.075, 0.0125), 0.0035, M_WHITE); parent(b, root)
    for sx in (-1, 1):
        s = rbox('mbtn', (0.0035, 0.018, 0.0065), 0.0012, M_GREY); s.location = (sx * 0.0305, 0.0, 0.0); parent(s, root)
    cu = bpy.data.curves.new('mtxt', 'FONT'); cu.body = 'CARDIO EM'; cu.size = 0.0062; cu.extrude = 0.00015; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    t = bpy.data.objects.new('mtxt', cu); link(t); t.location = (0, 0.006, 0.00635); t.data.materials.append(M_TXT); parent(t, root)
    led = rbox('led', (0.009, 0.0016, 0.0008), 0.0003, LEDM); led.location = (0, -0.017, 0.0064); parent(led, root)
    root['led'] = led.name; return root
def set_led(module, color, strength=3.0):
    led = bpy.data.objects[module['led']]
    m = led.data.materials[0]; b = m.node_tree.nodes['Principled BSDF']; c = hexc(color)
    b.inputs['Base Color'].default_value = (*c, 1); b.inputs['Emission Color'].default_value = (*c, 1); b.inputs['Emission Strength'].default_value = strength
def make_cradle():
    root = empty('cradle')
    a = rbox('cb', (0.080, 0.122, 0.014), 0.005, M_BLUE); parent(a, root)
    d = rbox('dock', (0.066, 0.086, 0.0035), 0.0015, M_BLUE2); d.location = (0, 0.012, 0.0085); parent(d, root)
    for sx in (-1, 1):
        r = rbox('rib', (0.0035, 0.07, 0.0045), 0.0012, M_BLUE); r.location = (sx * 0.0345, 0.012, 0.0095); parent(r, root)
    p = rbox('port', (0.016, 0.006, 0.006), 0.001, M_DARK); p.location = (0, -0.0605, 0.0); parent(p, root)
    return root
def make_holder():  # holder with jack
    root = empty('holder')
    b = rbox('hb', (0.068, 0.084, 0.007), 0.003, M_GREY); parent(b, root)
    j = rbox('jack', (0.020, 0.022, 0.014), 0.004, M_WHITE); j.location = (-0.040, 0.026, 0.003); parent(j, root)
    h = cyl('hole', 0.0045, 0.002, M_DARK, 24); h.rotation_euler = (0, math.radians(90), 0); h.location = (-0.0505, 0.026, 0.003); parent(h, root)
    for sx in (-1, 1):
        k = rbox('post', (0.004, 0.012, 0.004), 0.001, M_WHITE); k.location = (sx * 0.027, -0.03, 0.0055); parent(k, root)
    return root
def patch_outline():
    pts = []
    def arc(cx, cy, r, a0, a1, n=8):
        for i in range(n + 1): a = math.radians(lerp(a0, a1, i / n)); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    bw, bh, r = 0.058, 0.052, 0.012
    arc(-bw + r, -bh + r, r, 180, 270); arc(bw - r, -bh + r, r, 270, 360, 4)
    pts.append((bw + 0.01, -0.020)); th = 0.021; L = 0.24
    pts.append((L, -th)); arc(L, 0, th, -90, 90, 10); pts.append((bw + 0.01, 0.020))
    arc(bw - r, bh - r, r, 0, 90, 4); arc(0.03, bh + 0.004, 0.012, 0, 180, 8); arc(-0.002, bh + 0.004, 0.012, 0, 180, 8)
    arc(-bw + r, bh - r, r, 90, 180)
    return pts
def make_patch():
    root = empty('patch'); pts = patch_outline()
    me = bpy.data.meshes.new('pm'); bm = bmesh.new(); vs = [bm.verts.new((x, y, 0)) for x, y in pts]
    bm.faces.new(vs); bm.normal_update(); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('pbody', me); link(o); sol = o.modifiers.new('s', 'SOLIDIFY'); sol.thickness = 0.0012; sol.offset = 1
    bv = o.modifiers.new('bv', 'BEVEL'); bv.width = 0.0004; bv.segments = 2
    o.data.materials.append(M_PATCH); parent(o, root)
    liner = bpy.data.meshes.new('lm'); bm = bmesh.new(); vs = [bm.verts.new((x, y, 0)) for x, y in [(0, -0.056), (0.25, -0.056), (0.25, 0.056), (0, 0.056)]]
    bm.faces.new(vs); bm.to_mesh(liner); bm.free(); lo = bpy.data.objects.new('liner', liner); link(lo)
    lm = mat('liner', hexc('#BFD9EE'), 0.3, alpha=0.5); lm.blend_method = 'BLEND' if hasattr(lm, 'blend_method') else None; lo.data.materials.append(lm); lo.location = (0.0, 0, 0.0006); parent(lo, root)
    root['liner'] = lo.name; return root
def make_electrode(name):
    root = empty('el' + name)
    pad = cyl('pad', 0.0185, 0.0012, M_PAD, 40); parent(pad, root)
    sn = cyl('snap', 0.0065, 0.0042, SNAP[name], 32); sn.location = (0, 0, 0.0025); parent(sn, root)
    return root
def make_cable(color=M_CABLE, r=0.0017):
    cu = bpy.data.curves.new('cab', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 3; cu.resolution_u = 4
    sp = cu.splines.new('POLY'); sp.points.add(39); o = bpy.data.objects.new('cable', cu); link(o); o.data.materials.append(color); return o
def set_cable(o, pts):
    p = np.array([list(v) for v in pts]); n = len(p); N = 40
    def cr(t):
        t = t * (n - 1); i = min(int(t), n - 2); u = t - i
        p0 = p[max(i - 1, 0)]; p1 = p[i]; p2 = p[i + 1]; p3 = p[min(i + 2, n - 1)]
        return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)
    sp = o.data.splines[0]
    for i in range(N): q = cr(i / (N - 1)); sp.points[i].co = (q[0], q[1], q[2], 1)
def make_tablet():
    root = empty('tablet')
    b = rbox('tb', (0.30, 0.195, 0.009), 0.007, M_DARK); parent(b, root)
    bpy.ops.mesh.primitive_plane_add(size=1); s = bpy.context.active_object; s.name = 'screen'
    m = bpy.data.materials.new('scr'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tex = nt.nodes.new('ShaderNodeTexImage'); em = nt.nodes.new('ShaderNodeEmission'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    em.inputs['Strength'].default_value = 2.6; nt.links.new(tex.outputs['Color'], em.inputs['Color']); nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    s.data.materials.append(m); s.location = (0, 0, 0.00455); parent(s, root); root['screen'] = s.name; root['tex'] = tex.name
    st = bpy.data.objects.new('standleg', None)
    return root
IMGS = {}
for n in ['login', 'connect', 'electrode-check', 'live', 'review', 'pdf', 'beats', 'trend']:
    IMGS[n] = bpy.data.images.load(IMG + n + '.jpg'); IMGS[n].colorspace_settings.name = 'sRGB'
def set_screen(tab, name):
    s = bpy.data.objects[tab['screen']]; tex = s.data.materials[0].node_tree.nodes[tab['tex']]; tex.image = IMGS[name]
    iw, ih = IMGS[name].size; asp = iw / ih; maxw, maxh = 0.282, 0.168
    if asp > maxw / maxh: sw, sh = maxw, maxw / asp
    else: sw, sh = maxh * asp, maxh
    s.scale = (sw, sh, 1)
def make_charge_cable(): return make_cable(M_DARK, 0.0025)
def make_ring():
    bpy.ops.mesh.primitive_torus_add(major_radius=0.012, minor_radius=0.0012, major_segments=40, minor_segments=8); o = bpy.context.active_object; o.name = 'ring'
    m = mat('ring', hexc('#5CC8FF'), 0.3, emit=hexc('#5CC8FF'), es=8.0); o.data.materials.append(m); o.rotation_euler = (math.radians(90), 0, 0); return o
def make_mannequin():
    root = empty('man')
    def sph(name, sc, loc):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1); o = bpy.context.active_object; o.name = name; o.scale = sc; o.location = loc
        smooth(o, 80); o.data.materials.append(M_MAN); parent(o, root); return o
    sph('chest', (0.19, 0.105, 0.25), (0, 0, 0))
    return root
CH = (0.19, 0.105, 0.25)
def chest_y(x, z): return -CH[1] * math.sqrt(max(1 - (x / CH[0]) ** 2 - (z / CH[2]) ** 2, 0.02))

MOD = make_module(); CRA = make_cradle(); HOL = make_holder(); PAT = make_patch(); TAB = make_tablet(); CHG = make_charge_cable(); RING = make_ring(); MAN = make_mannequin()
ELN = ['RA', 'LA', 'RL', 'LL']; ELS = [make_electrode(n) for n in ELN]; CAB = [make_cable() for _ in ELN]
set_screen(TAB, 'login')
ALL = [MOD, CRA, HOL, PAT, TAB, CHG, RING, MAN] + ELS + CAB
def descendants(o):
    out = [o]
    for c in o.children: out += descendants(c)
    return out
def vis(o, v):
    for d in descendants(o): d.hide_render = not v; d.hide_viewport = not v
def hide_all():
    for o in ALL: vis(o, False)
def setxf(o, loc=None, rot=None, sc=None):
    if loc is not None: o.location = loc
    if rot is not None: o.rotation_euler = rot
    if sc is not None: o.scale = (sc, sc, sc) if isinstance(sc, (int, float)) else sc
