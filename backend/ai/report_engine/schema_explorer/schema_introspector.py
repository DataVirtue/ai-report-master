from typing import Dict, List
from sqlalchemy import inspect
from db import DbEngine


class SchemaIntrospector:
    schema = "public"
    ignore_table_containing = [
        "auth",
        "django",
        "migration",
        "historical",
        "counter",
        "token",
        "permissionsrole",
        "importer",
        "otp",
        "machine",
        "history",
    ]
    ignore_table_exact = []

    def __init__(self) -> None:
        self.engine = DbEngine().engine
        self.inspector = inspect(self.engine)

    def set_ignore_tables(self, table_name_list: List) -> None:
        self.ignore_table_exact = table_name_list

    def set_ignore_tables_containing(self, table_name_contains_list: List) -> None:
        self.ignore_table_containing = table_name_contains_list

    def get_ignore_tables(self) -> List:
        return self.ignore_table_exact

    def get_ignore_tables_containing(self) -> List:
        return self.ignore_table_containing

    def _check_any_match(self, string, possible_contain_matches):
        for exp in possible_contain_matches:
            if exp in string:
                return True
        return False

    def parse_foreign_key_dict(self, foreign_keys: List) -> Dict:
        result = {}
        if len(foreign_keys) <= 0:
            return result
        for fk_dict in foreign_keys:
            for col in fk_dict["constrained_columns"]:
                result[col] = {
                    "referred_schema": fk_dict["referred_schema"],
                    "referred_table": fk_dict["referred_table"],
                    "referred_columns": fk_dict["referred_columns"],
                    "is_composite_foreign_key": len(fk_dict["constrained_columns"]) > 1,
                }
        return result

    def get_sematic_column_type(self, column_type_name: str) -> str:
        if column_type_name in [
            "integer",
            "decimal",
            "float",
            "numeric",
            "smallint",
            "double_precision",
            "real",
        ]:
            return "numeric"

        if column_type_name in ["string", "text", "varchar", "char"]:
            return "text"

        if "varchar" in column_type_name:
            return "text"

        if column_type_name in ["timestamp", "timestamptz", "datetime"]:
            return "datetime"

        if column_type_name in ["date"]:
            return "date"

        if column_type_name in ["boolean"]:
            return "boolean"

        if column_type_name in ["json"]:
            return "json"

        return "other"

    def parse_column_data(
        self, columns: List, primary_key: Dict, foreign_keys: Dict
    ) -> List:
        results = []
        for column in columns:
            composite_primary_key = False
            is_primary_key = False
            col_name = column["name"]
            col_type = str(column["type"]).lower()
            if len(primary_key["constrained_columns"]) > 1:
                composite_primary_key = True
            if col_name in primary_key["constrained_columns"]:
                is_primary_key = True

            results.append(
                {
                    "name": col_name,
                    "type": col_type,
                    "semantic_type": self.get_sematic_column_type(col_type),
                    "nullable": column["nullable"],
                    "is_primary_key": is_primary_key,
                    "part_of_composite_primary_key": composite_primary_key,
                    "is_foreign_key": col_name in foreign_keys,
                    "referred_schema": foreign_keys[col_name]["referred_schema"]
                    if col_name in foreign_keys
                    else "",
                    "referred_table": foreign_keys[col_name]["referred_table"]
                    if col_name in foreign_keys
                    else "",
                    "referred_columns": foreign_keys[col_name]["referred_columns"]
                    if col_name in foreign_keys
                    else "",
                }
            )
        return results

    def get_relationships(self, current_table: str, column_data: list) -> List:
        result = []
        for column in column_data:
            if not column.get("is_foreign_key"):
                continue
            result.append(
                {
                    "table_name": column["referred_table"],
                    "on_columns": column["referred_columns"],
                    "fk_column": column["name"],
                    "base_table": current_table,
                }
            )
        return result

    def get_schema(self) -> Dict:
        schema_dict = {}
        table_names = self.inspector.get_table_names(self.schema)

        print("total tables", len(table_names))

        if len(self.ignore_table_exact) != 0:
            table_names = [
                name for name in table_names if name not in self.ignore_table_exact
            ]

        print("total tables after exact filter", len(table_names))
        if len(self.ignore_table_containing) != 0:
            table_names = [
                name
                for name in table_names
                if not self._check_any_match(name, self.ignore_table_containing)
            ]

        print("total tables after contains filter", len(table_names))
        schema_dict["data"] = []
        max_columns = 0
        max_column_table_name = ""
        for table_name in table_names:
            columns = self.inspector.get_columns(table_name, schema=self.schema)
            primary_keys = self.inspector.get_pk_constraint(table_name)
            foreign_keys = self.inspector.get_foreign_keys(table_name)
            parsed_foreign_key_dict = self.parse_foreign_key_dict(foreign_keys)
            columns_list = self.parse_column_data(
                columns, primary_keys, parsed_foreign_key_dict
            )
            relationship = self.get_relationships(table_name, columns_list)
            max_columns = max(max_columns, len(columns))
            if max_columns == len(columns):
                max_column_table_name = table_name
            schema_dict["data"].append(
                {
                    "table_name": table_name,
                    "columns": columns_list,
                    "relationships": relationship,
                }
            )

        print("Max Number of columns", max_columns, "Table Name", max_column_table_name)
        return schema_dict
