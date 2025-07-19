import asyncio
import argparse
from metadata_store import (
    add_service,
    update_metadata,
    init_db,
    list_services,
)
from metadata_parser import fetch_metadata, parse_metadata_to_json


async def ingest(service_url: str):
    metadata_xml, version_hash = await fetch_metadata(service_url)
    metadata_json = parse_metadata_to_json(metadata_xml)
    service = get_service_by_url(service_url)
    if service:
        update_metadata(service["id"], metadata_json, version_hash)
        print(f"Updated service {service_url}")
    else:
        service_id = add_service(service_url, metadata_json, version_hash)
        print(f"Added service {service_url} with id {service_id}")


def get_service_by_url(url: str):
    services = [s for s in list_services() if s["service_url"] == url]
    return services[0] if services else None


def main():
    parser = argparse.ArgumentParser(description="Ingest OData metadata")
    parser.add_argument("--url", required=True, help="Base URL of OData service")
    args = parser.parse_args()
    init_db()
    asyncio.run(ingest(args.url))


if __name__ == "__main__":
    main()
