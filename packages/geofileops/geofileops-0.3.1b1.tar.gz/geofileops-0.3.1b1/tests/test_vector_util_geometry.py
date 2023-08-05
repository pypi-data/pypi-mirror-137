# -*- coding: utf-8 -*-
"""
Tests for functionalities in vector_util, regarding geometry operations.
"""

from pathlib import Path
import sys

import geopandas as gpd
import shapely.geometry as sh_geom

# Add path so the local geofileops packages are found
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from geofileops import geofile
from geofileops.util import geometry_util
from geofileops.util.geometry_util import GeometryType
from geofileops.util import grid_util
import test_helper

def test_geometrytype():
    geometrytype = GeometryType(3)
    assert geometrytype is GeometryType.POLYGON
    geometrytype = GeometryType('PoLyGoN')
    assert geometrytype is GeometryType.POLYGON
    geometrytype = GeometryType(GeometryType.POLYGON)
    assert geometrytype is GeometryType.POLYGON

def test_makevalid():
    # Test Point
    point_valid = geometry_util.make_valid(test_helper.TestData.point)
    assert isinstance(point_valid, sh_geom.Point)

    # Test MultiPoint
    multipoint_valid = geometry_util.make_valid(test_helper.TestData.multipoint)
    assert isinstance(multipoint_valid, sh_geom.MultiPoint)

    # Test LineString
    linestring_valid = geometry_util.make_valid(test_helper.TestData.linestring)
    assert isinstance(linestring_valid, sh_geom.LineString)
    
    # Test MultiLineString
    multilinestring_valid = geometry_util.make_valid(test_helper.TestData.multilinestring)
    assert isinstance(multilinestring_valid, sh_geom.MultiLineString)

    # Test Polygon, self-intersecting
    polygon_invalid = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (5, 10), (4, 11), (4, 9), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,8), (8,8), (8,2), (2,2)]])
    poly_valid = geometry_util.make_valid(polygon_invalid)
    assert isinstance(poly_valid, sh_geom.MultiPolygon)
    assert len(poly_valid) == 2
    assert len(poly_valid[0].interiors) == 1

    # Test MultiPolygon
    multipolygon_invalid = sh_geom.MultiPolygon([polygon_invalid, test_helper.TestData.polygon2])
    multipoly_valid = geometry_util.make_valid(multipolygon_invalid)
    assert isinstance(multipoly_valid, sh_geom.MultiPolygon)

    # Test GeometryCollection (as combination of all previous ones)
    geometrycollection_invalid = sh_geom.GeometryCollection([
            test_helper.TestData.point, test_helper.TestData.multipoint, test_helper.TestData.linestring, 
            test_helper.TestData.multilinestring, polygon_invalid, multipolygon_invalid])
    geometrycollection_valid = geometry_util.make_valid(geometrycollection_invalid)
    assert isinstance(geometrycollection_valid, sh_geom.GeometryCollection)

def test_numberpoints():
    # Test Point
    numberpoints = geometry_util.numberpoints(test_helper.TestData.point)
    numberpoints_geometrycollection = numberpoints
    assert numberpoints == 1

    # Test MultiPoint
    numberpoints = geometry_util.numberpoints(test_helper.TestData.multipoint)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 3
    
    # Test LineString
    numberpoints = geometry_util.numberpoints(test_helper.TestData.linestring)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 3
    
    # Test MultiLineString
    numberpoints = geometry_util.numberpoints(test_helper.TestData.multilinestring)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 6

    # Test Polygon
    numberpoints = geometry_util.numberpoints(test_helper.TestData.polygon)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 11

    # Test MultiPolygon
    numberpoints = geometry_util.numberpoints(test_helper.TestData.multipolygon)
    numberpoints_geometrycollection += numberpoints
    assert numberpoints == 16

    # Test GeometryCollection (as combination of all previous ones)
    numberpoints = geometry_util.numberpoints(test_helper.TestData.geometrycollection)
    assert numberpoints == numberpoints_geometrycollection

