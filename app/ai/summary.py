def generate_ai_summary(project_json):
    from datetime import datetime
    
    meta = project_json.get('meta', {})
    journey_log = project_json.get('journey', {}).get('logs', [])
    title = meta.get('title', 'Untitled Project')
    tech_stack = meta.get('tech_stack', [])
    status = meta.get('status', 'in_progress')
    total_steps = len(journey_log)

    # Calculate duration
    if journey_log and len(journey_log) >= 2:
        try:
            start = datetime.strptime(journey_log[0]['created_at'], '%Y-%m-%dT%H:%M:%S')
            end = datetime.strptime(journey_log[-1]['created_at'], '%Y-%m-%dT%H:%M:%S')
            duration = end - start
            duration_days = duration.days
        except (KeyError, ValueError):
            duration_days = 0
    else:
        duration_days = 0

    # Post type distribution
    post_type_count = {}
    for log in journey_log:
        pt = log.get("post_type", "update")
        post_type_count[pt] = post_type_count.get(pt, 0) + 1

    dominant_type = max(post_type_count, key=post_type_count.get) if post_type_count else "update"

    # Construct rule-based summary
    summary_lines = []

    summary_lines.append(
    f"{title} is a build-in-public platform built with {', '.join(tech_stack)} "
    f"to record project development through logged updates."
    )

    if tech_stack:
        summary_lines.append(
            f"The stack is used to handle data storage, update tracking, and project metadata management."
        )

    summary_lines.append(
        f"The project is currently {status.replace('_', ' ')} "
        f"and has {total_steps} documented updates over {duration_days} days."
    )

    if dominant_type == "milestone":
        summary_lines.append(
            "The project includes milestone updates that mark completed phases or major development steps."
        )
    else:
        summary_lines.append(
            f"Most updates are categorized as {dominant_type}, "
            f"covering {interpret_post_type(dominant_type)}."
        )  

    rule_based_summary = '\n\n'.join(summary_lines)
    
    # Integrate AI API here
    from app.ai.prompt import build_summary_prompt
    from app.ai.llm import run_llm

    try:
        prompt = build_summary_prompt(project_json, rule_based_summary)
        ai_output = run_llm(prompt)

        if not ai_output or len(ai_output.strip()) < 20:
            return rule_based_summary

        return ai_output.strip()

    except Exception as e:
        return rule_based_summary

def interpret_post_type(post_type):
    mapping = {
        "feature": "building new functionality",
        "learning": "reflection and learning",
        "decision": "architectural decision-making",
        "fix": "stability and bug fixing",
        "init": "project foundation work",
        "milestone": "major progress milestones",
        "update": "general progress tracking",
    }
    return mapping.get(post_type, "ongoing development")

