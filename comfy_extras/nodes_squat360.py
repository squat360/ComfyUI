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


def _mean(values):
    if not values:
        return None
    return sum(values) / float(len(values))


def _map_cue(code):
    if code in ("DEPTH_INSUFFICIENT", "DEPTH_CHECK"):
        return "DEPTH_CHECK"
    if code in ("KNEE_VALGUS", "KNEE_TRACK"):
        return "KNEE_TRACK"
    if code == "TORSO_LEAN":
        return "TORSO_LEAN"
    return code


def _parse_sessions(history_json):
    if not history_json or not str(history_json).strip():
        return []
    try:
        data = json.loads(history_json)
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        sessions = data.get("sessions") or []
    elif isinstance(data, list):
        sessions = data
    else:
        return []
    out = []
    for item in sessions:
        if not isinstance(item, dict):
            continue
        cues = item.get("cueCodes") or item.get("cues") or []
        if isinstance(cues, str):
            cues = [cues]
        score = item.get("formScore")
        load = item.get("loadKg")
        if load is None:
            load = item.get("load_kg")
        out.append({
            "reps": int(item.get("reps") or 0),
            "loadKg": None if load is None else float(load),
            "formScore": None if score is None else int(score),
            "cueCodes": [_map_cue(str(c)) for c in cues][:8],
        })
    return out[-12:]


def _parse_findings(findings_json):
    if not findings_json or not str(findings_json).strip():
        return []
    try:
        data = json.loads(findings_json)
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        data = data.get("findings") or []
    if not isinstance(data, list):
        return []
    out = []
    for item in data:
        if not isinstance(item, dict):
            continue
        out.append({
            "code": _map_cue(str(item.get("code") or "")),
            "severity": str(item.get("severity") or "info"),
        })
    return out


def _decide_coach(goal, days_per_week, findings, history):
    history = history[-12:]
    scores = [h["formScore"] for h in history if h.get("formScore") is not None]
    recent = scores[-3:]
    prior = scores[-6:-3]
    recent_mean = _mean(recent)
    prior_mean = _mean(prior)

    trend = "flat"
    if recent_mean is not None and prior_mean is not None:
        if recent_mean - prior_mean >= 4:
            trend = "improving"
        elif prior_mean - recent_mean >= 4:
            trend = "declining"
    elif recent_mean is not None and recent_mean < 70:
        trend = "declining"
    elif recent_mean is not None and recent_mean >= 88:
        trend = "improving"

    live_cues = [
        f["code"] for f in findings
        if f.get("severity") in ("cue", "flag", "warning")
    ]
    cue_hits = {}
    for row in history:
        for code in row.get("cueCodes") or []:
            cue_hits[code] = cue_hits.get(code, 0) + 1
    for code in live_cues:
        cue_hits[code] = cue_hits.get(code, 0) + 2
    persistent = sorted(cue_hits.items(), key=lambda item: (-item[1], item[0]))
    persistent = [code for code, n in persistent if n >= 2]
    priority_cue = persistent[0] if persistent else (live_cues[0] if live_cues else None)

    last_two = history[-2:]
    vols = [row["reps"] * (row["loadKg"] or 0) for row in last_two]
    vol_drop = len(vols) == 2 and vols[0] > 0 and vols[1] < vols[0] * 0.8
    score_drop = (
        len(last_two) == 2
        and last_two[0].get("formScore") is not None
        and last_two[1].get("formScore") is not None
        and last_two[1]["formScore"] < last_two[0]["formScore"] - 8
    )
    high_frequency = len(history) >= max(5, int(days_per_week) + 2)

    recovery = "normal"
    if vol_drop and score_drop:
        recovery = "fatigued"
    elif high_frequency and trend == "declining":
        recovery = "fatigued"
    elif trend == "improving" and (recent_mean or 0) >= 88:
        recovery = "fresh"

    phase = "accumulate"
    if recovery == "fatigued" or (trend == "declining" and len(history) >= 4):
        phase = "deload"
    elif priority_cue in ("DEPTH_CHECK", "KNEE_TRACK", "TORSO_LEAN"):
        phase = "rebuild"
    elif recovery == "fresh" and trend == "improving" and goal == "strength":
        phase = "intensify"
    elif recovery == "fresh" and goal == "hypertrophy":
        phase = "accumulate"

    load_bias = 0.0
    calorie_bias = 0
    if phase == "intensify":
        load_bias = 5.0
        calorie_bias = 80
    elif phase == "deload":
        load_bias = -10.0
        calorie_bias = -120
    elif phase == "rebuild":
        load_bias = -5.0
        calorie_bias = 0
    elif trend == "improving":
        load_bias = 2.5
        calorie_bias = 40

    reasoning = []
    if scores:
        extra = f" (recent {recent_mean:.0f})" if recent_mean is not None else ""
        reasoning.append(f"Form trend {trend} across {len(scores)} scored sessions{extra}.")
    else:
        reasoning.append("No scored history yet — opening week uses live camera cues only.")
    reasoning.append(f"Recovery looks {recovery}{' (volume dropped last session)' if vol_drop else ''}.")
    if priority_cue:
        reasoning.append(f"Persistent cue: {priority_cue.replace('_', ' ').lower()}.")
    reasoning.append(f"Selected {phase} for {goal} at {days_per_week} days/week.")

    if phase == "deload":
        closer = "Cut load and protect sleep this week."
    elif phase == "rebuild":
        closer = "Technique before kilos until the cue clears."
    elif phase == "intensify":
        closer = "Add a little load. Film one work set."
    else:
        closer = "Build clean volume. Keep depth honest on camera."
    briefing = f"{goal} plan: {phase} block, recovery {recovery}, form {trend}. {closer}"

    return {
        "phase": phase,
        "recovery": recovery,
        "trend": trend,
        "priorityCue": priority_cue or "",
        "loadBiasKg": load_bias,
        "calorieBias": calorie_bias,
        "briefing": briefing,
        "reasoning": reasoning,
    }


