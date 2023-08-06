from typing import Any

from ..error.illegal_attr_checker import IllegalAttrChecker
from ..query_runner.query_runner import QueryRunner, Row
from .graph_object import Graph


class GraphProjectRunner(IllegalAttrChecker):
    def __init__(self, query_runner: QueryRunner, namespace: str):
        self._query_runner = query_runner
        self._namespace = namespace

    def __call__(
        self, graph_name: str, node_spec: Any, relationship_spec: Any, **config: Any
    ) -> Graph:
        self._query_runner.run_query(
            f"CALL {self._namespace}($graph_name, $node_spec, $relationship_spec, $config)",
            {
                "graph_name": graph_name,
                "node_spec": node_spec,
                "relationship_spec": relationship_spec,
                "config": config,
            },
        )

        return Graph(graph_name, self._query_runner)

    def estimate(self, node_spec: Any, relationship_spec: Any, **config: Any) -> Row:
        self._namespace += ".estimate"
        result = self._query_runner.run_query(
            f"CALL {self._namespace}($node_spec, $relationship_spec, $config)",
            {
                "node_spec": node_spec,
                "relationship_spec": relationship_spec,
                "config": config,
            },
        )

        return result[0]

    @property
    def cypher(self) -> "GraphProjectRunner":
        return GraphProjectRunner(self._query_runner, self._namespace + ".cypher")

    def subgraph(
        self,
        graph_name: str,
        from_G: Graph,
        node_filter: str,
        relationship_filter: str,
        **config: Any,
    ) -> Graph:
        self._namespace += ".subgraph"
        self._query_runner.run_query(
            f"CALL {self._namespace}($graph_name, $from_graph_name, $node_filter, $relationship_filter, $config)",
            {
                "graph_name": graph_name,
                "from_graph_name": from_G.name(),
                "node_filter": node_filter,
                "relationship_filter": relationship_filter,
                "config": config,
            },
        )

        return Graph(graph_name, self._query_runner)
