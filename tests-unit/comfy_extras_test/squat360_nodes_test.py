import json
import pytest
from comfy_extras.nodes_squat360 import (
    Squat360WorkoutGenerator,
    Squat360AvatarPrompt,
    Squat360FoodPlan,
    Squat360FormAdvice,
    Squat360SuperCoach,
    Squat360CloudLlmPrompt,
    Squat360AssistantBundle,
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


class TestSquat360SuperCoach:
    def test_intensify_when_form_is_fresh_and_climbing(self):
        node = Squat360SuperCoach()
        history = json.dumps({
            "sessions": [
                {"reps": 5, "loadKg": 80, "formScore": 80, "cueCodes": []},
                {"reps": 5, "loadKg": 82, "formScore": 82, "cueCodes": []},
                {"reps": 5, "loadKg": 85, "formScore": 84, "cueCodes": []},
                {"reps": 5, "loadKg": 87, "formScore": 90, "cueCodes": []},
                {"reps": 5, "loadKg": 90, "formScore": 91, "cueCodes": []},
                {"reps": 5, "loadKg": 92, "formScore": 92, "cueCodes": []},
            ]
        })
        phase, briefing, reasoning, answer, cue, load, calories = node.decide(
            "strength", 3, history, "[]", "should I add weight"
        )
        assert phase == "intensify"
        assert load == 5.0
        assert calories == 80
        assert "Add about 5 kg" in answer
        assert "fresh" in briefing
        assert cue == ""

    def test_deload_when_volume_and_form_drop(self):
        node = Squat360SuperCoach()
        history = json.dumps({
            "sessions": [
                {"reps": 5, "loadKg": 100, "formScore": 88, "cueCodes": []},
                {"reps": 5, "loadKg": 70, "formScore": 75, "cueCodes": []},
            ]
        })
        phase, briefing, reasoning, answer, cue, load, calories = node.decide(
            "strength", 3, history, "[]", "I am tired"
        )
        assert phase == "deload"
        assert load == -10.0
        assert calories == -120
        assert "deload" in answer.lower()

    def test_rebuild_on_persistent_depth_cue(self):
        node = Squat360SuperCoach()
        history = json.dumps({
            "sessions": [
                {"reps": 5, "loadKg": 80, "formScore": 80, "cueCodes": ["DEPTH_CHECK"]},
                {"reps": 5, "loadKg": 80, "formScore": 81, "cueCodes": ["DEPTH_CHECK"]},
            ]
        })
        phase, briefing, reasoning, answer, cue, load, calories = node.decide(
            "strength", 3, history, "[]", "is my depth the problem"
        )
        assert phase == "rebuild"
        assert cue == "DEPTH_CHECK"
        assert load == -5.0
        assert "Depth is the limiter" in answer


class TestSquat360CloudLlmPrompt:
    def test_builds_system_and_user_prompts_without_network(self):
        node = Squat360CloudLlmPrompt()
        system, user = node.build(
            "strength",
            "intensify this week",
            "Form trend improving.",
            "should I add weight",
            json.dumps({"sessions": [{"reps": 5, "loadKg": 90, "formScore": 92, "cueCodes": []}]}),
            "intensify",
            "fresh",
            "improving",
            "",
            5.0,
            80,
        )
        assert "Stay inside the provided JSON" in system
        data = json.loads(user)
        assert data["goal"] == "strength"
        assert data["question"] == "should I add weight"
        assert data["decision"]["phase"] == "intensify"
        assert data["decision"]["loadBiasKg"] == 5.0
        assert data["history"][0]["formScore"] == 92


class TestSquat360AssistantBundle:
    def test_bundle_wires_all_assistant_outputs(self):
        node = Squat360AssistantBundle()
        workout, food, form, avatar, score, briefing, reasoning = node.build_bundle(
            "Alex", "strength", 80.0, "high_protein_omnivore", 4, "cue", "warning", 110.0, 48.0, True
        )
        assert "Alex" in workout
        assert "Super Coach" in workout
        assert "Target:" in food
        assert "KNEE_VALGUS" in form
        assert "Alex" in avatar
        assert score == 40
        assert briefing
        assert "rebuild" in briefing or "Selected" in reasoning
