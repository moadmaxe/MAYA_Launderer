
import maya.cmds as cmds
import maya.mel as mel
import random

class MayaLaundererGodMode:
    def __init__(self):
        self.window_name = "launderer_god_ui"
        self.icons = {
            "cube": "polyCube.png",
            "cyl": "polyCylinder.png",
            "sphere": "polySphere.png",
            "plane": "polyMesh.png",
            "cone": "polyCone.png",
            "torus": "polyTorus.png",
            "group": "group.png",
            "locator": "locator.png",
            "curve": "curveEP.png",
            "camera": "Camera.png",
            "light": "spotlight.png"
        }

    def create_ui(self):
        # 1. CLEANUP OLD WINDOW
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        # 2. MAIN WINDOW
        self.window = cmds.window(self.window_name, title="Launderer v7.3: Industrial", widthHeight=(450, 750))
        
        # 3. MAIN LAYOUT
        main_layout = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="ASSET LAUNDRY: INDUSTRIAL", font="boldLabelFont", align="center", height=40, backgroundColor=[0.12, 0.12, 0.12])
        
        # 4. TABS CONTAINER
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        
        # ================= TAB 1: STRUCTURE =================
        tab1 = cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
        
        # Frame 1.1: Import
        cmds.frameLayout(label="1. Import & Hierarchy", collapsable=False, marginHeight=5, bgc=[0.2, 0.2, 0.2])
        col1 = cmds.columnLayout(adjustableColumn=True)
        cmds.button(label="IMPORT OBJ / FBX", command=self.import_file, height=40, backgroundColor=[0.2, 0.4, 0.6])
        cmds.separator(style="none", h=5)
        
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        self.chk_sep = cmds.checkBox(label="Explode Mesh Shells", value=True)
        self.chk_grp = cmds.checkBox(label="Ungroup to World", value=True)
        cmds.setParent(col1) # Back to Column
        
        cmds.button(label="SEPARATE SELECTED", command=self.run_separate, height=30, backgroundColor=[0.3, 0.3, 0.3])
        cmds.separator(style="in", h=10)
        
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=True, columnAttach=(1, 'both', 2), columnWidth2=(200, 200))
        cmds.button(label="Parent to World (Shift+P)", command=self.parent_world)
        cmds.button(label="Delete Empty Groups", command=self.delete_empty_groups)
        cmds.setParent(tab1) # JUMP BACK TO TAB ROOT (Safe!)

        # Frame 1.2: Metadata
        cmds.frameLayout(label="2. Metadata Stripper", collapsable=False, marginHeight=5, bgc=[0.25, 0.2, 0.2])
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Removes 'Blender_Custom_Props' and extra attributes.", align="left", font="obliqueLabelFont")
        cmds.button(label="NUKE CUSTOM ATTRIBUTES", command=self.nuke_attributes, height=30, backgroundColor=[0.6, 0.2, 0.2])
        cmds.setParent(self.tabs) # JUMP BACK TO TABS (Safe!)

        # ================= TAB 2: GEOMETRY =================
        tab2 = cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
        
        # Frame 2.1: Basic
        cmds.frameLayout(label="Standard Cleanup", collapsable=False, marginHeight=5, bgc=[0.2, 0.25, 0.2])
        cmds.columnLayout(adjustableColumn=True)
        self.chk_norm = cmds.checkBox(label="Normals: Conform & Soften (30deg)", value=True)
        self.chk_piv = cmds.checkBox(label="Pivots: Center & Zero Transforms", value=True)
        self.chk_hist = cmds.checkBox(label="Delete History", value=True)
        cmds.button(label="RUN BASIC CLEAN", command=self.run_basic_clean, height=35, backgroundColor=[0.3, 0.5, 0.3])
        cmds.setParent(tab2) # Back to Tab 2

        # Frame 2.2: Deep
        cmds.frameLayout(label="Deep Geometry Audit (Forensic)", collapsable=False, marginHeight=5, bgc=[0.3, 0.2, 0.2])
        cmds.columnLayout(adjustableColumn=True)
        self.chk_lamina = cmds.checkBox(label="Fix Lamina Faces (Overlapping)", value=True)
        self.chk_manifold = cmds.checkBox(label="Fix Non-Manifold Geometry", value=True)
        self.chk_zero_edge = cmds.checkBox(label="Remove Zero-Length Edges", value=True)
        self.chk_merge = cmds.checkBox(label="Merge Vertices (0.001)", value=True)
        cmds.button(label="RUN DEEP FORENSIC CLEAN", command=self.run_deep_clean, height=35, backgroundColor=[0.7, 0.2, 0.2])
        cmds.setParent(self.tabs) # Back to Tabs

        # ================= TAB 3: DISGUISE =================
        tab3 = cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
        cmds.text(label="Select objects -> Apply Native Name", align="center", font="obliqueLabelFont")
        
        cmds.frameLayout(label="Naming Strategy", collapsable=False)
        self.chk_random_idx = cmds.checkBox(label="Simulate Deletions (Random Indices)", value=True)
        cmds.setParent(tab3) # Back to Tab 3

        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(130, 60))
        # Icons
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["cube"], label='pCube', command=lambda *args: self.rename_specific("pCube"), bgc=[0.25, 0.25, 0.25])
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["cyl"], label='pCylinder', command=lambda *args: self.rename_specific("pCylinder"), bgc=[0.25, 0.25, 0.25])
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["sphere"], label='pSphere', command=lambda *args: self.rename_specific("pSphere"), bgc=[0.25, 0.25, 0.25])
        
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["group"], label='group', command=lambda *args: self.rename_specific("group"), bgc=[0.2, 0.2, 0.3])
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["locator"], label='locator', command=lambda *args: self.rename_specific("locator"), bgc=[0.2, 0.2, 0.3])
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["curve"], label='curve', command=lambda *args: self.rename_specific("curve"), bgc=[0.2, 0.2, 0.3])
        
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["light"], label='spotLight', command=lambda *args: self.rename_specific("spotLight"), bgc=[0.3, 0.2, 0.2])
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["camera"], label='camera', command=lambda *args: self.rename_specific("camera"), bgc=[0.3, 0.2, 0.2])
        cmds.iconTextButton(style='iconAndTextHorizontal', image=self.icons["plane"], label='pPlane', command=lambda *args: self.rename_specific("pPlane"), bgc=[0.25, 0.25, 0.25])
        cmds.setParent(tab3) # Back to Tab 3
        
        cmds.separator(height=10)
        cmds.button(label="Group Selection (group#)", command=self.smart_group, height=35)
        cmds.setParent(self.tabs) # Back to Tabs

        # ================= TAB 4: POLISH =================
        tab4 = cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
        cmds.frameLayout(label="Professional Polish", collapsable=False)
        self.chk_mat = cmds.checkBox(label="Convert Materials (aiStandardSurface)", value=True)
        self.chk_wire = cmds.checkBox(label="Randomize Wireframe Colors", value=True)
        self.chk_layer = cmds.checkBox(label="Add to 'Clean_Geo' Layer", value=True)
        cmds.button(label="APPLY FINAL POLISH", command=self.run_polish, height=40, backgroundColor=[0.3, 0.6, 0.3])
        cmds.setParent(main_layout) # Back to Main

        # 5. FINALIZE
        cmds.tabLayout(self.tabs, edit=True, tabLabel=((tab1, '1. Structure'), (tab2, '2. Geometry'), (tab3, '3. Disguise'), (tab4, '4. Polish')))
        
        cmds.text(label="Execution Log:", align="left", parent=main_layout, font="boldLabelFont")
        self.scroll_field = cmds.scrollField(editable=False, wordWrap=True, height=100, parent=main_layout)
        
        cmds.showWindow(self.window)

    def log(self, message):
        print(message)
        cmds.scrollField(self.scroll_field, edit=True, insertText=message + "\n")
        cmds.refresh()

    def get_selection(self):
        sel = cmds.ls(selection=True, type="transform", long=True)
        if not sel: self.log("Nothing selected!"); return []
        return sel

    # --- ACTIONS ---
    def import_file(self, *args):
        filters = "OBJ/FBX (*.obj *.fbx);;All Files (*.*)"
        file_path = cmds.fileDialog2(fileFilter=filters, dialogStyle=2, fileMode=1)
        if file_path:
            cmds.file(file_path[0], i=True, ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, options="mo=1")
            self.log(f"Imported: {file_path[0]}")

    def run_separate(self, *args):
        sel = self.get_selection()
        if not sel: return
        self.log("Exploding meshes...")
        new_sel = []
        for obj in sel:
            try:
                sep = cmds.polySeparate(obj, ch=False)
                if cmds.checkBox(self.chk_grp, query=True, value=True):
                    try:
                        unp = cmds.parent(sep, w=True)
                        new_sel.extend(unp); cmds.delete(obj)
                    except: new_sel.extend(sep)
                else: new_sel.extend(sep)
            except: new_sel.append(obj)
        valid = [x for x in new_sel if cmds.objExists(x)]
        if valid: cmds.select(valid)
        self.log(f"Separated into {len(valid)} objects.")

    def parent_world(self, *args):
        sel = self.get_selection()
        if sel: cmds.parent(sel, w=True); self.log("Parented to World.")

    def delete_empty_groups(self, *args):
        transforms = cmds.ls(type="transform", long=True)
        deleted = 0
        for t in transforms:
            if not cmds.listRelatives(t, c=True) and not cmds.listRelatives(t, shapes=True):
                try: cmds.delete(t); deleted += 1
                except: pass
        self.log(f"Deleted {deleted} empty groups.")

    def nuke_attributes(self, *args):
        sel = self.get_selection()
        if not sel: return
        count = 0
        for obj in sel:
            ud_attrs = cmds.listAttr(obj, userDefined=True) or []
            for attr in ud_attrs:
                try: cmds.setAttr(f"{obj}.{attr}", lock=False); cmds.deleteAttr(obj, attribute=attr); count += 1
                except: pass
        self.log(f"Removed {count} attributes.")

    def run_basic_clean(self, *args):
        sel = self.get_selection()
        if not sel: return
        for obj in sel:
            if not cmds.objExists(obj): continue
            if cmds.checkBox(self.chk_norm, query=True, value=True):
                try: cmds.polyNormalPerVertex(obj, unFreezeNormal=True); cmds.polyNormal(obj, nm=2, unm=0, ch=0); cmds.polySetToFaceNormal(obj); cmds.polySoftEdge(obj, angle=30, ch=0)
                except: pass
            if cmds.checkBox(self.chk_piv, query=True, value=True):
                try: cmds.xform(obj, cp=True); cmds.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0, pn=1)
                except: pass
            if cmds.checkBox(self.chk_hist, query=True, value=True): cmds.delete(obj, ch=True)
        self.log("Basic Clean Done.")

    def run_deep_clean(self, *args):
        sel = self.get_selection()
        if not sel: return
        if cmds.checkBox(self.chk_merge, query=True, value=True):
            for obj in sel: 
                try: cmds.polyMergeVertex(obj, d=0.001, ch=False)
                except: pass
        
        do_lamina = cmds.checkBox(self.chk_lamina, query=True, value=True)
        do_manifold = cmds.checkBox(self.chk_manifold, query=True, value=True)
        if do_lamina or do_manifold:
            for obj in sel:
                try: cmds.polyCleanup(obj, on=True, nm=do_manifold, lam=do_lamina)
                except: pass
        cmds.select(sel)
        self.log("Deep Clean Done.")

    def rename_specific(self, base_name):
        sel = self.get_selection()
        if not sel: return
        
        use_random = cmds.checkBox(self.chk_random_idx, query=True, value=True)
        self.log(f"Renaming to {base_name}...")
        
        random.shuffle(sel)
        start_idx = 1
        
        for obj in sel:
            if not cmds.objExists(obj): continue
            
            if use_random:
                jump = random.randint(1, 5)
                idx = start_idx + jump
                start_idx = idx
            else:
                idx = start_idx
                start_idx += 1
                
            new_name = f"{base_name}{idx}"
            while cmds.objExists(new_name):
                idx += 1
                new_name = f"{base_name}{idx}"
                start_idx = idx
            
            renamed = cmds.rename(obj, new_name)
            
            shapes = cmds.listRelatives(renamed, shapes=True, fullPath=True)
            if shapes:
                if "group" in base_name: shape_tgt = None
                else: 
                    # Default rule: Name + "Shape" + Number
                    num = new_name.replace(base_name, "")
                    if "pCube" in base_name: shape_tgt = f"pCubeShape{num}"
                    elif "pCylinder" in base_name: shape_tgt = f"pCylinderShape{num}"
                    elif "pSphere" in base_name: shape_tgt = f"pSphereShape{num}"
                    elif "pPlane" in base_name: shape_tgt = f"pPlaneShape{num}"
                    elif "curve" in base_name: shape_tgt = f"curveShape{num}"
                    elif "camera" in base_name: shape_tgt = f"cameraShape{num}"
                    elif "spotLight" in base_name: shape_tgt = f"spotLightShape{num}"
                    elif "locator" in base_name: shape_tgt = f"locatorShape{num}"
                    else: shape_tgt = f"{new_name}Shape"
                
                if shape_tgt:
                    for s in shapes:
                        if s.split("|")[-1] != shape_tgt:
                            try: cmds.rename(s, shape_tgt)
                            except: pass
        self.log("Renaming complete.")

    def smart_group(self, *args):
        sel = self.get_selection()
        if not sel: return
        grp = cmds.group(sel, n="group1")
        cmds.xform(grp, cp=True)
        self.log(f"Grouped into {grp}")

    def run_polish(self, *args):
        sel = self.get_selection()
        if not sel: return
        if cmds.checkBox(self.chk_mat, query=True, value=True): self.process_materials(sel)
        if cmds.checkBox(self.chk_wire, query=True, value=True):
            for obj in sel:
                shapes = cmds.listRelatives(obj, shapes=True) or []
                for s in shapes:
                    cmds.setAttr(s + ".overrideEnabled", 1); cmds.setAttr(s + ".overrideColor", random.randint(3, 30))
        if cmds.checkBox(self.chk_layer, query=True, value=True):
            if not cmds.objExists("Clean_Geo_Lyr"): cmds.createDisplayLayer(n="Clean_Geo_Lyr", empty=True)
            cmds.editDisplayLayerMembers("Clean_Geo_Lyr", sel)
        self.log("Polished.")

    def process_materials(self, objects):
        if not cmds.pluginInfo('mtoa', query=True, loaded=True): return
        processed = set()
        for obj in objects:
            shapes = cmds.listRelatives(obj, shapes=True) or []
            for shape in shapes:
                se_list = cmds.listConnections(shape, type='shadingEngine') or []
                for se in se_list:
                    mats = cmds.listConnections(se + ".surfaceShader") or []
                    if not mats: continue
                    mat = mats[0]
                    if mat in processed: continue
                    if cmds.objectType(mat) in ['phong', 'lambert', 'blinn']:
                        new_mat = cmds.shadingNode('aiStandardSurface', asShader=True)
                        new_mat = cmds.rename(new_mat, mat.replace("Material", "M") + "_ai")
                        if cmds.attributeQuery("color", node=mat, exists=True):
                            c = cmds.getAttr(mat + ".color")[0]
                            cmds.setAttr(new_mat + ".baseColor", c[0], c[1], c[2], type="double3")
                        cmds.connectAttr(new_mat + ".outColor", se + ".surfaceShader", force=True)
                        processed.add(new_mat)

tool = MayaLaundererGodMode()
tool.create_ui()