def _answer_coach_question(question, decision, goal):
    q = question.strip().lower()
    if not q:
        return decision["briefing"]
    if any(word in q for word in ("depth", "hole", "parallel", "box")):
        if decision["priorityCue"] == "DEPTH_CHECK":
            return "Depth is the limiter. Keep the box or tape until hip crease is repeatable, then add load."
        return "Depth is not the main flag. Film a side set and keep the same stance markers."
    if any(word in q for word in ("knee", "valgus", "cave")):
        if decision["priorityCue"] == "KNEE_TRACK":
            return "Knees need a front-camera week: banded walks, slow step-downs, then squat."
        return "Knee tracking looks secondary. Still cue knees over second toe on the ascent."
    if any(word in q for word in ("eat", "food", "calorie", "protein", "diet")):
        bias = decision["calorieBias"]
        sign = "+" if bias >= 0 else ""
        return f"Eat for {goal}. This block biases {sign}{bias} kcal around the current target."
    if any(word in q for word in ("deload", "tired", "fatigue", "sore", "sleep")):
        if decision["phase"] == "deload" or decision["recovery"] == "fatigued":
            return "Yes — treat this as a deload. Drop load, keep some movement, sleep more."
        return f"Recovery is {decision['recovery']}. Train as written unless sleep tanks two nights in a row."
    if any(word in q for word in ("weight", "kilo", "load", "pr", "progress")):
        load = decision["loadBiasKg"]
        if load > 0:
            return f"Add about {load:g} kg only if the last filmed work set was clean."
        if load < 0:
            return f"Take {abs(load):g} kg off until form trend stops declining."
        return "Hold load. Collect one more clean session before changing the bar."
    return f"{decision['briefing']} Ask about depth, knees, food, fatigue, or load for a tighter call."


def _workout_with_coach(summary, decision):
    phase = decision["phase"]
    load = decision["loadBiasKg"]
    if phase == "deload":
        suffix = f" Deload: leave {abs(load):g} kg on the bar and stop at RPE 6."
    elif phase == "rebuild":
        suffix = " Rebuild: pause reps and a target. Load is a tool, not the point."
    elif phase == "intensify":
        suffix = f" Intensify: add ~{load:g} kg if last work set was clean."
    elif load > 0:
        suffix = f" Progression: +{load:g} kg if depth held."
    else:
        suffix = ""
    header = f"=== Super Coach: {phase.upper()} ===\n{decision['briefing']}\n\n"
    return header + summary + suffix


