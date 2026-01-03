import os
import json
import sys
from app import create_app, db
from app.models import Users, Projects, Posts

app = create_app()

STATUS_TO_STAGE = {
    "ideation": "idea",
    "in_progress": "active_development",
    "beta": "stabilization",
    "launched": "maintenance"
}

def infer_journey_intent(post_type, step):
    post_type = post_type.lower()

    if step == 1:
        return "foundation"

    if post_type == "init":
        return "foundation"

    if post_type in ["feature", "refactor"] and step <= 3:
        return "foundation"

    if post_type in ["feature", "update"]:
        return "progress"

    if post_type in ["decision"]:
        return "decision"

    if post_type in ["milestone", "deploy"]:
        return "milestone"

    if post_type in ["learning", "reflection"]:
        return "reflection"

    if post_type in ["fix"]:
        return "maintenance"

    return "progress"



def export_project_data(project_id):
    with app.app_context():
        project = Projects.query.get(project_id)

        if not project:
            print(f"Project with ID {project_id} not found.")
            return

        posts = Posts.query.filter_by(project_id=project.id).order_by(Posts.created_at.asc(),Posts.id.asc()).all()
        
        journey_log = []

        for index , post in enumerate(posts):
            step = index + 1
            post_type = post.post_type.lower()
            

            journey_log.append({
                'step': step,
                'title': post.title,
                'content': post.content,
                'post_type':post_type,
                'intent':infer_journey_intent(post_type, step),
                'created_at': post.created_at.strftime('%Y-%m-%dT%H:%M:%S')
            })
        
        project_data = {
            'schema_version':'1.1.0',
            'enums':{
                'post_types':[
                    'init',
                    'update',
                    'feature',
                    'fix',
                    'decision',
                    'learning',
                    'milestone',
                    'reflection'
                ]
            },
            'meta':{
                'id':project.id,
                'title':project.title,
                "tech_stack": [t.strip() for t in project.tech_stack.split(",")] if project.tech_stack else [],
                'description':project.description,
                'status':project.status,
                'project_stage':STATUS_TO_STAGE.get(project.status, "unknown"),
                'repo_url':project.repo_url,
                'start_date':project.start_date.strftime('%Y-%m-%d %H:%M:%S') if project.start_date else None,
                'created_at':project.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at':project.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            },

            'journey':{
                'total_steps':len(journey_log),
                'logs':journey_log
            }
        }

        # Save to project root /exports directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        export_dir = os.path.join(base_dir, 'exports')
        os.makedirs(export_dir, exist_ok=True)

        export_file = os.path.join(export_dir, f'project_{project.id}.json')

        with open(export_file, 'w') as f:
            json.dump(project_data, f, indent=4)

        print(f"✓ Project {project.id} exported successfully to: {export_file}")

if __name__ == "__main__":
    # Default to Project ID 1
    target_id = 1
    
    # sys.argv contains what you typed in terminal: ['export.py', '5']
    if len(sys.argv) > 1:
        target_id = int(sys.argv[1]) # Grabs the '5' and converts it to an integer
        
    export_project_data(target_id)
