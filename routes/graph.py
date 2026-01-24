from fastapi import APIRouter, HTTPException
import os
from config import VAULT, init_vault
from utils import clean_dataframe_for_json

router = APIRouter(tags=["Graph"])


@router.get("/graph")
async def get_graph():
    """Endpoint principal: retorna nós e arestas para o gráfico"""
    try:
        vault = init_vault()
    except Exception as e:
        return {"nodes": [], "edges": [], "error": str(e)}

    try:
        g = vault.graph

        nodes = []
        edges = []

        for node_id in g.nodes():
            nodes.append(
                {
                    "id": node_id,
                    "label": os.path.splitext(node_id)[0],
                    "size": g.degree(node_id) + 3,
                }
            )

        for source, target in g.edges():
            edges.append(
                {"id": f"{source}-{target}", "source": source, "target": target}
            )

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {"total_notes": len(nodes), "total_links": len(edges)},
        }

    except Exception as e:
        return {"nodes": [], "edges": [], "error": str(e)}
