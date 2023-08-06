import sys
from uuid import uuid4

from migra import Migration
from schemainspect import get_inspector
from sqlbag import S

from .call import get_response
from .conn import trans
from .copy import handle_copy_instruction
from .schema import create_fk_constraints, drop_fk_constraints, temporarily_dropped_fks
from .summary import Summary

# from . import results2


def do_copy(config: dict):
    safe_config = dict(config)
    real_db_url = safe_config.pop("real_db_url")
    copy_db_url = safe_config.pop("copy_db_url")

    with S(real_db_url) as s:
        summary = Summary.get_schema_summary(get_inspector(s))

    state = {}

    state["w"] = {_[0]: set() for _ in summary["tables"]}
    state["a"] = {_[0]: set() for _ in summary["tables"]}

    with S(real_db_url) as ss:
        with trans(ss.connection().connection) as t:

            with S(copy_db_url) as ssc:
                with trans(ssc.connection().connection) as tc:

                    i = get_inspector(ss)

                    m = Migration(ssc, i)
                    m.set_safety(False)
                    m.add_all_changes()
                    m.apply()

                    for c in drop_fk_constraints(i):
                        tc.ex(c)

            base = dict(inspected=summary, **safe_config)

            base["step"] = 0
            base["run_id"] = str(uuid4())

            result = {}

            with S(copy_db_url) as ssc:
                with trans(ssc.connection().connection) as tc:
                    while True:
                        req = {**base, **result}
                        response = get_response(req)

                        if not response.get("carry_on"):
                            print("Complete.")
                            break

                        handle_copy_instruction(response, config, state, t, tc)

                        result = dict(
                            done=response["step"],
                            step=response["step"],
                            stage=response.get("stage", 0),
                            s=dict(
                                w={k: len(v) for k, v in state["w"].items()},
                                a={k: len(v) for k, v in state["a"].items()},
                            ),
                        )

    with S(copy_db_url) as ssc:
        with trans(ssc.connection().connection) as tc:
            for c in create_fk_constraints(i):
                tc.ex(c)


def do_inspect(config: dict):
    raise NotImplementedError


def do_check(config: dict):
    safe_config = dict(config)

    print("Checking api_key:")

    try:
        req = dict(api_key=safe_config["api_key"], check="true")

    except LookupError:
        print("api_key not found in config file")
        sys.exit(1)

    from requests.exceptions import HTTPError

    try:
        resp = get_response(req)

        print("Connection successful - valid API key.")
        print()

    except HTTPError as e:
        if e.response.status_code == 403:
            print(
                "Access forbidden. Bad API key? If in doubt contact support@databaseci.com."
            )

        else:
            print(
                "Unknown error - Likely this is a server error, and we're investigating. For more details please contact support@databaseci.com."
            )

        sys.exit(1)

    real_db_url = safe_config.pop("real_db_url")
    copy_db_url = safe_config.pop("copy_db_url")

    print("Checking production database connectivity...")

    with S(real_db_url) as s:
        s.execute("select 1")

    print("Prod connection successful.")
    print()

    print("Checking copy/destination database connectivity...")

    with S(real_db_url) as s:
        s.execute("select 1")

    print("Copy/destination connection successful.")
    print()
