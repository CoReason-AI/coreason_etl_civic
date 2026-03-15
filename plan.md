1.  **Decompose and select the first atomic unit.**
    - The task is to build a configuration object to hold the CIViC API Base URL, target files, and other constants.
    - I will create `src/coreason_etl_civic/config.py` with a Pydantic `BaseSettings` class following the naming conventions (e.g., `EpistemicCivicPolicy` or `EpistemicCivicManifest`).
    - The object will include fields: `civic_nightly_base_url`, `gene_summaries_file`, `variant_summaries_file`, `clinical_evidence_summaries_file`.

2.  **Verify the creation of `src/coreason_etl_civic/config.py`.**
    - I will run `cat src/coreason_etl_civic/config.py` to ensure the file was created and contains the correct code.

3.  **Create tests for the configuration object in `tests/test_config.py`.**
    - I will create `tests/test_config.py` containing test functions to verify the default values of `EpistemicCivicPolicy` and the ability to override them using environment variables.
    - I will also add property-based testing using `hypothesis` as mandated by `AGENTS.md`.

4.  **Verify the creation of `tests/test_config.py` and run tests.**
    - I will run `cat tests/test_config.py` to ensure the file was created.
    - I will run `uv run pytest tests/test_config.py` to verify the new tests pass.

5.  **Run the full test suite.**
    - I will run `uv run pytest` to ensure all pre-existing and newly added tests pass successfully and there are zero regressions.

6.  **Complete pre commit steps.**
    - Complete pre commit steps to make sure proper testing, verifications, reviews and reflections are done.

7.  **Submit the change.**
    - I will submit the change for this single atomic unit.
