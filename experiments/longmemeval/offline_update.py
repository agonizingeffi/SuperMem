import os
from supermem.memory.supermem import SuperMemory

def load_supermem(collection_name):
    config = {
        "memory_manager": {
            "model_name": "openai",
            "configs": {
                "model": "gpt-4o-mini",
                "api_key": "",
                "max_tokens": 16000,
                "openai_base_url": ""
            }
        },
        "retrieve_strategy": "embedding",
        "embedding_retriever": {
            "model_name": "qdrant",
            "configs": {
                "collection_name": collection_name,
                "embedding_model_dims": 384,
                "path": f"/{collection_name}",
            }
        },
        "update": "offline",
    }
    supermem = SuperMemory.from_config(config)
    return supermem

base_dir = ""

for collection_name in os.listdir(base_dir):
    collection_path = os.path.join(base_dir, collection_name)
    if not os.path.isdir(collection_path):
        continue  

    print(f"Processing collection: {collection_name}")

    try:
        supermem = load_supermem(collection_name)
        supermem.construct_update_queue_all_entries()
        supermem.offline_update_all_entries(score_threshold=0.8)
        print(f"Finished updating {collection_name}")
    except Exception as e:
        print(f"Error processing {collection_name}: {e}")
