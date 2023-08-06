import requests
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Field:
    """
    Represents a VYZE field.
    """

    def __init__(self, relation, origin, target):
        self._relation = relation
        self._origin = origin
        self._target = target

    @property
    def type(self):
        return None

    @property
    def relation(self):
        return self._relation

    @property
    def origin(self):
        return self._origin

    @property
    def target(self):
        return self._target

    def __str__(self):
        return str(self._relation)

    def __repr__(self):
        return f'Field {str(self._relation)}'


class Model:
    """
    Represents a VYZE model.
    """

    def __init__(self, name, base, target):
        self._name = name
        self._base = base
        self._target = target

        self._description = None
        self._object = None
        self._type = None

        self._abstracts = dict()
        self._specials = dict()

        self._fields = dict()
        self._field = None

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def object(self):
        return self._object

    @property
    def type(self):
        return self._type

    @property
    def abstracts(self):
        return self._abstracts

    @property
    def specials(self):
        return self._specials

    @property
    def fields(self):
        return self._fields.values()

    @property
    def field_names(self):
        return [str(f) for f in self._fields.values()]

    @property
    def fq_name(self):
        """
        Returns:
            The fully qualified name of the model of the form `base.name/target`.
        """
        return f'{self._base}.{self._name}/{self._target}'

    @property
    def scoped_name(self):
        """
        Returns:
            The name of the model usually only valid in its target universe.
        """
        return stringify_object_ident(self.fq_name, self._target)

    def get_field(self, field):
        ident = stringify_object_ident(field, self._base)
        return self._fields.get(ident)

    def __str__(self):
        return simplify_object_ident(f'{self._base}.{self._name}/{self._target}', self._target)

    def __repr__(self):
        return f'Model {str(self)}'


class Universe:
    """
    Represents a VYZE universe.
    """

    def __init__(self, name):
        self._name = name

        self._description = None
        self._bases = None
        self._dependencies = None

        self._models = dict()

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def bases(self):
        return self._bases

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def models(self):
        return self._models.values()

    def get_model(self, model):
        ident = stringify_object_ident(model, self.name)
        return self._models.get(ident)

    def _add_object_def(self, object_def):
        name, base, target = parse_object_def(object_def, self.name)
        model = Model(name, base, target)
        self._models[f'{base}.{name}/{target}'] = model
        return model

    def _add_abstraction_def(self, abstraction_def):
        split_abs = abstraction_def.split(':')

        name_a, base_a, target_a = parse_object_def(split_abs[0], self.name)
        ident_a = f'{base_a}.{name_a}/{target_a}'
        abstract = self._models.get(ident_a)
        if not abstract:
            raise RuntimeError(f'missing abstract: {ident_a}')

        name_b, base_b, target_b = parse_object_def(split_abs[1], self.name)
        ident_b = f'{base_b}.{name_b}/{target_b}'
        special = self._models.get(ident_b)
        if not special:
            raise RuntimeError(f'missing special: {ident_b}')

        abstract.specials[ident_b] = special
        special.abstracts[ident_a] = abstract

    def _add_relation_def(self, relation_def):
        split_rel = relation_def.split(':')

        name_a, base_a, target_a = parse_object_def(split_rel[0], self.name)
        ident_a = f'{base_a}.{name_a}/{target_a}'
        relation = self._models.get(ident_a)
        if not relation:
            raise RuntimeError(f'missing relation: {ident_a}')

        name_b, base_b, target_b = parse_object_def(split_rel[1], self.name)
        ident_b = f'{base_b}.{name_b}/{target_b}'
        origin = self._models.get(ident_b)
        if not origin:
            raise RuntimeError(f'missing origin: {ident_b}')

        name_c, base_c, target_c = parse_object_def(split_rel[2], self.name)
        ident_c = f'{base_c}.{name_c}/{target_c}'
        target = self._models.get(ident_c)
        if not target:
            raise RuntimeError(f'missing target: {ident_c}')

        field = Field(relation, origin, target)

        relation._field = field
        origin._fields[ident_a] = field

    def __repr__(self):
        return f'Universe {self.name}'


def load_universe_from_api(universe_name, url='https://api.vyze.io/app/'):
    """
    Loads a universe, its models, fields and values from the VYZE API.

    Args:
        universe_name: Name of the universe.
        url: URL of the VYZE API.

    Returns:
        A universe object if successful or None otherwise.
    """

    resp = requests.get(f'{url}universe/resolve/{universe_name}')
    if resp.status_code != 200:
        return None
    universe_id = resp.json()
    resp = requests.get(f'{url}universe/{universe_id}/export?o=1')
    if resp.status_code != 200:
        return None
    universe_def = resp.content
    return load_universe(universe_def)


def load_universe_from_file(filepath):
    """
    Loads a universe, its models, fields and values from a definition file.

    Args:
        filepath: Path of the definition file.

    Returns:
        A universe object if successful or None otherwise.
    """

    with open(filepath) as f:
        contents = f.read()
        return load_universe(contents)


def load_universe(universe_def):
    def_struct = yaml.load(universe_def, Loader=Loader)
    universe = Universe(def_struct['name'])
    universe._description = def_struct['description']
    universe._bases = def_struct['bases']
    universe._dependencies = def_struct['dependencies']

    for object_def in def_struct['objects']:
        universe._add_object_def(object_def)

    for info in def_struct['info']:
        mapping = info['mapping']
        model = universe.get_model(mapping)
        if not model:
            continue
        model._description = info['description']
        model._type = info['type']
        model._object = info.get('object')

    for abstraction_def in def_struct['abstractions']:
        universe._add_abstraction_def(abstraction_def)

    for relation_def in def_struct['relations']:
        universe._add_relation_def(relation_def)

    universe.loaded = True

    return universe


def stringify_object_ident(name, target):
    name, base, target = parse_object_def(name, target)
    return f'{base}.{name}/{target}'


def simplify_object_ident(name, universe=None):
    """
        Creates a simplified, scoped name for the given model name.

        - `model_name`, if the model entirely resides in this universe
        - `base_universe.model_name/`, if the model was copied from the universe `base_universe`
        - `base_universe.model_name`, if the model entirely resides in the universe `base_universe`
        - `base_universe.model_name/target_universe`, if the model was copied from the universe `base_universe` and resides in the universe `target_universe`
    Args:
        name: model identifier of any form
        universe: scope of the identifier

    Returns:
        A scoped model identifier.
    """

    name, base, target = parse_object_def(name, universe)

    if universe and target == universe:
        if base == universe:
            return name
        else:
            return f'{base}.{name}'
    else:
        if target == base:
            return f'{base}.{name}'
        else:
            return f'{base}.{name}/{target}'


def parse_object_def(object_def, universe_scope=None):
    """
    Parses an object identifier. If the object identifier is scoped it usually requires a universe scope.

    Args:
        object_def: The object identifier.
        universe_scope: Universe name of the universe serving as scope.

    Returns:
        A triple `name`, `base`, `target` representing the name, base and target of the identifier.
    """

    split_a = object_def.split('/')
    base_part = split_a[0]
    split_b = base_part.split('.')

    if len(split_b) == 1:
        if not universe_scope:
            raise RuntimeError('requires universe scope')
        base = universe_scope
        name = split_b[0]
    elif len(split_b) == 2:
        base = split_b[0]
        name = split_b[1]
    else:
        return None, None, None

    if len(split_a) == 1:
        target = base
    elif len(split_a) == 2:
        if split_a[1] == '':
            if not universe_scope:
                raise RuntimeError('requires universe scope')
            target = universe_scope
        else:
            target = split_a[1]
    else:
        return None, None, None

    return name, base, target
