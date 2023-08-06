import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Field:

    def __init__(self, relation, origin, target):
        self.relation = relation
        self.origin = origin
        self.target = target

    def __str__(self):
        return str(self.relation)

    def __repr__(self):
        return f'Field {str(self.relation)}'


class Model:

    def __init__(self, name, base, target):
        self.name = name
        self.base = base
        self.target = target

        self.description = None
        self.object = None
        self.type = None

        self.abstracts = dict()
        self.specials = dict()

        self._fields = dict()
        self._field = None

    def get_field(self, field):
        ident = stringify_object_ident(field, self.base)
        return self._fields.get(ident)

    def get_field_names(self):
        return [str(f) for f in self._fields.values()]

    def __str__(self):
        return simplify_object_ident(f'{self.base}.{self.name}/{self.target}', self.target)

    def __repr__(self):
        return f'Model {str(self)}'


class Universe:

    def __init__(self, name):
        self.name = name

        self.description = None
        self.bases = None
        self.dependencies = None

        self._models = dict()

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


def load_universe(universe_def):
    def_struct = yaml.load(universe_def, Loader=Loader)
    universe = Universe(def_struct['name'])
    universe.description = def_struct['description']
    universe.bases = def_struct['bases']
    universe.dependencies = def_struct['dependencies']

    for object_def in def_struct['objects']:
        universe._add_object_def(object_def)

    for abstraction_def in def_struct['abstractions']:
        universe._add_abstraction_def(abstraction_def)

    for relation_def in def_struct['relations']:
        universe._add_relation_def(relation_def)

    universe.loaded = True

    return universe


def stringify_object_ident(name, target):
    name, base, target = parse_object_def(name, target)
    return f'{base}.{name}/{target}'


def simplify_object_ident(name, universe):
    name, base, target = parse_object_def(name, universe)
    if target == universe:
        if base == universe:
            return name
        else:
            return f'{base}.{name}'
    else:
        if target == base:
            return f'{base}.{name}'
        else:
            return f'{base}.{name}/{target}'


def parse_object_def(object_def, universe_name):
    split_a = object_def.split('/')
    base_part = split_a[0]
    split_b = base_part.split('.')

    if len(split_b) == 1:
        base = universe_name
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
            target = universe_name
        else:
            target = split_a[1]
    else:
        return None, None, None

    return name, base, target
