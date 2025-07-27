# run_validation.py

from great_expectations.data_context import get_context
from great_expectations.core.batch import RuntimeBatchRequest

def run_validation(file_path: str, suite_name: str = "employees_suite") -> bool:
    context = get_context(context_root_dir="gx")

    # 1. Add datasource
    context.add_datasource(
        name="local_filesystem",
        class_name="Datasource",
        execution_engine={"class_name": "PandasExecutionEngine"},
        data_connectors={
            "default_runtime_data_connector_name": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["default_identifier_name"]
            }
        }
    )

    # 2. Load or create suite
    try:
        suite = context.get_expectation_suite(suite_name)
    except Exception:
        suite = context.create_expectation_suite(suite_name)

    # 3. Create batch request
    batch_request = RuntimeBatchRequest(
        datasource_name="local_filesystem",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="employees_csv",
        runtime_parameters={"path": file_path},
        batch_identifiers={"default_identifier_name": "default_id"}
    )

    validator = context.get_validator(batch_request=batch_request, expectation_suite=suite)

    # 4. Define expectations (can be moved to a separate function if needed)
    validator.expect_column_to_exist("employee_id")
    validator.expect_column_values_to_not_be_null("employee_id")
    validator.expect_column_values_to_be_unique("employee_id")
    validator.expect_column_values_to_not_be_null("age")
    validator.expect_column_values_to_be_between("age", min_value=20, max_value=60)

    # 5. Save expectations
    validator.save_expectation_suite(discard_failed_expectations=False)

    # 6. Register checkpoint
    context.add_or_update_checkpoint(
        name="employees_checkpoint",
        config_version=1.0,
        class_name="Checkpoint",
        validations=[
            {
                "batch_request": batch_request.to_dict(),
                "expectation_suite_name": suite_name,
            }
        ]
    )

    # 7. Run validation
    results = context.run_checkpoint(checkpoint_name="employees_checkpoint")
    return results["success"]
