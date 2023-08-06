from src.vyze.universe import parse_object_def, load_universe_from_file, load_universe_from_api, simplify_object_ident


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


def test_simplify_object_ident__1():
    assert simplify_object_ident('base.object/base', 'base') == 'object'
    assert simplify_object_ident('base.object/image', 'base') == 'base.object/image'
    assert simplify_object_ident('base.object', 'base') == 'object'
    assert simplify_object_ident('object', 'base') == 'object'


def test_simplify_object_ident__2():
    assert simplify_object_ident('base.object/base', 'data') == 'base.object'
    assert simplify_object_ident('base.object/image', 'data') == 'base.object/image'
    assert simplify_object_ident('base.object', 'data') == 'base.object'
    assert simplify_object_ident('object', 'data') == 'object'


def test_load_universe_from_file():
    universe = load_universe_from_file('./test_universe.yml')
    assert len(universe._description) > 0
    assert len(universe._models) > 0
    assert universe.get_model('base.object/fussball')
    verein = universe.get_model('verein')
    assert verein
    assert len(verein.fields) > 0
    url_field = verein.get_field('verein#url')
    assert url_field
    assert len(verein.field_names) > 0
    assert len(verein.description) > 0
    assert url_field.origin == verein
    assert url_field.target.name == 'verein@url'


def test_load_universe_from_api():
    universe = load_universe_from_api('data')
    assert len(universe.description) > 0
    assert len(universe.models) > 0
    assert universe.get_model('base.object/')
    assert universe.get_model('data.@data')
    assert universe.get_model('data.@integer')
    assert universe.get_model('data.@boolean')
    assert universe.get_model('data.@string')
    assert universe.get_model('data.@string').object
