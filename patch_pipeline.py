import re

with open("src/coreason_etl_civic/pipeline.py", "r") as f:
    content = f.read()

new_content = content.replace(
    """from coreason_etl_civic.utils.logger import logger""",
    """from dlt.helpers.dbt.runner import create_runner\n\nfrom coreason_etl_civic.utils.logger import logger"""
)

new_logic = """    load_info = pipeline.run(
        [
            genes,
            variants,
            evidence,
        ],
    )

    logger.info("CIViC DLT Pipeline Completed", load_info=str(load_info))

    logger.info("Starting dbt transformations")
    from dlt.common.runners import Venv
    from dlt.common.destination.client import DestinationClientDwhConfiguration
    from typing import cast
    venv = Venv.restore_current()
    client_config = cast(DestinationClientDwhConfiguration, pipeline.destination_client().config)
    dbt = create_runner(
        venv,
        client_config,
        pipeline.working_dir,
        package_location="dbt/coreason_etl_civic"
    )
    dbt_results = dbt.run_all()
    logger.info("dbt transformations completed")
    for r in dbt_results:
        logger.info(f"dbt result: {r.model_name} -> {r.status}")"""

old_logic = """    load_info = pipeline.run(
        [
            genes,
            variants,
            evidence,
        ],
    )

    logger.info("CIViC DLT Pipeline Completed", load_info=str(load_info))"""

new_content = new_content.replace(old_logic, new_logic)

with open("src/coreason_etl_civic/pipeline.py", "w") as f:
    f.write(new_content)
