import os
import json
import sys
from app import create_app, db
from app.models import Users, Projects, Posts

app = create_app()

def export_project_data(project_id):
    with app.app_context():
        project = Projects.query.get(project_id)

        if not project:
            print(f"Project with ID {project_id} not found.")
            return

        posts = Posts.query.filter_by(project_id=project.id).order_by(Posts.created_at.asc(),Posts.id.asc()).all()
        
        journey_log = []

        for index , post in enumerate(posts):
            journey_log.append({
                'step': index + 1,
                'title': post.title,
                'content': post.content,
                'post_type': post.post_type or 'UPDATE',
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        project_data = {
            'meta':{
                'id':project.id,
                'title':project.title,
                "tech_stack": [t.strip() for t in project.tech_stack.split(",")] if project.tech_stack else [],
                'description':project.description,
                'status':project.status,
                'created_at':project.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at':project.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            },

            'journey':{
                'total_journey_steps':len(journey_log),
                'journey_log':journey_log
            },

            'ai_script':{
                'script':project.ai_script,
                'created_at':project.ai_script_created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }

        base_dir = os.path.dirname(os.path.abspath(__file__))
        export_dir = os.path.join(base_dir, 'exports')
        os.makedirs(export_dir, exist_ok=True)

        export_file = os.path.join(export_dir, f'{project.id}.json')

        with open(export_file, 'w') as f:
            json.dump(project_data, f, indent=4)

        print(f"Project {project.id} exported to {export_file}")

if __name__ == "__main__":
    # Default to Project ID 1
    target_id = 1
    
    # sys.argv contains what you typed in terminal: ['export_single_project.py', '5']
    if len(sys.argv) > 1:
        target_id = int(sys.argv[1]) # Grabs the '5' and converts it to an integer
        
    export_project_data(target_id)