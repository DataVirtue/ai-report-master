from schema_introspector import SchemaIntrospector
from semantic_model_analyzer import SemanticModelAnalyzer
from relationship_graph_builder import RelationshipGraphBuilder
from cluster_detector import ClusterDetector
from fact_table_detector import FactTableDetector
from embedding_document_generator import EmbeddingDocumentGenerator


def main():
    introspector = SchemaIntrospector()
    modelAnalyzer = SemanticModelAnalyzer()
    graphBuilder = RelationshipGraphBuilder()
    clusterDetector = ClusterDetector()
    factTableDetector = FactTableDetector()

    schema_dict = introspector.get_schema()
    print(schema_dict["data"][100])
    schema_analysis = modelAnalyzer.generate_table_stats(schema_dict)
    relationship_graph = graphBuilder.build_graph(schema_dict["data"])
    cluster = clusterDetector.get_clusters(relationship_graph)
    fact_table_analysis = factTableDetector.generate_role_hint(
        schema_analysis, relationship_graph
    )
    embedding_generator = EmbeddingDocumentGenerator()
    embedding_documents = embedding_generator.generate_embedding_documents(
        schema_dict["data"], fact_table_analysis
    )
    # print("*" * 1000)
    # print(schema_analysis[220])
    # print("*" * 1000)
    # print(relationship_graph)
    # print("*" * 1000)
    # print(cluster)
    # print("*" * 1000)
    # print(fact_table_analysis)
    # print("*" * 1000)
    sorted_data = dict(
        sorted(
            fact_table_analysis.items(),
            key=lambda item: 1 - item[1]["normalized_fact_score"],
        )
    )
    print(list(sorted_data.items())[0:10])
    print("*" * 100)
    for emb in embedding_documents[:10]:
        print(emb["embedding_text"])
    # print(embedding_documents[:10])


if __name__ == "__main__":
    main()
