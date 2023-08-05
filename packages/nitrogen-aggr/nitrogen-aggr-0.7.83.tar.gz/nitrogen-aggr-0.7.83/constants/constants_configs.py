# project
class Config:
    """
     the structure of self.config file
    """

    STEP_CONFIG = "step_config"
    ARGS = "args"
    PROJECT_CONFIG = "project_config"
    STEP_NAME = "step_name"
    CLIENT = "client"
    WORKFLOW = "workflow"
    USER = "user"
    FRAMEWORK = "framework"
    ENV = "env"
    JOB_ID = "job_id"
    LOG_LEVEL = "log_level"
    SSD_JOB_ID = "ssd_job_id"
    AWS_KEY = "awskey"
    AWS_SECRET = "awssecret"
    VAULT_KEY = "vault_key"
    VAULT_METADATA = "vault_metadata"
    PROJECT_TEST = "project_test.yaml"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT_FILENAME = "%Y%m%dT%H%M%S "
    FISCAL_MONTH_END = "fiscal_month_end"
    CURRENT_YEAR = "current_year"
    PROJECT_ROOT_PATH = "project_root_path"
    CLIENT2 = "client2"
    CMS_LOCATION = "cms_location"
    NPI_PARQUET_LOCATION = "npi_parquet_location"
    LOCATION_MASTER = "master_location"
    LOCATION_SSD = "ssd_location"
    LOCATION_AGGR = "aggr_location"
    LOCATION_REFERENCE = "reference_location"
    LOCATION_REPORT = "report_location"
    PARENT_DEMO_CLIENT = "parent_demo_client"

## project_test
class ProjectTest:
    AWS_TEST_DIRECTORY = "aws_test_directory"
    AWS_TEST_DIRECTORY_BUCKET = "bucket"
    AWS_TEST_DIRECTORY_BASE_KEY = "base_key"

    TEST_DATA_FACTORY = "test_data_factory"
    TEST_DATA_FACTORY_FRACTION = "fraction"
    TEST_DATA_FACTORY_LIMIT = "limit"

    TEST_ETL_JOB = "test_etl_job"
    TEST_ETL_JOB_JOBS = "jobs"
