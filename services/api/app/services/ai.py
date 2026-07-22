from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractedOwnershipRecord:
    name: str
    confidence: float
    fields: list[dict[str, object]]


class ModelGateway:
    """Provider-neutral AI task gateway.

    Keep provider/model names out of product code. Route by task, data sensitivity, latency,
    region, and cost from here.
    """

    def extract_ownership_record(self, ocr_text: str) -> ExtractedOwnershipRecord:
        # Replace with strict JSON schema extraction via OpenAI/Gemini provider adapters.
        fields = [
            {"field_name": "product_name", "value": "Galaxy Book4 Pro 14", "confidence": 0.96, "evidence": "Product"},
            {"field_name": "brand", "value": "Samsung", "confidence": 0.91, "evidence": "Galaxy Book"},
            {"field_name": "model", "value": "NP940XGK", "confidence": 0.94, "evidence": "Model"},
            {"field_name": "purchase_date", "value": "2026-03-18", "confidence": 0.97, "evidence": "Purchase Date"},
            {"field_name": "price", "value": 148990, "confidence": 0.95, "evidence": "Total"},
            {"field_name": "gst", "value": 22727, "confidence": 0.92, "evidence": "GST"},
            {"field_name": "seller", "value": "Amazon India", "confidence": 0.96, "evidence": "Tax Invoice"},
            {"field_name": "payment_method", "value": "HDFC credit card", "confidence": 0.9, "evidence": "Payment"},
            {"field_name": "warranty_period", "value": "12 months", "confidence": 0.88, "evidence": "Warranty"},
        ]
        return ExtractedOwnershipRecord(name="Galaxy Book4 Pro 14", confidence=0.94, fields=fields)

    def answer_inventory_question(self, query: str, snippets: list[str]) -> str:
        if "warrant" in query.lower():
            return "The next warranty action is Sony Camera Lens, expiring on 13 Aug 2026."
        if "total" in query.lower() or "value" in query.lower():
            return "Your indexed household purchase value is INR 32.4L across 134 assets."
        if snippets:
            return f"I found {len(snippets)} relevant ownership records. Top match: {snippets[0]}"
        return "I did not find a confident match yet. Try a product name, seller, date, or price range."


model_gateway = ModelGateway()

