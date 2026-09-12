import json

class Squat360WorkoutGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "athlete_name": ("STRING", {"default": "Athlete"}),
                "goal": (["strength", "hypertrophy", "conditioning"], {"default": "strength"}),
                "depth_cue": (["none", "cue", "warning"], {"default": "none"}),
                "knee_cue": (["none", "cue", "warning"], {"default": "none"}),
                "days_per_week": ("INT", {"default": 3, "min": 1, "max": 6, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("workout_summary", "workout_json")
    FUNCTION = "generate_workout"
    CATEGORY = "Squat360/AI Assistant"

    def generate_workout(self, athlete_name, goal, depth_cue, knee_cue, days_per_week):
        blocks = []
        if goal == "strength":
            main_title = "Back squat strength focus"
            main_detail = "3-5 sets x 3-5 reps @ RPE 7-8. 3-4 min rest between work sets. Coach spots depth."
        elif goal == "hypertrophy":
            main_title = "Lower body volume progression"
            main_detail = "4 sets x 8-12 reps with controlled 2s eccentric tempo. 90-120s rest."
        else:
            main_title = "Squat conditioning circuit"
            main_detail = "EMOM 15 min: 8 goblet squats + 10 kettlebell swings + 30s easy erg."

        if depth_cue != "none":
            main_detail += " Depth cue active: use 14-inch box or target tape until hip crease passes knee joint."
        if knee_cue != "none":
            main_detail += " Knee cue active: place mini-band above patella to reinforce active abduction."

        blocks.append({
            "day": "Day 1",
            "title": main_title,
            "detail": main_detail,
        })

        if days_per_week >= 2:
            blocks.append({
                "day": "Day 2",
                "title": "Posterior chain & hinge",
                "detail": "Romanian deadlift 3x6-8 + hip thrusts 3x10. Maintain neutral lumbar spine.",
            })

        if days_per_week >= 3:
            blocks.append({
                "day": "Day 3",
                "title": "Unilateral stability & core brace",
                "detail": "Bulgarian split squat 3x8/leg + Copenhagen plank 3x25s/side. Ribs stacked.",
            })

        if days_per_week >= 4:
            blocks.append({
                "day": "Day 4",
                "title": "Accessory & mobility reset",
                "detail": "Goblet pause squats 3x5 (3s pause) + ankle dorsiflexion rocks + hamstring floss.",
            })

        summary_lines = [f"=== Squat 360 Custom Workout for {athlete_name} ({goal.upper()}) ==="]
        for b in blocks:
            summary_lines.append(f"{b['day']}: {b['title']}\n  {b['detail']}")

        summary = "\n\n".join(summary_lines)
        data_json = json.dumps({
            "athlete": athlete_name,
            "goal": goal,
            "days_per_week": days_per_week,
            "blocks": blocks,
        }, indent=2)

        return (summary, data_json)


class Squat360AvatarPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "athlete_name": ("STRING", {"default": "Athlete"}),
                "goal": (["strength", "hypertrophy", "conditioning"], {"default": "strength"}),
                "style": (["clean_modern", "anime_aesthetic", "cinematic_gym", "cyberpunk_athletic"], {"default": "clean_modern"}),
                "theme": (["power_and_grit", "relentless_focus", "zen_recovery", "championship_energy"], {"default": "power_and_grit"}),
            },
            "optional": {
                "extra_details": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "generate_avatar_prompt"
    CATEGORY = "Squat360/AI Assistant"

    def generate_avatar_prompt(self, athlete_name, goal, style, theme, extra_details=""):
        style_descriptors = {
            "clean_modern": "clean modern digital portrait, crisp lines, athletic lighting, contemporary fitness brand visual",
            "anime_aesthetic": "high-detail anime fitness aesthetic, vibrant studio lighting, expressive dynamic portrait, cute athletic mascot vibe",
            "cinematic_gym": "cinematic dramatic lighting, high contrast gym ambiance, barbell rack background, bokeh, photorealistic depth",
            "cyberpunk_athletic": "futuristic biometric gym, neon cyan and amber accents, HUD telemetry overlays, high-tech training aesthetic",
        }

        theme_descriptors = {
            "power_and_grit": "unwavering determination, focused intense gaze, chalk dust in air, champion mindset",
            "relentless_focus": "calm laser-sharp focus, disciplined posture, perfectly composed breathing",
            "zen_recovery": "energized post-workout confidence, relaxed smile, vibrant wellness energy",
            "championship_energy": "victorious athletic celebration, peak physical form, inspirational motivation",
        }

        pos_parts = [
            f"motivational gym avatar portrait of athlete {athlete_name}",
            f"{goal} training dedication",
            theme_descriptors.get(theme, ""),
            style_descriptors.get(style, ""),
            "masterpiece, top tier quality, sharp focus",
        ]
        if extra_details.strip():
            pos_parts.append(extra_details.strip())

        positive = ", ".join([p for p in pos_parts if p])
        negative = "low quality, blurry, deformed anatomy, bad hands, bad eyes, extra limbs, watermark, text, signature"

        return (positive, negative)


class Squat360FoodPlan:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "athlete_name": ("STRING", {"default": "Athlete"}),
                "goal": (["strength", "hypertrophy", "conditioning"], {"default": "strength"}),
                "weight_kg": ("FLOAT", {"default": 75.0, "min": 35.0, "max": 200.0, "step": 0.5}),
                "diet_preference": (["high_protein_omnivore", "balanced_omnivore", "vegetarian", "plant_based"], {"default": "high_protein_omnivore"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("food_plan_summary", "food_plan_json")
    FUNCTION = "generate_food_plan"
    CATEGORY = "Squat360/AI Assistant"

    def generate_food_plan(self, athlete_name, goal, weight_kg, diet_preference):
        if goal == "hypertrophy":
            protein_g_per_kg = 2.0
            cal_multiplier = 36.0
        elif goal == "strength":
            protein_g_per_kg = 1.8
            cal_multiplier = 33.0
        else:  # conditioning
            protein_g_per_kg = 1.6
            cal_multiplier = 30.0

        target_protein = int(round(weight_kg * protein_g_per_kg))
        target_calories = int(round(weight_kg * cal_multiplier))
        fat_calories = int(round(target_calories * 0.25))
        fat_g = int(round(fat_calories / 9.0))
        remaining_cal = target_calories - (target_protein * 4) - fat_calories
        carb_g = max(50, int(round(remaining_cal / 4.0)))

        is_veg = "vegetarian" in diet_preference or "plant" in diet_preference

        breakfast = "Tofu scramble + avocado toast + mixed berries" if is_veg else "3 eggs + egg whites scramble + oatmeal with blueberries"
        pre_workout = "Rice cakes with almond butter + sliced banana"
        post_workout = "Plant protein shake + dates + chia seeds" if is_veg else "Whey isolate shake + white rice bowl with grilled chicken breast and steamed greens"
        dinner = "Lentil & chickpea curry with quinoa and steamed broccoli" if is_veg else "Grilled salmon or lean beef + sweet potato wedges + roasted asparagus"

        meals = [
            {"meal": "Breakfast", "title": "Energy & Protein Prime", "detail": breakfast},
            {"meal": "Pre-Workout (60-90m prior)", "title": "Glycogen Fuel", "detail": pre_workout},
            {"meal": "Post-Workout", "title": "Muscle Synthesis Recovery", "detail": post_workout},
            {"meal": "Dinner", "title": "Tissue Repair Plate", "detail": dinner},
        ]

        summary_lines = [
            f"=== Squat 360 Nutrition Plan for {athlete_name} ===",
            f"Target: {target_calories} kcal | Protein: {target_protein}g | Carbs: {carb_g}g | Fats: {fat_g}g",
            f"Weight: {weight_kg:.1f}kg | Goal: {goal.capitalize()} | Style: {diet_preference.replace('_', ' ').capitalize()}",
            "",
        ]
        for m in meals:
            summary_lines.append(f"[{m['meal']}] {m['title']}\n  {m['detail']}")

        summary = "\n".join(summary_lines)
        plan_json = json.dumps({
            "athlete": athlete_name,
            "weight_kg": weight_kg,
            "goal": goal,
            "diet": diet_preference,
            "macros": {
                "calories": target_calories,
                "protein_g": target_protein,
                "carbs_g": carb_g,
                "fats_g": fat_g,
            },
            "meals": meals,
        }, indent=2)

        return (summary, plan_json)


class Squat360FormAdvice:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "exercise": (["squat", "biceps_curl", "plank", "overhead_press"], {"default": "squat"}),
                "knee_or_elbow_angle": ("FLOAT", {"default": 85.0, "min": 20.0, "max": 180.0, "step": 1.0}),
                "torso_angle": ("FLOAT", {"default": 65.0, "min": 0.0, "max": 180.0, "step": 1.0}),
                "knee_valgus_detected": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("advice_text", "advice_json", "technique_score")
    FUNCTION = "evaluate_form"
    CATEGORY = "Squat360/AI Assistant"

    def evaluate_form(self, exercise, knee_or_elbow_angle, torso_angle, knee_valgus_detected):
        findings = []
        score = 100

        if exercise == "squat":
            if knee_or_elbow_angle > 105.0:
                findings.append({
                    "code": "DEPTH_INSUFFICIENT",
                    "severity": "cue",
                    "message": f"Knee angle reached {knee_or_elbow_angle:.1f}° (parallel target is <= 90°).",
                    "coach_hint": "Cue hip crease below top of patella. Consider target box squat.",
                })
                score -= 20
            elif knee_or_elbow_angle < 60.0:
                findings.append({
                    "code": "DEEP_SQUAT",
                    "severity": "info",
                    "message": f"Deep squat depth achieved ({knee_or_elbow_angle:.1f}°). Check lumbar stability at bottom.",
                    "coach_hint": "Maintain pelvic brace if butt-wink occurs in deep hole.",
                })
            else:
                findings.append({
                    "code": "DEPTH_SOLID",
                    "severity": "good",
                    "message": f"Good depth reached ({knee_or_elbow_angle:.1f}°).",
                    "coach_hint": "Consistent depth across work sets.",
                })

            if torso_angle < 50.0:
                findings.append({
                    "code": "TORSO_LEAN",
                    "severity": "cue",
                    "message": f"Excessive forward torso tilt ({torso_angle:.1f}°).",
                    "coach_hint": "Cue chest up, spread the floor, brace lats against the bar.",
                })
                score -= 15

            if knee_valgus_detected:
                findings.append({
                    "code": "KNEE_VALGUS",
                    "severity": "warning",
                    "message": "Inward knee collapse (valgus) detected during ascent.",
                    "coach_hint": "Cue pushing knees out over second toe. Add banded clamshells and abduction drills.",
                })
                score -= 25

        elif exercise == "biceps_curl":
            if knee_or_elbow_angle > 60.0:
                findings.append({
                    "code": "PEAK_CONTRACTION",
                    "severity": "cue",
                    "message": f"Elbow flexion stopped at {knee_or_elbow_angle:.1f}°.",
                    "coach_hint": "Cue full range of motion up to 40°-50° without swinging elbows forward.",
                })
                score -= 20
            else:
                findings.append({
                    "code": "FULL_CURL_ROM",
                    "severity": "good",
                    "message": "Full biceps contraction ROM verified.",
                    "coach_hint": "Maintain controlled 2s lowering phase.",
                })

        elif exercise == "plank":
            if torso_angle < 160.0:
                findings.append({
                    "code": "HIP_SAG_OR_PIKE",
                    "severity": "cue",
                    "message": f"Spine-to-hip alignment at {torso_angle:.1f}° (target is 170°-180° straight line).",
                    "coach_hint": "Tuck pelvis slightly, squeeze glutes and brace core as if taking a punch.",
                })
                score -= 25
            else:
                findings.append({
                    "code": "SOLID_PLANK",
                    "severity": "good",
                    "message": "Excellent straight torso alignment maintained.",
                    "coach_hint": "Progress hold duration or elevate single foot.",
                })

        advice_lines = [
            f"=== Squat 360 Form Assessment: {exercise.replace('_', ' ').upper()} ===",
            f"Technique Score: {max(0, score)}/100",
            "",
        ]
        for f in findings:
            advice_lines.append(f"[{f['severity'].upper()}] {f['code']}: {f['message']}\n  -> Coach Hint: {f['coach_hint']}")

        advice_text = "\n".join(advice_lines)
        advice_json = json.dumps({
            "exercise": exercise,
            "technique_score": max(0, score),
            "findings": findings,
        }, indent=2)

        return (advice_text, advice_json, max(0, score))


class Squat360AssistantBundle:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "athlete_name": ("STRING", {"default": "Athlete"}),
                "goal": (["strength", "hypertrophy", "conditioning"], {"default": "strength"}),
                "weight_kg": ("FLOAT", {"default": 75.0, "min": 35.0, "max": 200.0, "step": 0.5}),
                "diet_preference": (["high_protein_omnivore", "balanced_omnivore", "vegetarian", "plant_based"], {"default": "high_protein_omnivore"}),
                "days_per_week": ("INT", {"default": 3, "min": 2, "max": 6, "step": 1}),
                "depth_cue": (["none", "cue", "warning"], {"default": "none"}),
                "knee_cue": (["none", "cue", "warning"], {"default": "none"}),
                "knee_or_elbow_angle": ("FLOAT", {"default": 85.0, "min": 20.0, "max": 180.0, "step": 1.0}),
                "torso_angle": ("FLOAT", {"default": 65.0, "min": 0.0, "max": 180.0, "step": 1.0}),
                "knee_valgus_detected": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("workout_summary", "food_plan_summary", "form_advice", "avatar_prompt", "technique_score")
    FUNCTION = "build_bundle"
    CATEGORY = "Squat360/AI Assistant"

    def build_bundle(
        self,
        athlete_name,
        goal,
        weight_kg,
        diet_preference,
        days_per_week,
        depth_cue,
        knee_cue,
        knee_or_elbow_angle,
        torso_angle,
        knee_valgus_detected,
    ):
        workout = Squat360WorkoutGenerator().generate_workout(
            athlete_name, goal, depth_cue, knee_cue, days_per_week
        )
        food = Squat360FoodPlan().generate_food_plan(athlete_name, goal, weight_kg, diet_preference)
        form = Squat360FormAdvice().evaluate_form("squat", knee_or_elbow_angle, torso_angle, knee_valgus_detected)
        avatar = Squat360AvatarPrompt().generate_avatar_prompt(
            athlete_name, goal, "clean_modern", "power_and_grit"
        )
        return (workout[0], food[0], form[0], avatar[0], form[2])


NODE_CLASS_MAPPINGS = {
    "Squat360WorkoutGenerator": Squat360WorkoutGenerator,
    "Squat360AvatarPrompt": Squat360AvatarPrompt,
    "Squat360FoodPlan": Squat360FoodPlan,
    "Squat360FormAdvice": Squat360FormAdvice,
    "Squat360AssistantBundle": Squat360AssistantBundle,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Squat360WorkoutGenerator": "Squat 360 Workout Generator",
    "Squat360AvatarPrompt": "Squat 360 Avatar Motivation Prompt",
    "Squat360FoodPlan": "Squat 360 Custom Food Plan",
    "Squat360FormAdvice": "Squat 360 Form Advice & Angle Evaluator",
    "Squat360AssistantBundle": "Squat 360 AI Assistant Bundle",
}