def test_remove_inner_rings():
    # Apply to single Polygon, with area tolerance smaller than holes
    polygon_removerings = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (1, 10), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,4), (4,4), (4,2), (2,2)], [(5,5), (5,6), (7,6), (7,5), (5,5)]])
    poly_result = geometry_util.remove_inner_rings(polygon_removerings, min_area_to_keep=1)
    assert isinstance(poly_result, sh_geom.Polygon)
    assert len(poly_result.interiors) == 2

    # Apply to single Polygon, with area tolerance between 
    # smallest hole (= 2m²) and largest (= 4m²)
    poly_result = geometry_util.remove_inner_rings(polygon_removerings, min_area_to_keep=3)
    assert isinstance(poly_result, sh_geom.Polygon)
    assert len(poly_result.interiors) == 1

    # Apply to MultiPolygon, with area tolerance between 
    # smallest hole (= 2m²) and largest (= 4m²)
    polygon_removerings2 = sh_geom.Polygon(shell=[(100, 100), (100, 110), (110, 110), (110, 100), (100,100)])
    multipoly_removerings = sh_geom.MultiPolygon([polygon_removerings, polygon_removerings2])
    poly_result = geometry_util.remove_inner_rings(multipoly_removerings, min_area_to_keep=3)
    assert isinstance(poly_result, sh_geom.MultiPolygon)
    assert len(poly_result[0].interiors) == 1
    
def test_simplify_ext_lang_basic():
    # Test LineString lookahead -1 
    linestring = sh_geom.LineString([(0, 0), (10, 10), (20, 20)])
    geom_simplified = geometry_util.simplify_ext(
            geometry=linestring, 
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1,
            lookahead=-1)
    assert isinstance(geom_simplified, sh_geom.LineString)
    assert len(geom_simplified.coords) < len(linestring.coords)
    assert len(geom_simplified.coords) == 2

    # Test Polygon lookahead -1 
    poly = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (1, 10), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,8), (8,8), (8,2), (2,2)]])
    geom_simplified = geometry_util.simplify_ext(
            geometry=poly, 
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1,
            lookahead=-1)
    assert isinstance(geom_simplified, sh_geom.Polygon)
    assert geom_simplified.exterior is not None
    assert poly.exterior is not None
    assert len(geom_simplified.exterior.coords) < len(poly.exterior.coords)
    assert len(geom_simplified.exterior.coords) == 5

    # Test Point simplification
    point = sh_geom.Point((0, 0))
    geom_simplified = geometry_util.simplify_ext(
            geometry=point, 
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.Point)
    assert len(geom_simplified.coords) == 1

    # Test MultiPoint simplification
    multipoint = sh_geom.MultiPoint([(0, 0), (10, 10), (20, 20)])
    geom_simplified = geometry_util.simplify_ext(
            geometry=multipoint,
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.MultiPoint)
    assert len(geom_simplified) == 3

    # Test LineString simplification
    linestring = sh_geom.LineString([(0, 0), (10, 10), (20, 20)])
    geom_simplified = geometry_util.simplify_ext(
            geometry=linestring, 
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.LineString)
    assert len(geom_simplified.coords) < len(linestring.coords)
    assert len(geom_simplified.coords) == 2
    
    # Test MultiLineString simplification
    multilinestring = sh_geom.MultiLineString(
            [list(linestring.coords), [(100, 100), (110, 110), (120, 120)]])
    geom_simplified = geometry_util.simplify_ext(
            geometry=multilinestring, 
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.MultiLineString)
    assert len(geom_simplified) == 2
    assert len(geom_simplified[0].coords) < len(multilinestring[0].coords)
    assert len(geom_simplified[0].coords) == 2
    
    # Test Polygon simplification
    poly = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (1, 10), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,8), (8,8), (8,2), (2,2)]])
    geom_simplified = geometry_util.simplify_ext(
            geometry=poly,
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.Polygon)
    assert geom_simplified.exterior is not None
    assert poly.exterior is not None
    assert len(geom_simplified.exterior.coords) < len(poly.exterior.coords)
    assert len(geom_simplified.exterior.coords) == 5

    # Test MultiPolygon simplification
    poly2 = sh_geom.Polygon(shell=[(100, 100), (100, 110), (110, 110), (110, 100), (100,100)])
    multipoly = sh_geom.MultiPolygon([poly, poly2])
    geom_simplified = geometry_util.simplify_ext(
            geometry=multipoly,
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.MultiPolygon)
    assert len(geom_simplified) == 2
    assert len(geom_simplified[0].exterior.coords) < len(poly.exterior.coords)
    assert len(geom_simplified[0].exterior.coords) == 5

    # Test GeometryCollection (as combination of all previous ones) simplification
    geom = sh_geom.GeometryCollection([point, multipoint, linestring, multilinestring, poly, multipoly])
    geom_simplified = geometry_util.simplify_ext(
            geometry=geom,
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.GeometryCollection)
    assert len(geom_simplified) == 6

