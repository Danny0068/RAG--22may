from typing import List, Dict
import groq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
import json

class ThemeAnalyzer:
    def __init__(self, api_key: str):
        self.client = groq.Client(api_key=api_key)
        self.theme_prompt = PromptTemplate(
            input_variables=["documents", "query"],
            template="""
            Analyze the following documents and identify common themes related to the query: {query}
            
            Documents:
            {documents}
            
            Please identify and explain the main themes, providing specific citations from the documents.
            Format your response as JSON with the following structure:
            {
                "themes": [
                    {
                        "name": "Theme name",
                        "description": "Theme description",
                        "citations": [
                            {
                                "document_id": "DOC001",
                                "page": "Page number",
                                "paragraph": "Paragraph number",
                                "text": "Relevant text"
                            }
                        ]
                    }
                ]
            }
            """
        )
    
    def analyze_themes(self, documents: List[Dict], query: str) -> Dict:
        """Analyze documents and identify themes"""
        # Prepare documents for analysis
        doc_texts = []
        for doc in documents:
            doc_texts.append(f"Document {doc['id']}:\n{doc['content']}")
        
        # Create prompt
        prompt = self.theme_prompt.format(
            documents="\n\n".join(doc_texts),
            query=query
        )
        
        # Get theme analysis from Groq
        response = self.client.chat.completions.create(
            model="llama2-70b-4096",
            messages=[
                {"role": "system", "content": "You are a document analysis expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse response
        try:
            themes = json.loads(response.choices[0].message.content)
            return themes
        except json.JSONDecodeError:
            return {"error": "Failed to parse theme analysis"} 