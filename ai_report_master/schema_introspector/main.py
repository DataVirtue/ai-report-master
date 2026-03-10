from schema_introspector import SchemaIntrospector
from semantic_model_analyzer import SemanticModelAnalyzer
from relationship_graph_builder import RelationshipGraphBuilder
from cluster_detector import ClusterDetector
from fact_table_detector import FactTableDetector
from embedding_document_generator import EmbeddingDocumentGenerator
from embedding_generator import EmbeddingGenerator
from vector_store import FaissVectorStore
from table_retriever import TableRetriever


def main():
    base_query = "Represent this query for retrieving relevant tables: "
    search_query_1 = base_query + "invoice series for sales"
    search_query_2 = base_query + "top 10 distributors"

    introspector = SchemaIntrospector()
    modelAnalyzer = SemanticModelAnalyzer()
    graphBuilder = RelationshipGraphBuilder()
    clusterDetector = ClusterDetector()
    factTableDetector = FactTableDetector()
    embedding_doc_generator = EmbeddingDocumentGenerator()
    embedding_generator = EmbeddingGenerator()
    vector_store = FaissVectorStore(embedding_generator.dimension())
    table_retriever = TableRetriever(embedding_generator, vector_store)
    schema_dict = introspector.get_schema()
    print(schema_dict["data"][100])
    schema_analysis = modelAnalyzer.generate_table_stats(schema_dict)
    relationship_graph = graphBuilder.build_graph(schema_dict["data"])
    cluster = clusterDetector.get_clusters(relationship_graph)
    fact_table_analysis = factTableDetector.generate_role_hint(
        schema_analysis, relationship_graph
    )
    embedding_documents = embedding_doc_generator.generate_embedding_documents(
        schema_dict["data"], fact_table_analysis
    )
    text_list = [doc["embedding_text"] for doc in embedding_documents]

    embedded_batch = embedding_generator.embed_batch(text_list)

    # for i in range(len(embedding_documents)):
    #     doc = embedding_documents[i]
    #     vector = embedded_batch[i]
    #     vector_store.add(vector, doc)
    #
    vector_store.add_batch(embedded_batch, embedding_documents)
    print(embedded_batch)

    # print("*" * 1000)
    # print(schema_analysis[220])
    # print("*" * 1000)
    # print(relationship_graph)
    # print("*" * 1000)
    # print(cluster)
    # print("*" * 1000)
    # print(fact_table_analysis)
    # print("*" * 1000)
    # sorted_data = dict(
    #     sorted(
    #         fact_table_analysis.items(),
    #         key=lambda item: 1 - item[1]["normalized_fact_score"],
    #     )
    # )
    # print(list(sorted_data.items())[0:10])
    # print("*" * 100)
    # for emb in embedding_documents[:10]:
    #     print(emb["embedding_text"])
    # print("*" * 100)
    # search_vector = embedding_generator.embed_text(search_query_1)
    # print(search_query_1, vector_store.search(search_vector))
    # search_vector = embedding_generator.embed_text(search_query_2)
    # print("*" * 100)
    # print(search_query_2, vector_store.search(search_vector))
    print(table_retriever.retrieve_tables(search_query_1))


if __name__ == "__main__":
    main()
