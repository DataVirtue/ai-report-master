from schema_introspector import SchemaIntrospector
from semantic_model_analyzer import SemanticModelAnalyzer


def main():
    introspector = SchemaIntrospector()
    modelAnalyzer = SemanticModelAnalyzer()

    schema_dict = introspector.get_schema()
    print(schema_dict["data"][220])
    schema_analysis = modelAnalyzer.generate_table_stats(schema_dict)
    print("*" * 1000)
    print(schema_analysis[220])


if __name__ == "__main__":
    main()
