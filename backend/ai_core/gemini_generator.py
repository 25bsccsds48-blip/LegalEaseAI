import google.generativeai as genai

class GeminiDocumentGenerator:
    def __init__(self, settings):
        self.settings = settings
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate_document(self, request):
        prompt = f"Create a {request.document_type} between {request.parties}. Terms: {request.terms}. Date: {request.effective_date}. Make it professional with legal clauses."
        response = self.model.generate_content(prompt)
        return response.text