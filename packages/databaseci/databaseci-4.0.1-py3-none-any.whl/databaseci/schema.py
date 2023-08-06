from contextlib import contextmanager


def drop_fk_constraints(i):
    statements = []
    for k, x in i.constraints.items():
        if x.is_fk:
            statements.append(x.drop_statement)
    return statements


def create_fk_constraints(i):
    statements = []
    for k, x in i.constraints.items():
        if x.is_fk:
            statements.append(x.create_statement)
    return statements


@contextmanager
def temporarily_dropped_fks(db, i=None):
    if i is None:
        i = db.inspect()

    with db.transaction() as t:
        for st in drop_fk_constraints(i):
            t.ex(st)

    yield

    with db.transaction() as t:
        for st in create_fk_constraints(i):
            t.ex(st)
