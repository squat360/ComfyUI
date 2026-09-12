import json
import pytest
from comfy_extras.nodes_squat360 import (
    Squat360WorkoutGenerator,
    Squat360AvatarPrompt,
    Squat360FoodPlan,
    Squat360FormAdvice,
)


class TestSquat360WorkoutGenerator:
    def test_strength_workout(self):
        node = Squat360WorkoutGenerator()
        summary, json_str = node.generate_workout("Alex", "strength", "cue", "warning", 4)
        assert "Alex" in summary
        assert "STRENGTH" in summary
        assert "Depth cue active" in summary
        assert "Knee cue active" in summary
        data = json.loads(json_str)
        assert data["athlete"] == "Alex"
        assert data["goal"] == "strength"
        assert len(data["blocks"]) == 4

    def test_hypertrophy_workout(self):
        node = Squat360WorkoutGenerator()
        summary, json_str = node.generate_workout("Jordan", "hypertrophy", "none", "none", 3)
        assert "HYPERTROPHY" in summary
        data = json.loads(json_str)
        assert len(data["blocks"]) == 3

    def test_conditioning_workout(self):
        node = Squat360WorkoutGenerator()
        summary, json_str = node.generate_workout("Sam", "conditioning", "none", "none", 2)
        assert "CONDITIONING" in summary
        data = json.loads(json_str)
        assert len(data["blocks"]) == 2


class TestSquat360AvatarPrompt:
    def test_avatar_prompt_generation(self):
        node = Squat360AvatarPrompt()
        pos, neg = node.generate_avatar_prompt(
            "Alex", "strength", "clean_modern", "power_and_grit", "holding golden barbell"
        )
        assert "Alex" in pos
        assert "strength training dedication" in pos
        assert "clean modern digital portrait" in pos
        assert "holding golden barbell" in pos
        assert "low quality" in neg


class TestSquat360FoodPlan:
    def test_food_plan_omnivore(self):
        node = Squat360FoodPlan()
        summary, json_str = node.generate_food_plan("Alex", "strength", 80.0, "high_protein_omnivore")
        assert "Alex" in summary
        assert "Target:" in summary
        data = json.loads(json_str)
        assert data["macros"]["protein_g"] == 144
        assert len(data["meals"]) == 4

    def test_food_plan_vegetarian(self):
        node = Squat360FoodPlan()
        summary, json_str = node.generate_food_plan("Sam", "hypertrophy", 70.0, "vegetarian")
        assert "Tofu scramble" in summary
        data = json.loads(json_str)
        assert data["macros"]["protein_g"] == 140


class TestSquat360FormAdvice:
    def test_squat_insufficient_depth(self):
        node = Squat360FormAdvice()
        text, json_str, score = node.evaluate_form("squat", 115.0, 65.0, False)
        assert score < 100
        assert "DEPTH_INSUFFICIENT" in text
        data = json.loads(json_str)
        assert data["technique_score"] == 80

    def test_squat_valgus_and_lean(self):
        node = Squat360FormAdvice()
        text, json_str, score = node.evaluate_form("squat", 85.0, 45.0, True)
        assert "TORSO_LEAN" in text
        assert "KNEE_VALGUS" in text
        assert score == 60

    def test_biceps_curl(self):
        node = Squat360FormAdvice()
        text, json_str, score = node.evaluate_form("biceps_curl", 50.0, 65.0, False)
        assert "FULL_CURL_ROM" in text
        assert score == 100

    def test_plank_sag(self):
        node = Squat360FormAdvice()
        text, json_str, score = node.evaluate_form("plank", 85.0, 145.0, False)
        assert "HIP_SAG_OR_PIKE" in text
        assert score == 75
