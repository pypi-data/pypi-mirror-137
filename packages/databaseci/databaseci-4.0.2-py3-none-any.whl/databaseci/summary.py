class Summary:
    @staticmethod
    def get_schema_summary(i):
        tables = []
        linkages = []

        for k, t in i.tables.items():

            if t.is_partitioning_child_table:
                continue
            indexes = [
                _
                for _ in i.indexes.values()
                if _.schema == t.schema and _.table_name == t.name
            ]

            indexes.sort(key=lambda x: (x.is_pk, x.is_unique), reverse=True)

            pks = [tuple(_.key_columns) for _ in indexes if _.is_unique]

            _t = (t.signature, [(c.name, c.dbtype) for c in t.columns.values()], pks)

            tables.append(_t)

        for k, x in i.constraints.items():
            if x.is_fk:
                t, other_t = (
                    x.quoted_full_table_name,
                    x.quoted_full_foreign_table_name,
                )

                if (
                    i.tables[t].is_partitioning_child_table
                    or i.tables[other_t].is_partitioning_child_table
                ):
                    continue

                cols = x.fk_columns_local
                cols_f = x.fk_columns_foreign

                tup_a = ("key", t, tuple(cols))
                tup_b = ("key", other_t, tuple(cols_f))

                linkages.append((tup_a, tup_b))

        return dict(tables=tables, linkages=linkages)
