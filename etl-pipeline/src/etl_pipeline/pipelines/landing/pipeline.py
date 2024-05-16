"""
This is a boilerplate pipeline 'landing'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, pipeline, node
from . import nodes

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=nodes.pass_data, 
            inputs="sql.customer",
            outputs="l.customer", 
            name="landing_customer"
        ),
        node(
            func=nodes.pass_data, 
            inputs="l.customer",
            outputs="i.customer", 
            name="integration_customer"
        )
    ])
