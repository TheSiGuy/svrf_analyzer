from src.gds_analyzer import compute_centroid
import gdstk
"""
Pattern Validator module:
Logic to validate test patterns (good/bad) according to layout analysis specifications.
"""

def validate_patterns(rule_name, patterns, error_markers):
    """
    Validate patterns for a given rule.

    Args:
        rule_name (str): Name of the rule.
        patterns (list): List of pattern polygons on layer 255.0 (pattern marking layer).
        error_markers (list): List of polygons on layer 0.1 (result marker) indicating errors.

    Returns:
        dict: {
            'good': {'pass': int, 'fail': int},
            'bad': {'pass': int, 'fail': int},
        }
    """
    # Initialize results dict
    results = {
        'good': {'pass': 0, 'fail': 0},
        'bad': {'pass': 0, 'fail': 0},
    }

    # Check if pattern overlaps any error marker polygon
    def pattern_has_error(pattern, error_markers):
        for err in error_markers:
            if polygons_overlap(pattern, err):
                return True
        return False

    for pattern in patterns:
        centroid = compute_centroid(pattern)
        # x > 0 good case, else bad case
        is_good = centroid[0] > 0

        has_error = pattern_has_error(pattern, error_markers)

        if is_good:
            if not has_error:
                results['good']['pass'] += 1
            else:
                results['good']['fail'] += 1
        else:
            if has_error:
                results['bad']['pass'] += 1
            else:
                results['bad']['fail'] += 1

    return results


def polygons_overlap(poly1, poly2):
    """
    Check if two polygons overlap.
    Using bounding box for quick check, then precise check.

    Args:
        poly1, poly2: Polygon objects.

    Returns:
        bool: True if they overlap.
    """
    bbox1 = poly1.bounding_box()
    bbox2 = poly2.bounding_box()

    # Quick bbox overlap test
    if (bbox1[1][0] < bbox2[0][0] or bbox2[1][0] < bbox1[0][0] or
        bbox1[1][1] < bbox2[0][1] or bbox2[1][1] < bbox1[0][1]):
        return False

    # Returns list of polygons if overlapping
    intersection = gdstk.boolean(poly1, poly2, operation="and")
    return len(intersection) > 0
