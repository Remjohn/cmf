#!/usr/bin/env python3
"""Complete Pipeline Integration Tests"""

import pytest
import json
from pathlib import Path
import tempfile
import subprocess

# Import all agents
from agents.context_analyzer import ContextAnalyzer
from agents.scene_planner import ScenePlanner
from agents.asset_validator import AssetValidator
from agents.image_generator import ImageGenerator
from agents.layer_extractor import LayerExtractor
from agents.semantic_labeler import SemanticLabeler
from agents.text_synthesizer import TextSynthesizer
from agents.parameter_filler import ParameterFiller

class TestCompletePipeline:
    """End-to-end pipeline tests"""
    
    @pytest.fixture
    def sample_context(self):
        """Sample user input"""
        return {
            "script": "I'm at a 7 right now in terms of confidence",
            "topic": "confidence_check_in"
        }
    
    @pytest.fixture
    def temp_output_dir(self):
        """Temporary output directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_context_analyzer(self, sample_context):
        """Test context analysis"""
        analyzer = ContextAnalyzer()
        result = analyzer.process(sample_context)
        
        assert result["agent_id"] == "ContextAnalyzer"
        assert result["output"]["topic"] is not None
        assert result["output"]["confidence"] > 0.5
        assert len(result["output"]["ratings_detected"]) > 0
    
    def test_scene_planner(self, sample_context):
        """Test scene selection"""
        # First analyze
        analyzer = ContextAnalyzer()
        analyzed = analyzer.process(sample_context)
        
        # Then plan
        planner = ScenePlanner()
        result = planner.process(analyzed)
        
        assert result["agent_id"] == "ScenePlanner"
        assert len(result["output"]["selected_scenes"]) > 0
        assert result["output"]["selected_scenes"][0]["scene_id"] is not None
    
    def test_asset_validator_empty(self):
        """Test asset validator with no assets"""
        validator = AssetValidator()
        result = validator.process({
            "plan": {"selected_scenes": []},
            "assets": {"user_provided": [], "required_by_scenes": []}
        })
        
        assert result["agent_id"] == "AssetValidator"
        assert result["output"]["validation_status"] in ["pass", "partial", "fail"]
    
    def test_text_synthesizer(self, sample_context):
        """Test text generation"""
        analyzer = ContextAnalyzer()
        analyzed = analyzer.process(sample_context)
        
        synthesizer = TextSynthesizer()
        result = synthesizer.process({
            "context": analyzed["output"],
            "text_requests": [
                {
                    "type": "headline",
                    "max_length": 50,
                    "tone": "educational"
                }
            ]
        })
        
        assert result["agent_id"] == "TextSynthesizer"
        assert len(result["output"]["generated_texts"]) > 0
        text = result["output"]["generated_texts"][0]
        assert len(text["text"]) <= 50
        assert text["confidence"] > 0
    
    def test_parameter_filler(self, sample_context):
        """Test parameter filling"""
        # Analyze
        analyzer = ContextAnalyzer()
        analyzed = analyzer.process(sample_context)
        
        # Plan
        planner = ScenePlanner()
        planned = planner.process(analyzed)
        
        # Fill
        filler = ParameterFiller()
        result = filler.process({
            "selected_scenes": planned["output"]["selected_scenes"],
            "layer_graphs": [],
            "labeled_layers": [],
            "context": analyzed["output"],
            "brand_kit_id": "test_brand"
        })
        
        assert result["agent_id"] == "ParameterFiller"
        assert len(result["output"]["filled_scenes"]) > 0
        scene = result["output"]["filled_scenes"][0]
        assert scene["parameters"] is not None
        assert scene["completeness"] > 0
    
    def test_full_pipeline_simple_scene(self, sample_context, temp_output_dir):
        """Test complete pipeline for simple rating scene"""
        
        # Step 1: Analyze
        analyzer = ContextAnalyzer()
        analyzed = analyzer.process(sample_context)
        
        # Step 2: Plan
        planner = ScenePlanner()
        planned = planner.process(analyzed)
        
        # Step 3: Fill parameters
        filler = ParameterFiller()
        filled = filler.process({
            "selected_scenes": planned["output"]["selected_scenes"],
            "layer_graphs": [],
            "labeled_layers": [],
            "context": analyzed["output"],
            "brand_kit_id": "test_brand"
        })
        
        # Verify pipeline output
        assert len(filled["output"]["filled_scenes"]) > 0
        scene_config = filled["output"]["filled_scenes"][0]
        
        # Verify scene config structure
        assert "scene_id" in scene_config
        assert "parameters" in scene_config
        
        # Check rating value was extracted
        if scene_config["scene_id"] == "RATING_METER_1_TO_10":
            assert "rating_value" in scene_config["parameters"]
            assert scene_config["parameters"]["rating_value"] == 7


class TestAgentValidation:
    """Test agent input/output validation"""
    
    def test_context_analyzer_invalid_input(self):
        """Test context analyzer with invalid input"""
        analyzer = ContextAnalyzer()
        result = analyzer.process({})  # Empty input
        
        # Should handle gracefully
        assert "agent_id" in result or "error" in result
    
    def test_scene_planner_no_scenes_match(self):
        """Test scene planner when no scenes match"""
        planner = ScenePlanner()
        result = planner.process({
            "output": {
                "topic": "unknown_topic",
                "intent": "unknown",
                "ratings_detected": [],
                "key_concepts": []
            }
        })
        
        # Should return empty or fallback scenes
        assert result["agent_id"] == "ScenePlanner"
        assert "selected_scenes" in result["output"]


class TestSceneRendering:
    """Test scene rendering (requires Motion Canvas setup)"""
    
    @pytest.mark.skip(reason="Requires Motion Canvas and Node.js")
    def test_render_rating_meter(self, temp_output_dir):
        """Test rendering rating meter scene"""
        config = {
            "scene_id": "RATING_METER_1_TO_10",
            "version": "1.0",
            "parameters": {
                "rating_value": 7,
                "min_value": 0,
                "max_value": 10,
                "label_text": "Test"
            },
            "brand_kit_id": "test_brand",
            "timing": {
                "mode": "absolute",
                "duration_frames": 150,
                "fps": 30
            }
        }
        
        config_path = temp_output_dir / "test_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        # Render
        # (Would call Motion Canvas here)
        # output_path = render_scene(config, temp_output_dir)
        # assert output_path.exists()


class TestErrorHandling:
    """Test error handling and recovery"""
    
    def test_missing_asset_handling(self):
        """Test handling of missing assets"""
        validator = AssetValidator()
        result = validator.process({
            "plan": {"selected_scenes": [{"scene_id": "BODY_MAP_FOCUS"}]},
            "assets": {
                "user_provided": [],
                "required_by_scenes": [
                    {"scene_id": "BODY_MAP_FOCUS", "requires": ["body_image"]}
                ]
            }
        })
        
        assert len(result["output"]["missing_assets"]) > 0
        assert "body_image" in result["output"]["missing_assets"]
    
    def test_low_confidence_handling(self):
        """Test low confidence scenarios"""
        # Create context with minimal info
        analyzer = ContextAnalyzer()
        result = analyzer.process({"script": "test"})
        
        # Should have lower confidence but still return
        assert "confidence" in result["output"]


def test_agent_execution_times():
    """Benchmark agent execution times"""
    import time
    
    sample_input = {
        "script": "I'm at a 7 right now",
        "topic": "confidence"
    }
    
    # Time each agent
    times = {}
    
    # Context Analyzer
    start = time.time()
    analyzer = ContextAnalyzer()
    analyzer.process(sample_input)
    times["ContextAnalyzer"] = time.time() - start
    
    # Check times are reasonable
    assert times["ContextAnalyzer"] < 2.0, "Context analysis too slow"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
