from src.vyze.universe import parse_object_def, load_universe_from_file, load_universe_from_api


def test_object_def__1():
    name, base, target = parse_object_def('object', 'base')
    assert name == 'object'
    assert base == 'base'
    assert target == 'base'


def test_object_def__2():
    name, base, target = parse_object_def('base.object', 'data')
    assert name == 'object'
    assert base == 'base'
    assert target == 'base'


def test_object_def__3():
    name, base, target = parse_object_def('base.object/', 'data')
    assert name == 'object'
    assert base == 'base'
    assert target == 'data'


def test_object_def__4():
    name, base, target = parse_object_def('base.object/user', 'data')
    assert name == 'object'
    assert base == 'base'
    assert target == 'user'


def test_load_universe_from_file():
    universe = load_universe_from_file('./test_universe.yml')
    assert len(universe.description) > 0
    assert len(universe._models) > 0
    assert universe.get_model('base.object/fussball')
    verein = universe.get_model('verein')
    assert verein
    assert len(verein._fields) > 0
    assert verein.get_field('verein#url')
    assert len(verein.get_field_names()) > 0
    assert len(verein.description) > 0


def test_load_universe_from_api():
    universe = load_universe_from_api('data')
    assert len(universe.description) > 0
    assert len(universe._models) > 0
    assert universe.get_model('base.object/')
    assert universe.get_model('data.@data')
    assert universe.get_model('data.@integer')
    assert universe.get_model('data.@boolean')
    assert universe.get_model('data.@string')
    assert universe.get_model('data.@string').object
