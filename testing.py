from src.config_objects import MetadataConfig, COMBINED_DEFAULT


#Testing
schema_path=r"C:/Users/nemats/My Code/api_formatter-main/api_formatter/data/Schema/CombinedSchema.json"
example_1=r"C:/Users/nemats/My Code/api_formatter-main/api_formatter/data/Metadata Samples/child_mortality_metadata.json"
example_2=r"C:/Users/nemats/My Code/api_formatter-main/api_formatter/data/Metadata Samples/cpi_metadata.json"
example_3=r"C:/Users/nemats/My Code/api_formatter-main/api_formatter/data/Metadata Samples/retail_sales_metadata.json"
example_4=r"C:/Users/nemats/My Code/api_formatter-main/api_formatter/data/Metadata Samples/custom_example.json"


#importing metadata
combined_meta=MetadataConfig(schema_path,COMBINED_DEFAULT)
combined_meta.load_metadata_from_file(example_4)



#set key and values
combined_meta.set("Dataset.publisher.name","New Publication")


#query
print(combined_meta.get("Dataset.publisher.name"))
# print(combined_meta.get("Edition"))


## Qulaity Assurance
# combined_meta.validate()
# combined_meta.print_QA_errors()


