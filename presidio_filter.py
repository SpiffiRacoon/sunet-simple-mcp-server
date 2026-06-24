from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig


class PII_filter:
    def __init__(self):
        self.swedish_nlp_config = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "sv", 
                    "model_name": "sv_core_news_lg"
                    }
                ],
            "ner_model_configuration": {
                "labels_to_ignore": ["O"],
                "model_to_presidio_entity_mapping": {
                    "PRS": "PERSON"  # Maps spaCy's Swedish 'PRS' label to Presidio's 'PERSON'
                    }
                }
            }
        self.provider = NlpEngineProvider(nlp_configuration=self.swedish_nlp_config)
        self.swedish_nlp_engine = self.provider.create_engine()
        self.analyzer = AnalyzerEngine(nlp_engine=self.swedish_nlp_engine, supported_languages=["sv"])
        self.anonymizer = AnonymizerEngine()
    
    def apply_filter(self, content_raw: (str | list[dict])) -> str:
        analysis_results = self.analyzer.analyze(
            text=content_raw, 
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"], 
            language='sv'
            )
        
        anonymized_result = self.anonymizer.anonymize(
            text=content_raw, 
            analyzer_results=analysis_results,
            operators={
                "PERSON": OperatorConfig("replace", {"new_value": "[NAMN_REDAKTERAT]"}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EPOST_REDAKTERAT]"}),
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[TELEFON_REDAKTERAT]"}),
            }
        )
        return anonymized_result.text
