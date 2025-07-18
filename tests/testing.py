from config_objects import MetadataConfig, COMBINED_DEFAULT


#Testing
schema_path="C:\\Users\\nemats\\My Code\\api_formatter-main\\api_formatter\\data\\CombinedSchema.json"
combined_meta=MetadataConfig(schema_path,COMBINED_DEFAULT)
#combined_meta.load_metadata_from_file("C\\Users\\nemats\\My Code\\api_formatter-main\\api_formatter\\tests\\Metadata Samples\\child_mortality_metadata.json")
combined_meta.load_metadata_from_file(r"C:\Users\nemats\My Code\api_formatter-main\api_formatter\tests\Metadata Samples\child_mortality_metadata.json")
combined_meta.validate()
combined_meta.print_QA_errors()



