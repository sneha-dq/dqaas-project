from great_expectations.data_context import get_context
from great_expectations.core.batch import BatchRequest
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.core.batch import RuntimeBatchRequest

# Step 1: Get the context
context = get_context(context_root_dir="gx")

# Step 2: Define (and register) a datasource pointing to the local data folder
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

# Step 3: Create (or load) the expectation suite
suite_name = "employees_suite"
try:
    suite = context.get_expectation_suite(suite_name)
except:
    suite = context.create_expectation_suite(suite_name)

# Step 4: Load the data
batch_request = RuntimeBatchRequest(
    datasource_name="local_filesystem",
    data_connector_name="default_runtime_data_connector_name",
    data_asset_name="employees_csv",
    runtime_parameters={"path": "data/employees.csv"},
    batch_identifiers={"default_identifier_name": "default_id"}
)

validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite=suite
)

# Step 5: Define expectations via code
validator.expect_column_to_exist("employee_id")
validator.expect_column_values_to_not_be_null("employee_id")
validator.expect_column_values_to_be_unique("employee_id")
validator.expect_column_values_to_not_be_null("age")
validator.expect_column_values_to_be_between("age", min_value=20, max_value=60)

# Step 6: Save the suite
validator.save_expectation_suite(discard_failed_expectations=False)

# Step 7: Create or update a checkpoint
context.add_or_update_checkpoint(
    name="employees_checkpoint",
    config_version=1.0,
    class_name="Checkpoint",
    validations=[
        {
            "batch_request": batch_request.to_dict(),  # <-- Convert to dict here
            "expectation_suite_name": suite_name,
        }
    ]
)

# Step 8: Run the checkpoint
results = context.run_checkpoint(checkpoint_name="employees_checkpoint")

if results["success"]:
    print("✅ Data validation passed.")
else:
    print("❌ Data validation failed.")
