#!/usr/bin/env python3
"""Text Synthesizer Agent - Generate concise explainer copy"""

import json
import sys
import re
from typing import Dict, List

class TextSynthesizer:
    """Generates explainer text for scenes"""
    
    # Text templates by type and tone
    TEMPLATES = {
        "headline": {
            "educational": [
                "Understanding {concept}",
                "The {concept} explained",
                "{concept}: What you need to know"
            ],
            "emotional": [
                "Your {concept} matters",
                "Discover {concept}",
                "Transform your {concept}"
            ],
            "neutral": [
                "{concept}",
                "About {concept}",
                "{concept} overview"
            ]
        },
        "subtext": {
            "educational": [
                "Learn how {concept} works",
                "{concept} in simple terms",
                "Breaking down {concept}"
            ],
            "emotional": [
                "Feel the power of {concept}",
                "Unlock your {concept}",
                "Experience {concept}"
            ],
            "neutral": [
                "Key insights on {concept}",
                "{concept} essentials",
                "What is {concept}?"
            ]
        },
        "definition": {
            "educational": [
                "{concept} is the {description}",
                "{concept} refers to {description}",
                "Simply put, {concept} means {description}"
            ],
            "emotional": [
                "{concept} is your {description}",
                "{concept} represents {description}",
                "Think of {concept} as your {description}"
            ],
            "neutral": [
                "{concept}: {description}",
                "{concept} - {description}",
                "{description}"
            ]
        },
        "label": {
            "educational": ["{concept}"],
            "emotional": ["{concept}"],
            "neutral": ["{concept}"]
        }
    }
    
    # Concept refinements
    REFINEMENTS = {
        "gut_brain_connection": "gut-brain axis",
        "nervous_system": "nervous system",
        "self_assessment": "progress check",
        "confidence_assessment": "confidence level"
    }
    
    def __init__(self):
        pass
    
    def process(self, input_data: Dict) -> Dict:
        """Generate text for all requests"""
        context = input_data.get("context", {})
        text_requests = input_data.get("text_requests", [])
        
        generated_texts = []
        
        for request in text_requests:
            text_result = self._generate_text(request, context)
            generated_texts.append(text_result)
        
        return {
            "agent_id": "TextSynthesizer",
            "version": "1.0",
            "output": {
                "generated_texts": generated_texts
            }
        }
    
    def _generate_text(self, request: Dict, context: Dict) -> Dict:
        """Generate a single text item"""
        text_type = request.get("type", "headline")
        max_length = request.get("max_length", 50)
        tone = request.get("tone", "educational")
        required_concepts = request.get("required_concepts", [])
        
        # Extract context
        topic = context.get("topic", "")
        key_concepts = context.get("key_concepts", [])
        intent = context.get("intent", "")
        
        # Merge concepts
        concepts = list(set(key_concepts + required_concepts))
        if not concepts and topic:
            concepts = [topic]
        
        # Generate primary text
        primary_text = self._generate_primary(
            text_type, 
            tone, 
            topic, 
            concepts, 
            context
        )
        
        # Ensure length constraint
        primary_text = self._truncate_text(primary_text, max_length)
        
        # Generate alternatives
        alternatives = self._generate_alternatives(
            text_type,
            tone,
            topic,
            concepts,
            context,
            max_length
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            primary_text,
            concepts,
            text_type
        )
        
        return {
            "type": text_type,
            "text": primary_text,
            "character_count": len(primary_text),
            "confidence": confidence,
            "alternatives": alternatives[:2]  # Top 2
        }
    
    def _generate_primary(
        self,
        text_type: str,
        tone: str,
        topic: str,
        concepts: List[str],
        context: Dict
    ) -> str:
        """Generate primary text"""
        
        # Get templates
        templates = self.TEMPLATES.get(text_type, {}).get(tone, [])
        if not templates:
            templates = self.TEMPLATES.get(text_type, {}).get("neutral", [])
        
        # Select best concept
        concept = self._select_best_concept(concepts, topic)
        
        # Refine concept
        concept_clean = self._refine_concept(concept)
        
        # Fill template
        if templates:
            template = templates[0]
            text = template.format(
                concept=concept_clean,
                description=self._get_description(concept_clean, context)
            )
        else:
            text = concept_clean.title()
        
        return self._polish_text(text)
    
    def _generate_alternatives(
        self,
        text_type: str,
        tone: str,
        topic: str,
        concepts: List[str],
        context: Dict,
        max_length: int
    ) -> List[str]:
        """Generate alternative phrasings"""
        alternatives = []
        
        templates = self.TEMPLATES.get(text_type, {}).get(tone, [])
        concept = self._select_best_concept(concepts, topic)
        concept_clean = self._refine_concept(concept)
        
        # Try different templates
        for template in templates[1:3]:  # Skip first (used for primary)
            try:
                text = template.format(
                    concept=concept_clean,
                    description=self._get_description(concept_clean, context)
                )
                text = self._polish_text(text)
                text = self._truncate_text(text, max_length)
                alternatives.append(text)
            except:
                pass
        
        # Try different concepts
        for alt_concept in concepts[:2]:
            if alt_concept != concept:
                alt_clean = self._refine_concept(alt_concept)
                if templates:
                    text = templates[0].format(
                        concept=alt_clean,
                        description=self._get_description(alt_clean, context)
                    )
                    text = self._polish_text(text)
                    text = self._truncate_text(text, max_length)
                    alternatives.append(text)
        
        return alternatives[:3]
    
    def _select_best_concept(self, concepts: List[str], topic: str) -> str:
        """Select most relevant concept"""
        if not concepts:
            return topic or "concept"
        
        # Prefer shorter, more specific concepts
        concepts_sorted = sorted(concepts, key=lambda x: (len(x), x))
        return concepts_sorted[0]
    
    def _refine_concept(self, concept: str) -> str:
        """Clean and refine concept text"""
        # Check refinements
        if concept in self.REFINEMENTS:
            return self.REFINEMENTS[concept]
        
        # Clean up
        refined = concept.replace("_", " ")
        refined = refined.replace("-", " ")
        refined = re.sub(r'\s+', ' ', refined).strip()
        
        return refined
    
    def _get_description(self, concept: str, context: Dict) -> str:
        """Get description for concept"""
        # Simple descriptions
        descriptions = {
            "gut": "connection between your digestive system and mind",
            "brain": "command center of your body",
            "intuition": "inner guidance system",
            "confidence": "belief in yourself",
            "progress": "journey forward",
            "transformation": "positive change"
        }
        
        # Try to find match
        for key, desc in descriptions.items():
            if key in concept.lower():
                return desc
        
        # Fallback
        return f"key to understanding {concept}"
    
    def _polish_text(self, text: str) -> str:
        """Polish and clean text"""
        # Capitalize properly
        text = text.strip()
        if text and not text[0].isupper():
            text = text[0].upper() + text[1:]
        
        # Clean spacing
        text = re.sub(r'\s+', ' ', text)
        
        # Remove trailing punctuation except ! or ?
        while text and text[-1] in '.,;:':
            text = text[:-1]
        
        return text
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        
        # Try to truncate at word boundary
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.7:  # At least 70% of max
            return truncated[:last_space]
        
        # Hard truncate with ellipsis
        return truncated[:max_length-1] + "…"
    
    def _calculate_confidence(
        self,
        text: str,
        concepts: List[str],
        text_type: str
    ) -> float:
        """Calculate generation confidence"""
        confidence = 0.6  # Base
        
        # Has concepts
        if concepts:
            confidence += 0.2
        
        # Good length
        if 5 < len(text) < 100:
            confidence += 0.1
        
        # Contains concept words
        text_lower = text.lower()
        if any(c.lower() in text_lower for c in concepts):
            confidence += 0.1
        
        return min(confidence, 1.0)

def main():
    """CLI entry point"""
    try:
        input_data = json.loads(sys.stdin.read())
        synthesizer = TextSynthesizer()
        output = synthesizer.process(input_data)
        print(json.dumps(output, indent=2))
        sys.exit(0)
    except Exception as e:
        error = {
            "error": str(e),
            "agent_id": "TextSynthesizer"
        }
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
