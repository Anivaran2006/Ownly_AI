from dataclasses import dataclass


@dataclass(frozen=True)
class OcrResult:
    provider: str
    text: str
    layout: dict[str, object]


class OcrProvider:
    def extract(self, object_key: str, mime_type: str) -> OcrResult:
        raise NotImplementedError


class TesseractOcrProvider(OcrProvider):
    def extract(self, object_key: str, mime_type: str) -> OcrResult:
        return OcrResult(
            provider="tesseract",
            text=(
                "Amazon India Tax Invoice\n"
                "Product: Galaxy Book4 Pro 14\n"
                "Model: NP940XGK\n"
                "Purchase Date: 18 Mar 2026\n"
                "Total: INR 148,990\n"
                "GST: INR 22,727\n"
                "Payment: HDFC credit card\n"
                "Warranty: 12 months\n"
            ),
            layout={"source_object_key": object_key, "mime_type": mime_type, "quality": "stub"},
        )


class GoogleDocumentAiProvider(OcrProvider):
    def extract(self, object_key: str, mime_type: str) -> OcrResult:
        raise NotImplementedError("Connect Google Document AI processor here.")


class AzureDocumentIntelligenceProvider(OcrProvider):
    def extract(self, object_key: str, mime_type: str) -> OcrResult:
        raise NotImplementedError("Connect Azure Document Intelligence client here.")


def get_ocr_provider(provider_name: str) -> OcrProvider:
    if provider_name == "google_document_ai":
        return GoogleDocumentAiProvider()
    if provider_name == "azure_document_intelligence":
        return AzureDocumentIntelligenceProvider()
    return TesseractOcrProvider()

