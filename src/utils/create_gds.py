import gdstk

def create_test_layout_cell():
    # Create a library, user units set to microns (µm), database units is 1nm
    lib = gdstk.Library(unit=1e-6, precision=1e-9)

    # Suggested layer and datatype variable names
    pattern_layer_no = 100
    pattern_marking_layer_no = 255
    error_location_marker_layer_no = 0
    result_marker_layer_no = 0
    result_marker_layer_dt = 1
    rule_grouping_marker_layer_no = 255
    rule_grouping_marker_dt = 1
    rule_name_text_layer_no = 22
    rule_name_textype = 22

    # Create the cell
    cell = lib.new_cell("SQUARES")

    # pattern parameters
    pattern_side = 1  # in µm
    error_side = 0.5  # sqrt(0.25) µm

    # Centers of patterns
    centers_main = [(4, 0), (8, 0), (-4, 0), (-8, 0)]

    # Add the patterns on layer 100
    for cx, cy in centers_main:
        ptrn = gdstk.rectangle(
            (cx - pattern_side / 2, cy - pattern_side / 2),
            (cx + pattern_side / 2, cy + pattern_side / 2),
            layer=pattern_layer_no
        )
        cell.add(ptrn)

    # Add the pattern markers and the error location markers on 255 and 0
    for marking_layer in [pattern_marking_layer_no, error_location_marker_layer_no]:
        for cx, cy in centers_main:
            marking_polygon = gdstk.rectangle(
                (cx - pattern_side / 2, cy - pattern_side / 2),
                (cx + pattern_side / 2, cy + pattern_side / 2),
                layer=marking_layer
            )
            cell.add(marking_polygon)

    # Result_marking_plygons at (4, 0) and (-8, 0) on layer 0.1
    for cx in [4, -8]:
        result_marking_plygon = gdstk.rectangle(
            (cx - error_side / 2, -error_side / 2),
            (cx + error_side / 2, error_side / 2),
            layer=result_marker_layer_no,
            datatype=result_marker_layer_dt
        )
        cell.add(result_marking_plygon)

    # Rule grouping marking polygon on layer 255.1
    cover_margin = 1  # margin
    min_x = min(x for x, _ in centers_main) - cover_margin
    max_x = max(x for x, _ in centers_main) + cover_margin
    min_y = -1
    max_y = 1

    rule_grouping_polygon = gdstk.rectangle(
        (min_x, min_y),
        (max_x, max_y),
        layer=rule_grouping_marker_layer_no,
        datatype=rule_grouping_marker_dt
    )
    cell.add(rule_grouping_polygon)

    # Rule name text label
    label = gdstk.Label(
        "check_name",
        origin=(0, -0.5),  # µm
        layer=rule_name_text_layer_no,
        texttype=rule_name_textype
    )
    cell.add(label)
    return cell

    # Write the GDS file
    # lib.write_gds("test.gds")

    # print("GDSII file 'test.gds' created successfully.")
