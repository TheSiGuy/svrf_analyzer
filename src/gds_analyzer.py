"""
GDS Analyzer module:
Functions to load GDS layout, extract markers, associate rule groups with patterns, and extract rule names (text labels).
"""

import gdstk



# Layer numbers and Datatypes
rule_name_layer=22
rule_name_datatype=22
rule_grouping_marker_layer=255
rule_grouping_marker_datatype=1
pattern_marking_layer=255
pattern_marking_datatype=0

# Calculate the centroid of a polygon
def compute_centroid(polygon):
    vertices = polygon.points
    x = vertices[:, 0]
    y = vertices[:, 1]
    a = 0.5 * (x[:-1] * y[1:] - x[1:] * y[:-1]).sum()
    cx = (1 / (6 * a)) * ((x[:-1] + x[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1])).sum()
    cy = (1 / (6 * a)) * ((y[:-1] + y[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1])).sum()
    return (cx, cy)


def load_gds_layout(gds_path):
    """
    Load a GDS file and return the contained cells.
    """
    lib = gdstk.read_gds(gds_path)

    if len(lib.cells) == 0:
        raise ValueError(f"No cells found in {gds_path}")
    return lib.cells


def extract_markers(cell):
    """
    Extract polygons from a cell grouped by (layer, datatype).
    Returns a dict with keys (layer, datatype) and values list of polygons.
    The output will be like:
        # {
        #     (1, 0): [poly1, poly2],
        #     (2, 5): [poly3]
        # }
    """
    markers = {}
    for poly in cell.polygons:
        key = (poly.layer, poly.datatype)
        markers.setdefault(key, []).append(poly)
    return markers



def find_text_labels(cell, layer=rule_name_layer, datatype=rule_name_datatype):
    """
    Extract text labels from cell on the given layer and datatype.
    Returns list of dicts with text and position.
    Example:
        # [
        #     {'text': 'M.A.1', 'position': (10, 20)},
        #     {'text': 'L.S.1', 'position': (30, 40)}
        # ]
    """
    labels = []
    for text in cell.labels:
        if text.layer == layer and text.texttype == datatype:
            labels.append({'text': text.text, 'position': text.origin})
    return labels




def find_rule_groups(cell):
    """
    Extract polygons on layer 255 with datatype 1 (255.1) which represent rule group regions.
    Returns list of polygons.
    """
    rule_group_polys = []
    for poly in cell.polygons:
        if poly.layer == rule_grouping_marker_layer and poly.datatype == rule_grouping_marker_datatype:
            rule_group_polys.append(poly)
    return rule_group_polys


def polygon_contains_point(polygon, coord):
    """
    Check if a point lies inside a polygon.

    """
    return polygon.contain(coord)


def patterns_in_polygon(patterns, polygon):
    """
    Return patterns that lie inside polygon.
    Checks centroid of each pattern polygon.
    """
    contained = []
    for p in patterns:
        centroid = compute_centroid(p)
        if polygon_contains_point(polygon, centroid):
            contained.append(p)
    return contained


def associate_rules_to_patterns(cell):
    """
    Associate rule groups (255.1 polygons) with rule names (text on 22.22)
    and collect patterns (255.0 polygons) inside those groups.
    Returns dict {rule_name: [pattern_polygons]}:
        {
            'RULE_A': [pattern_poly1, pattern_poly2],
            'RULE_B': [pattern_poly3]
        }
    """
    rule_groups = find_rule_groups(cell)   # polygons on layer 255 and datatype 1
    text_labels = find_text_labels(cell)   # rule names on layer 22 and datatype 22
    patterns = [p for p in cell.polygons if p.layer == pattern_marking_layer and p.datatype == pattern_marking_datatype]

    rule_map = {}
    #Loop over each rule group polygon
    for group_poly in rule_groups:
        group_centroid = compute_centroid(group_poly)
        associated_label = None

        # Find label inside polygon
        #Checks if any label's position is inside the current rule polygon
        for label in text_labels:
            if polygon_contains_point(group_poly, label['position']):
                associated_label = label['text']
                break

        # If none found inside, pick nearest label by distance (Euclidean distance.)
        if associated_label is None:
            min_dist = float('inf')
            for label in text_labels:
                dx = label['position'][0] - group_centroid[0]
                dy = label['position'][1] - group_centroid[1]
                dist = dx*dx + dy*dy
                if dist < min_dist:
                    min_dist = dist
                    associated_label = label['text']

        contained_patterns = patterns_in_polygon(patterns, group_poly)
        rule_map[associated_label] = contained_patterns

    return rule_map






