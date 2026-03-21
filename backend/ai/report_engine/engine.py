from .schema_explorer import (
    SchemaIntrospector,
    SemanticModelAnalyzer,
    FactTableDetector,
)
from .graph import RelationshipGraphBuilder, GraphExpander
from .embeddings import EmbeddingDocumentGenerator, EmbeddingGeneratorWithOpenRouter
from .vector_store import FaissVectorStore
from .query_generation import (
    TableRetriever,
    SqlGenerator,
    QueryExecutor,
    QueryValidator,
)
from .context import ContextBuilder
from .embeddings import DocStringGenerator
from ai.handlers.open_router_handler import OpenRouterHandler
from db import DbEngine
import logging


logger = logging.getLogger(__name__)


class ReportEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        logging.info("Creating Report engine class")
        self.introspector = SchemaIntrospector()
        self.modelAnalyzer = SemanticModelAnalyzer()
        self.graphBuilder = RelationshipGraphBuilder()
        self.factTableDetector = FactTableDetector()
        self.embedding_doc_generator = EmbeddingDocumentGenerator()
        self.embedding_generator = EmbeddingGeneratorWithOpenRouter(
            embedding_model="openai/text-embedding-3-large"
        )
        self.sql_generator = SqlGenerator(OpenRouterHandler, "openai/o4-mini")
        self.docstring_generator = DocStringGenerator(
            OpenRouterHandler, "openai/o4-mini"
        )
        db_engine = DbEngine().engine
        query_validator = QueryValidator(["select"])
        self.query_exector = QueryExecutor(
            db_engine=db_engine, query_validator=query_validator
        )

        logging.info("Collecting Schema Data")
        schema_dict = self.introspector.get_schema()
        logging.info(f"Schema sample: {schema_dict['data'][100]}")
        schema_analysis = self.modelAnalyzer.generate_table_stats(schema_dict)
        relationship_graph = self.graphBuilder.build_graph(schema_dict["data"])

        self.graph_expander = GraphExpander(relationship_graph)
        fact_table_analysis = self.factTableDetector.generate_role_hint(
            schema_analysis, relationship_graph
        )
        # docstring_dict = docstring_generator.generate_doc_strings(schema_dict["data"])
        embedding_documents = self.embedding_doc_generator.generate_embedding_documents(
            schema_dict["data"], fact_table_analysis, {}
        )
        self.embedding_docs_dict = {}
        for doc in embedding_documents:
            self.embedding_docs_dict[doc["table_name"]] = doc

        self.context_builder = ContextBuilder(self.embedding_docs_dict)

        text_list = [doc["embedding_text"] for doc in embedding_documents]

        logging.info("Generating Embeddings")
        embedded_batch = self.embedding_generator.embed_batch(text_list)

        self.vector_store = FaissVectorStore(len(embedded_batch[0]))
        self.table_retriever = TableRetriever(
            self.embedding_generator, self.vector_store
        )
        self.vector_store.add_batch(embedded_batch, embedding_documents)
        logging.info("Class Initiation Succesful")

    def get_report_data(self, search_query, top_k=10):
        retrieved_tables = self.table_retriever.retrieve_tables(search_query, top_k)
        expanded_tables = self.graph_expander.expand_graph(retrieved_tables)
        context = self.context_builder.get_context(search_query, expanded_tables)
        sql = self.sql_generator.get_sql(context)
        data = self.query_exector.execute_query(search_query)
        return data


engine = ReportEngine()
