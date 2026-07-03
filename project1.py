# =====================================================================
# SYSTEM SCENARIO: Zero-Dependency Live API Harvester
# =====================================================================
import urllib.request
import json
import sys

def stream_live_market_data():
    # The real, live target URL - requesting 10 raw product payloads
    target_url = "https://world.openfoodfacts.org/api/v2/search?categories_tags=snacks&fields=code,product_name,brands&page_size=10"
    
    print("LOG: Initiating network socket connection to OpenFoodFacts...")
    
    # 1. Defensive Network Layer
    try:
        # We explicitly set a timeout of 10 seconds so our code never freezes infinitely
        with urllib.request.urlopen(target_url, timeout=10) as response:
            if response.status != 200:
                print(f"CRITICAL: Server returned error code {response.status}", file=sys.stderr)
                return
                
            # Read the raw stream of bytes and decode to standard UTF-8 text
            raw_bytes = response.read()
            string_data = raw_bytes.decode('utf-8')
            
    except Exception as network_error:
        print(f"CRITICAL: Ingestion failed due to network socket drop: {network_error}", file=sys.stderr)
        return

    # 2. Memory Parsing Layer
    try:
        payload = json.loads(string_data)
    except json.JSONDecodeError as parse_error:
        print(f"CRITICAL: Fetched data is corrupted JSON layout: {parse_error}", file=sys.stderr)
        return

    # 3. Defensive Extraction Loop (The Heart of the Pipeline)
    products = payload.get("products", [])
    print(f"LOG: Successfully received {len(products)} records. Beginning processing...\n")
    
    for index, item in enumerate(products, start=1):
        # DEFENSIVE: We use .get() with a fallback string instead of item["product_name"]
        # This prevents a missing field from crashing our entire loop mid-execution.
        product_id = item.get("code", "UNKNOWN_ID")
        name = item.get("product_name", "MISSING_PRODUCT_NAME")
        brand = item.get("brands", "UNKNOWN_BRAND")
        
        # Log our clean metrics
        print(f"Record {index} -> ID: {product_id} | Name: {name[:40]}... | Brand: {brand}")

# Execute the live harvest
stream_live_market_data()