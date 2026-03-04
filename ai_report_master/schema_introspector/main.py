from schema_introspector import SchemaIntrospector


def main():
    introspector = SchemaIntrospector()
    schema_dict = introspector.get_schema()
    print(schema_dict["data"][220])


if __name__ == "__main__":
    main()
