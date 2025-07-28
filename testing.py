from src.config_objects import MetadataConfig, COMBINED_DEFAULT

#Testing
schema_path=r"data/Schema/CombinedSchema.json"
example_1=r"data/Metadata Samples/child_mortality_metadata.json"
example_2=r"data/Metadata Samples/cpi_metadata.json"
example_3=r"data/Metadata Samples/retail_sales_metadata.json"
example_4=r"data/Metadata Samples/custom_example.json"


#importing metadata
combined_meta=MetadataConfig(schema_path,COMBINED_DEFAULT)
# combined_meta.load_metadata_from_file(example_1)

#set key and values
# combined_meta.set('Edition.alerts.type',"random")
combined_meta.set("Dataset.publisher.name",12)

# print(combined_meta.get("Dataset.publisher.name"))


# #query
# print(combined_meta.get("Dataset.publisher.name"))
# # print(combined_meta.get("Edition"))


# # Qulaity Assurance
# combined_meta.validate()
# combined_meta.print_QA_errors()

# # Negative test - enum violation
# print("\n[QA] set() negative test (enum violation):")
# try:
#     combined_meta.set("Edition.quality_designation", "invalid-designation")
# except ValueError as e:
#     print("Caught expected ValueError:", e)

# # import_from_dict demo
# print("\n[QA] import_from_dict() demo - change quality_designation:")
# combined_meta.import_from_dict({"Edition": {"quality_designation": "official"}})

# combined_meta.validate()
# print("\n[QA] After import_from_dict() change:")
# combined_meta.print_QA_errors()

# # preview outputs
# print("\n[QA] preview('json') output:")
# combined_meta.preview("json")

# print("\n[QA] preview('yaml') output:")
# combined_meta.preview("yaml")

# print("\n[QA] preview('xml') - expected ValueError:")
# try:
#     combined_meta.preview("xml")
# except ValueError as e:
#     print(f"Error: {e}")