def test_simplify_ext_lang_preservetopology():
    
    ### Test Polygon lookahead -1 ###
    poly = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (1, 10), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,8), (8,8), (8,2), (2,2)]])
    # If preserve_topology True, the original polygon is returned...
    geom_simplified = geometry_util.simplify_ext(
            geometry=poly, 
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=10,
            preserve_topology=True,
            lookahead=-1)
    assert isinstance(geom_simplified, sh_geom.Polygon)
    assert poly.equals(geom_simplified) is True

    # If preserve_topology True, the original polygon is returned...
    geom_simplified = geometry_util.simplify_ext(
            geometry=poly, 
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=10,
            preserve_topology=False,
            lookahead=-1)
    assert geom_simplified is None

def test_simplify_ext_invalid():
    # Test Polygon simplification, with invalid exterior ring
    poly = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (5, 10), (3, 12), (3, 9), (10, 10), (10, 0), (0,0)], 
            holes=[[(2,2), (2,8), (8,8), (8,2), (2,2)]])
    geom_simplified = geometry_util.simplify_ext(
            geometry=poly,
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert isinstance(geom_simplified, sh_geom.MultiPolygon)
    assert poly.exterior is not None
    assert len(geom_simplified[0].exterior.coords) < len(poly.exterior.coords)
    assert len(geom_simplified[0].exterior.coords) == 7
    assert len(geom_simplified[0].interiors) == len(poly.interiors)

    # Test Polygon simplification, with exterior ring that touches itself 
    # due to simplification and after make_valid results in multipolygon of 
    # 2 equally large parts (left and right part of M shape).
    poly_m_touch = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (5, 5), (10, 10), (10, 0), 
                   (8, 0), (8, 5), (5, 4), (2, 5), (2, 0), (0, 0)])
    geom_simplified = geometry_util.simplify_ext(
            geometry=poly_m_touch,
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert geom_simplified is not None
    assert geom_simplified.is_valid
    assert isinstance(geom_simplified, sh_geom.MultiPolygon)
    assert len(geom_simplified) == 2
    assert geometry_util.numberpoints(geom_simplified) < geometry_util.numberpoints(poly)
    
    # Test Polygon simplification, with exterior ring that crosses itself
    # due to simplification and after make_valid results in multipolygon of 
    # 3 parts (left, middle and right part of M shape).
    poly_m_cross = sh_geom.Polygon(
            shell=[(0, 0), (0, 10), (5, 5), (10, 10), (10, 0), 
                   (8, 0), (8, 5.5), (5, 4.5), (2, 5.5), (2, 0), (0, 0)])
    geom_simplified = geometry_util.simplify_ext(
            geometry=poly_m_cross,
            algorithm=geometry_util.SimplifyAlgorithm.LANG, 
            tolerance=1)
    assert geom_simplified is not None
    assert geom_simplified.is_valid
    assert isinstance(geom_simplified, sh_geom.MultiPolygon)
    assert len(geom_simplified) == 3

def test_simplify_ext_keep_points_on(tmpdir):
    
    #### Test if keep_points_on works properly ####
    
    ## First init some stuff ##
    # Read the test data
    input_path = test_helper.TestFiles.polygons_simplify_onborder_testcase_gpkg
    geofile.copy(input_path, tmpdir / input_path.name)
    input_gdf = geofile.read_file(input_path)

    # Create geometry where we want the points kept
    grid_gdf = grid_util.create_grid(
            total_bounds=(210431.875-1000, 176640.125-1000, 210431.875+1000, 176640.125+1000),
            nb_columns=2,
            nb_rows=2,
            crs='epsg:31370')
    geofile.to_file(grid_gdf, tmpdir / "grid.gpkg")
    grid_coords = [tile.exterior.coords for tile in grid_gdf['geometry']]
    grid_lines_geom = sh_geom.MultiLineString(grid_coords)
    
    ## Test rdp (ramer–douglas–peucker) ##
    # Without keep_points_on, the following point that is on the test data + 
    # on the grid is removed by rdp 
    point_on_input_and_border = sh_geom.Point(210431.875, 176599.375)
    tolerance_rdp = 0.5

    # Determine the number of intersects with the input test data
    nb_intersects_with_input = len(input_gdf[input_gdf.intersects(point_on_input_and_border)])
    assert nb_intersects_with_input > 0
    # Test if intersects > 0
    assert len(input_gdf[grid_gdf.intersects(point_on_input_and_border)]) > 0

    # Without keep_points_on the number of intersections changes 
    simplified_gdf = input_gdf.copy()
    # assert to evade pyLance warning 
    assert isinstance(simplified_gdf, gpd.GeoDataFrame)
    simplified_gdf.geometry = input_gdf.geometry.apply(
            lambda geom: geometry_util.simplify_ext(
                    geom, algorithm=geometry_util.SimplifyAlgorithm.RAMER_DOUGLAS_PEUCKER, 
                    tolerance=tolerance_rdp))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_rdp{tolerance_rdp}.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) != nb_intersects_with_input
    
    # With keep_points_on specified, the number of intersections stays the same 
    simplified_gdf = input_gdf.copy()
    # assert to evade pyLance warning 
    assert isinstance(simplified_gdf, gpd.GeoDataFrame)
    simplified_gdf.geometry = input_gdf.geometry.apply(
            lambda geom: geometry_util.simplify_ext(
                    geom, algorithm=geometry_util.SimplifyAlgorithm.RAMER_DOUGLAS_PEUCKER, 
                    tolerance=tolerance_rdp, keep_points_on=grid_lines_geom))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_rdp{tolerance_rdp}_keep_points_on.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) == nb_intersects_with_input
    
    ## Test vw (visvalingam-whyatt) ##
    # Without keep_points_on, the following point that is on the test data + 
    # on the grid is removed by vw 
    point_on_input_and_border = sh_geom.Point(210430.125, 176640.125)
    tolerance_vw = 16*0.25*0.25   # 1m²

    # Determine the number of intersects with the input test data
    nb_intersects_with_input = len(input_gdf[input_gdf.intersects(point_on_input_and_border)])
    assert nb_intersects_with_input > 0
    # Test if intersects > 0
    assert len(input_gdf[grid_gdf.intersects(point_on_input_and_border)]) > 0

    # Without keep_points_on the number of intersections changes 
    simplified_gdf = input_gdf.copy()
    # assert to evade pyLance warning 
    assert isinstance(simplified_gdf, gpd.GeoDataFrame)
    simplified_gdf.geometry = input_gdf.geometry.apply(
            lambda geom: geometry_util.simplify_ext(
                    geom, algorithm=geometry_util.SimplifyAlgorithm.VISVALINGAM_WHYATT, 
                    tolerance=tolerance_vw))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_vw{tolerance_vw}.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) != nb_intersects_with_input
    
    # With keep_points_on specified, the number of intersections stays the same 
    simplified_gdf = input_gdf.copy()
    # assert to evade pyLance warning 
    assert isinstance(simplified_gdf, gpd.GeoDataFrame)
    simplified_gdf.geometry = input_gdf.geometry.apply(
            lambda geom: geometry_util.simplify_ext(
                    geom, algorithm=geometry_util.SimplifyAlgorithm.VISVALINGAM_WHYATT, 
                    tolerance=tolerance_vw, 
                    keep_points_on=grid_lines_geom))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_vw{tolerance_vw}_keep_points_on.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) == nb_intersects_with_input
    
    ## Test lang ##
    # Without keep_points_on, the following point that is on the test data + 
    # on the grid is removed by lang 
    point_on_input_and_border = sh_geom.Point(210431.875,176606.125)
    tolerance_lang = 0.25
    step_lang = 8

    # Determine the number of intersects with the input test data
    nb_intersects_with_input = len(input_gdf[input_gdf.intersects(point_on_input_and_border)])
    assert nb_intersects_with_input > 0
    # Test if intersects > 0
    assert len(input_gdf[grid_gdf.intersects(point_on_input_and_border)]) > 0

    # Without keep_points_on the number of intersections changes 
    simplified_gdf = input_gdf.copy()
    # assert to evade pyLance warning 
    assert isinstance(simplified_gdf, gpd.GeoDataFrame)
    simplified_gdf.geometry = input_gdf.geometry.apply(
            lambda geom: geometry_util.simplify_ext(
                    geom, algorithm=geometry_util.SimplifyAlgorithm.LANG, 
                    tolerance=tolerance_lang, lookahead=step_lang))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_lang;{tolerance_lang};{step_lang}.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) != nb_intersects_with_input
    
    # With keep_points_on specified, the number of intersections stays the same 
    simplified_gdf = input_gdf.copy()
    # assert to evade pyLance warning 
    assert isinstance(simplified_gdf, gpd.GeoDataFrame)
    simplified_gdf.geometry = input_gdf.geometry.apply(
            lambda geom: geometry_util.simplify_ext(
                    geom, algorithm=geometry_util.SimplifyAlgorithm.LANG, 
                    tolerance=tolerance_lang, lookahead=step_lang, 
                    keep_points_on=grid_lines_geom))
    geofile.to_file(simplified_gdf, tmpdir / f"simplified_lang;{tolerance_lang};{step_lang}_keep_points_on.gpkg")
    assert len(simplified_gdf[simplified_gdf.intersects(point_on_input_and_border)]) == nb_intersects_with_input

def test_simplify_ext_no_simplification():
    # Backup reference to simplification module
    _temp_simplification = None
    if sys.modules.get('simplification'):
        _temp_simplification = sys.modules['simplification']
    try:
        # Fake that the module is not available
        sys.modules['simplification'] = None    # type: ignore

        # Using RDP needs simplification module, so should give ImportError
        geometry_util.simplify_ext(
                geometry=sh_geom.LineString([(0, 0), (10, 10), (20, 20)]), 
                algorithm=geometry_util.SimplifyAlgorithm.RAMER_DOUGLAS_PEUCKER, 
                tolerance=1)
        assert True is False
    except ImportError as ex:
        assert True is True
    finally:
        if _temp_simplification:
            sys.modules['simplification'] = _temp_simplification
        else:
            del sys.modules['simplification']

if __name__ == '__main__':
    # Init
    tmpdir = test_helper.init_test_for_debug(Path(__file__).stem)

    #test_makevalid()
    #test_numberpoints()
    #test_remove_inner_rings()
    #test_simplify_ext_lang_basic()
    test_simplify_ext_lang_preservetopology()
    #test_simplify_ext_invalid()
    #test_simplify_ext_keep_points_on(tmpdir)
    #test_simplify_ext_no_simplification()