def _food_with_coach(summary, old_calories, decision):
    new_calories = max(1400, int(old_calories + decision["calorieBias"]))
    text = summary.replace(f"{old_calories} kcal", f"{new_calories} kcal", 1)
    if decision["phase"] == "deload":
        text += "\n  Super Coach: earlier dinner, 8h sleep target."
    elif decision["phase"] == "intensify":
        text += "\n  Super Coach: extra carb serving on squat day."
    return text


class Squat360SuperCoach:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "goal": (["strength", "hypertrophy", "conditioning"], {"default": "strength"}),
                "days_per_week": ("INT", {"default": 3, "min": 1, "max": 6, "step": 1}),
                "history_json": ("STRING", {"multiline": True, "default": "{\"sessions\":[]}"}),
            },
            "optional": {
                "findings_json": ("STRING", {"multiline": True, "default": "[]"}),
                "question": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "FLOAT", "INT")
    RETURN_NAMES = ("phase", "briefing", "reasoning", "answer", "priority_cue", "load_bias_kg", "calorie_bias")
    FUNCTION = "decide"
    CATEGORY = "Squat360/AI Assistant"

    def decide(self, goal, days_per_week, history_json, findings_json="[]", question=""):
        decision = _decide_coach(goal, days_per_week, _parse_findings(findings_json), _parse_sessions(history_json))
        answer = _answer_coach_question(question, decision, goal) if str(question).strip() else ""
        return (
            decision["phase"],
            decision["briefing"],
            " ".join(decision["reasoning"]),
            answer,
            decision["priorityCue"],
            float(decision["loadBiasKg"]),
            int(decision["calorieBias"]),
        )


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
            },
            "optional": {
                "history_json": ("STRING", {"multiline": True, "default": ""}),
                "question": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "INT", "STRING", "STRING")
    RETURN_NAMES = ("workout_summary", "food_plan_summary", "form_advice", "avatar_prompt", "technique_score", "briefing", "reasoning")
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
        history_json="",
        question="",
    ):
        workout = Squat360WorkoutGenerator().generate_workout(
            athlete_name, goal, depth_cue, knee_cue, days_per_week
        )
        food = Squat360FoodPlan().generate_food_plan(athlete_name, goal, weight_kg, diet_preference)
        form = Squat360FormAdvice().evaluate_form("squat", knee_or_elbow_angle, torso_angle, knee_valgus_detected)
        avatar = Squat360AvatarPrompt().generate_avatar_prompt(
            athlete_name, goal, "clean_modern", "power_and_grit"
        )
        form_data = json.loads(form[1])
        findings = list(form_data.get("findings") or [])
        if depth_cue != "none":
            findings.append({"code": "DEPTH_CHECK", "severity": "cue"})
        if knee_cue != "none":
            findings.append({"code": "KNEE_TRACK", "severity": "cue"})
        decision = _decide_coach(goal, days_per_week, findings, _parse_sessions(history_json))
        food_data = json.loads(food[1])
        old_calories = int(food_data.get("macros", {}).get("calories") or 0)
        workout_text = _workout_with_coach(workout[0], decision)
        food_text = _food_with_coach(food[0], old_calories, decision)
        briefing = decision["briefing"]
        if str(question).strip():
            answer = _answer_coach_question(question, decision, goal)
            briefing = f"{briefing}\nQ: {question.strip()}\nA: {answer}"
        return (workout_text, food_text, form[0], avatar[0], form[2], briefing, " ".join(decision["reasoning"]))


NODE_CLASS_MAPPINGS = {
    "Squat360WorkoutGenerator": Squat360WorkoutGenerator,
    "Squat360AvatarPrompt": Squat360AvatarPrompt,
    "Squat360FoodPlan": Squat360FoodPlan,
    "Squat360FormAdvice": Squat360FormAdvice,
    "Squat360SuperCoach": Squat360SuperCoach,
    "Squat360AssistantBundle": Squat360AssistantBundle,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Squat360WorkoutGenerator": "Squat 360 Workout Generator",
    "Squat360AvatarPrompt": "Squat 360 Avatar Motivation Prompt",
    "Squat360FoodPlan": "Squat 360 Custom Food Plan",
    "Squat360FormAdvice": "Squat 360 Form Advice & Angle Evaluator",
    "Squat360SuperCoach": "Squat 360 Super Coach",
    "Squat360AssistantBundle": "Squat 360 AI Assistant Bundle",
}
