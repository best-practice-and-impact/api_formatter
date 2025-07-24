from src.config_objects import MetadataConfig, COMBINED_DEFAULT


#Testing
schema_path=r"data/Schema/CombinedSchema.json"
combined_meta=MetadataConfig(schema_path,COMBINED_DEFAULT)
combined_meta.load_metadata_from_file(r"data/Metadata Samples\child_mortality_test.json")
combined_meta.validate()
combined_meta.print_QA_errors()

