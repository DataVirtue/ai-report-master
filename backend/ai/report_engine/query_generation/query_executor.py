import logging
from typing import Dict, Tuple, List
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError


class QueryExecutor:
    def __init__(self, db_engine, query_validator):
        self.db_engine = db_engine
        self.query_validator = query_validator

    def execute_query(self, query) -> Tuple[List, bool, str]:
        is_valid, reason = self.query_validator.validate_query(query)
        if not is_valid:
            return [], False, reason

        with self.db_engine.connect() as connection:
            try:
                result_proxy = connection.execute(text(query))
                keys = list(result_proxy.keys())
                results = result_proxy.fetchall()
                # An empty result set is a valid, successful query, not an error.
                data = [dict(zip(keys, row, strict=False)) for row in results]
                return data, True, ""

            except DBAPIError as e:
                logging.error(f"Could not execute query {e}")
                return [], False, f"Query Failed with error {e}"

    def execute_query_with_pagination(
        self, query, items_per_page, offset
    ) -> Tuple[List, bool, str]:
        is_valid, reason = self.query_validator.validate_query(query)
        if not is_valid:
            return [], False, reason

        # Guard against invalid pagination bounds (e.g. page_no <= 0 upstream
        # produces a negative offset, which Postgres rejects outright).
        if items_per_page <= 0 or offset < 0:
            return [], False, "Pagination bounds are invalid"

        # The stored query has no LIMIT/OFFSET of its own, so wrap it as a
        # subquery and apply pagination to it. Without this wrapper the bound
        # params are never referenced and every page returns the full result.
        # inner_query is app-generated SQL already restricted to SELECT by the
        # validator above, so the composed statement is not user-tainted.
        inner_query = query.strip().rstrip(";")
        paginated_query = (  # noqa: S608 - inner_query is validated, select-only app SQL
            f"SELECT * FROM ({inner_query}) AS paginated_subquery "
            "LIMIT :limit OFFSET :offset"
        )

        with self.db_engine.connect() as connection:
            try:
                result_proxy = connection.execute(
                    text(paginated_query),
                    {"limit": items_per_page, "offset": offset},
                )
                keys = list(result_proxy.keys())
                results = result_proxy.fetchall()
                # An empty page is a valid, successful query, not an error.
                data = [dict(zip(keys, row, strict=False)) for row in results]
                return data, True, ""

            except DBAPIError as e:
                logging.error(f"Could not execute query {e}")
                return [], False, f"Query Failed with error {e}"
