#!/usr/bin/env python
from ete2 import Tree, TreeStyle, AttrFace, TextFace, add_face_to_node
__author__ = "Jaime Huerta-Cepas"
__email__ = "jhcepas@gmail.com"

def layout(node):
    node.img_style["size"] = 0
    node.img_style['hz_line_width'] = 2
    node.img_style['vt_line_width'] = 2
    
    if node.is_leaf():
        # parse names
        fields = node.name.split("__")
        name = fields[1].replace('_', ' ')
        code = "%s" %fields[0].strip()

        # Specie name
        nF = TextFace(name, fsize=12, fgcolor='#444', fstyle='italic')
        add_face_to_node(nF, node, column=0, position='aligned')

        # Species code
        cF = TextFace(code, fsize=12, fgcolor='grey')
        cF.margin_left = 4
        cF.margin_right = 4
        add_face_to_node(cF, node, column=1, position='branch-right')

        # Lead node styling 
        node.img_style['hz_line_color'] = "green"
        node.img_style['vt_line_color'] = "green"
        
    else:
        # L90: green, L70: blue, L50: dark blue, L30: pink and L10: red. For the species
        # tree discordance test we collapse all branches below L90.
        B = float(node.B)
        if B >= 90:
            color = "green"
        elif B >= 70:
            color = "blue"
        elif B >= 50:
            color = "darkblue"
        elif B >= 30:
            color = "pink"
        elif B >= 10:
            color = "red"
        else:
            color = "yellow"
    
        node.img_style['hz_line_color'] = color
        node.img_style['vt_line_color'] = color

if __name__ == "__main__":
    t = Tree('swisstree_speciestree.nhx')

    # basic tree styling 
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = layout
    ts.arc_span = 340
    ts.show_scale = False

    # branch sortings and adjustment
    t.ladderize()
    t.convert_to_ultrametric(100)

    # scale setup by try and error, this is the min that allows to show all names
    # without adding extra dashed lines
    ts.scale = 4

    # Render main tree
    for f in ["png", "pdf", "svg"]:
        ts.mode = 'c'
        t.render('swisstree_species_allbranches_c.%s' %f, tree_style=ts, w=1080, dpi=300)
        ts.mode = "r"
        t.render('swisstree_species_allbranches_r.%s'%f, tree_style=ts, w=1080, dpi=300)

    # Delete nodes with B>90, creating multifurcations. Only green branches
    # should remain
    for n in t.get_descendants():
        if float(getattr(n, "B", 100)) < 90:
            n.delete(True)

    # Readjust for ultratmetric visualization
    t.convert_to_ultrametric(100)

    # Render collapsed tree
    for f in ["png", "pdf", "svg"]:
        ts.mode = 'c'
        t.render('swisstree_species_collapsed90_c.%s' %f, tree_style=ts, w=1080, dpi=300)
        ts.mode = "r"
        t.render('swisstree_species_collapsed90_r.%s'%f, tree_style=ts, w=1080, dpi=300)

