BATCH_SIZE = 1000

from console.utils import clear_lines

from .paging import get_page
from .util import batched

pl = 0


def q(x):
    x = x.replace("'", "''")
    return f"'{x}'"


def ft(t):
    if not t:
        return "Empty."

    k = list(t[0])

    ttt = [str(type(_).__name__) for _ in t[0].values()]
    print(t)
    st = [{k: str(v) for k, v in r.items()} for r in t]

    st.insert(0, {k: k.upper() for k in k})

    w = {_: 0 for _ in k}

    for r in st:
        for kk in k:
            l = len(r[kk])
            if w[kk] < l:
                w[kk] = l

    for r in st:
        for tt, kk in zip(ttt, k):
            ww = w[kk]

            s = r[kk]

            if tt == "str":
                r[kk] = s.ljust(ww)

            else:
                r[kk] = s.rjust(ww)

    return "\n".join(" ".join(x.values()) for x in st)


def print_status(s):
    if pl:
        clear_lines(pl)

    a = s["a"]

    w = s["w"]

    t = list(set(w) | set(a))

    t.sort()

    rows = [
        dict(table=tt, loaded=len(a[tt]), chosen=len(w[tt]))
        for tt in t
        if a[tt] or w[tt]
    ]

    t = ft(rows)


def kfr(rows, pksi, exclude):

    if len(pksi) == 1:
        k = pksi[0]
        return set(x for row in rows if (x := row[k]) not in exclude and x is not None)

    return set(
        x
        for row in rows
        if (x := tuple(row[k] for k in pksi)) not in exclude and None not in x
    )


def kfr2(rows, pksi, exclude):

    if len(pksi) == 1:
        k = pksi[0]

        a, b = set(), []

        for r in rows:
            if (x := r[k]) not in exclude and x is not None:
                a.add(x)
                b.append(r)

        return a, b

    a, b = set(), []

    for r in rows:
        if (x := tuple(r[k] for k in pksi)) not in exclude and None not in x:
            a.add(x)
            b.append(r)

    return a, b


def do_select_instruction(i, t, tc, s):
    q = i["q"]

    bookmark = None

    while True:
        rows = get_page(
            t,
            q,
            ordering=",".join(i["pks"]),
            per_page=BATCH_SIZE,
            backwards=False,
            bookmark=bookmark,
        )

        if rows:
            a, r = kfr2(rows, i["pksi"], exclude=s["a"][i["table"]])

            if r:

                tc.insert(i["table"], r)
                # print('.')

            s["a"][i["table"]] |= a
            s["w"][i["table"]] -= a

            for l, o, ii in i["lo"]:

                kk = kfr(rows, ii, exclude=s["a"][l])
                s["w"][l] |= kk

            for aa, bb in zip(i["li"], i["qq"]):
                l, i, p, ii = aa
                do_inwards(t, l, i, a, s, p, bb, ii)

            print_status(s)

        if not rows.paging.has_next:
            break
    print_status(s)


def paramspec(batch, x):
    def ff(n):
        return f"%({n})s"

    def r(batch):
        its = []

        if x > 1:
            for i, _ in enumerate(batch):
                v = ",".join(ff(f"ppp{i}_{j}") for j in range(x))
                v = f"({v})"
                its.append(v)
        else:
            for i, _ in enumerate(batch):
                v = ff(f"ppp{i}")
                v = f"({v})"
                its.append(v)

        return ", ".join(its)

    return f"""
    
select * from (values {r(batch)})
    """


def paramd(batch, x):
    d = {}

    for i, b in enumerate(batch):
        if x > 1:
            for j in range(x):
                k = f"ppp{i}_{j}"
                d[k] = b[j]
        else:
            k = f"ppp{i}"
            d[k] = b

    return d


def do_select_instruction2(i, t, tc, s):
    w = s["w"][i["table"]]

    if w:
        for batch in batched(w, size=BATCH_SIZE):

            x = len(i["pks"])
            q = i["q"]
            q = q.format(paramspec(batch, x))
            bookmark = None

            while True:

                d = paramd(batch, x)

                rows = get_page(
                    t,
                    q,
                    paramd(batch, x),
                    ordering=",".join(i["pks"]),
                    per_page=BATCH_SIZE,
                    backwards=False,
                    bookmark=bookmark,
                )

                if rows:
                    a, r = kfr2(rows, i["pksi"], exclude=s["a"][i["table"]])

                    if r:

                        tc.insert(i["table"], r)
                        print(".")

                    s["a"][i["table"]] |= a
                    s["w"][i["table"]] -= a

                    for l, o, ii in i["lo"]:

                        kk = kfr(rows, ii, exclude=s["a"][l])

                        s["w"][l] |= kk

                    for aa, bb in zip(i["li"], i["qq"]):
                        l, i, p, ii = aa
                        do_inwards(t, l, i, a, s, p, bb, ii)

                    print_status(s)

                if rows.paging.has_next:
                    bookmark = rows.paging.next
                else:
                    break


def do_inwards(t, l, i, a, s, p, b, ii):

    if not a:
        return

    for batch in batched(a, size=BATCH_SIZE):

        bookmark = None

        qq = b

        x = len(i)

        qq = qq.format(paramspec(batch, x))

        while True:

            rows = get_page(
                t,
                qq,
                paramd(batch, x),
                ordering=",".join(p),
                per_page=BATCH_SIZE,
                backwards=False,
                bookmark=bookmark,
            )

            if rows:
                a = kfr(rows, ii, exclude=s["a"][l])

                s["w"][l] |= a

            if rows.paging.has_next:
                bookmark = rows.paging.next
            else:
                break


def handle_copy_instruction(instruction, config, state, t, tc):
    real_db_url = config.get("real_db_url")
    copy_db_url = config.get("copy_db_url")

    if instruction["stage"] == 0:

        if instruction["command"] == "sel":
            do_select_instruction(instruction, t, tc, state)

    elif instruction["stage"] == 1:
        if instruction["command"] == "sel":
            do_select_instruction2(instruction, t, tc, state)

    else:
        raise ValueError("Server error - invalid instructions.")
