from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import asyncio


class PII_filter:
    def __init__(self, entities=None, tokens=None):
        # Default entities if none provided
        self.entities = entities or ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"]
        
        # Default tokens mapping
        self.tokens = tokens or {
            "PERSON": "[NAMN_REDAKTERAT]",
            "EMAIL_ADDRESS": "[EPOST_REDAKTERAT]",
            "PHONE_NUMBER": "[TELEFON_REDAKTERAT]",
        }
        
        self.swedish_nlp_config = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "sv", 
                    "model_name": "sv_core_news_lg"
                    }
                ],
            "ner_model_configuration": {
                "labels_to_ignore": ["O", "LOC", "ORG", "TME"],
                "model_to_presidio_entity_mapping": {
                    "PRS": "PERSON"  # Maps spaCy's Swedish 'PRS' label to Presidio's 'PERSON'
                    }
                }
            }
        self.provider = NlpEngineProvider(nlp_configuration=self.swedish_nlp_config)
        self.swedish_nlp_engine = self.provider.create_engine()
        self.analyzer = AnalyzerEngine(nlp_engine=self.swedish_nlp_engine, supported_languages=["sv"])
        self.anonymizer = AnonymizerEngine()
    
    def _sync_apply_filter(self, content_raw: str) -> str:
        if not isinstance(content_raw, str):
            content_raw = str(content_raw)
        if not content_raw.strip():
            return content_raw

        analysis_results = self.analyzer.analyze(
            text=content_raw, 
            entities=self.entities, 
            language='sv'
        )
        
        # Construct dynamic operators based on provided configurations
        operators = {
            entity: OperatorConfig("replace", {"new_value": self.tokens.get(entity, f"[{entity}_REDAKTERAT]")})
            for entity in self.entities
        }
        
        anonymized_result = self.anonymizer.anonymize(
            text=content_raw, 
            analyzer_results=analysis_results,
            operators=operators
        )
        return anonymized_result.text
    
    async def apply_filter(self, content_raw: str) -> str:
        """Asynchronous wrapper to offload CPU work to a worker thread."""
        return await asyncio.to_thread(self._sync_apply_filter, content_raw)
