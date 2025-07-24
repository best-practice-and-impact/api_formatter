from src.config_objects import MetadataConfig, COMBINED_DEFAULT
import os, json, yaml

#Testing
schema_path=r"data/Schema/CombinedSchema.json"
sample_file = r"data/Metadata Samples\child_mortality_test.json"
results_dir = r"data/Metadata Samples"
os.makedirs(results_dir, exist_ok=True)

combined_meta=MetadataConfig(schema_path,COMBINED_DEFAULT)

# 1. Read file the validate then print erros
combined_meta.load_metadata_from_file(sample_file)
combined_meta.validate()
print("\n[QA] Initial cleanup check:")
combined_meta.print_QA_errors()

# read nested value
#print("\nEmail before change:", combined_meta.get("Dataset.contacts.email"))

# update nested value and re-validate
# combined_meta.set("Dataset.contacts.telephone", "+44 0000 000000")
print("\n[QA] import+from_dict() demo - change quality_designation")
combined_meta.import_from_dict({"Edition": {"quality_designation": "official"}})

combined_meta.validate()
print("\n[QA] After import_from_dict() change:")
combined_meta.print_QA_errors()

# export to json

combined_meta.export_to_json("child_mortality_test", file_path=results_dir)
print(f"\nJSON exported to {results_dir}/child_mortality_test_metadata.json ")

# preview function
print("\n[QA] preview('json') output:")
combined_meta.preview("json")

print("\n[QA] preview('yaml') output:")
combined_meta.preview("yaml")

print("\n[QA] preview('xml') - expected ValueError:")
try:
    combined_meta.preview("xml")
except ValueError as e:
    print(f"Error: {e}")

print("\n[QA] load_json() round-trip check")
schema_copy = combined_meta.load_json(schema_path)
print("Schema keys at root level:", list(schema_copy["properties"].keys()))

