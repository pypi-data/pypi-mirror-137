from src.vyze.universe import parse_object_def, load_universe


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


def test_load_universe__1():
    with open('./test_universe.yml') as f:
        contents = f.read()
        universe = load_universe(contents)
        assert len(universe.description) > 0
        assert len(universe._models) > 0
        assert universe.get_model('base.object/fussball')
        verein = universe.get_model('verein')
        assert verein
        assert len(verein._fields) > 0
        assert verein.get_field('verein#url')
        print(verein.get_field_names())
    assert True
