import hashlib
import httpx
import xml.etree.ElementTree as ET
from typing import Tuple


async def fetch_metadata(service_url: str) -> Tuple[str, str]:
    """Fetch $metadata content and return (metadata_xml, version_hash)."""
    url = service_url.rstrip("/") + "/$metadata"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        metadata_xml = resp.text
    version_hash = hashlib.sha256(metadata_xml.encode("utf-8")).hexdigest()
    return metadata_xml, version_hash


def parse_metadata_to_json(metadata_xml: str) -> str:
    """Parse EDMX XML into a minimal JSON representation."""
    root = ET.fromstring(metadata_xml)
    namespaces = {
        k or "edmx": v for k, v in root.attrib.items() if k.startswith("xmlns")
    }
    services = []
    for schema in root.findall(".//{*}Schema"):
        namespace = schema.attrib.get("Namespace")
        for entity in schema.findall("{*}EntityType"):
            services.append(
                {"namespace": namespace, "entity": entity.attrib.get("Name")}
            )
    return str({"services": services})
