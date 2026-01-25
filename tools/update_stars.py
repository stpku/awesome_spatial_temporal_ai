#!/usr/bin/env python3
"""Update GitHub stars count for projects"""

import json
import subprocess
import time

def get_stars(repo_url):
    """Get star count from GitHub API"""
    if 'github.com/' in repo_url:
        repo = repo_url.split('github.com/')[-1].rstrip('/')
        if repo.endswith('.git'):
            repo = repo[:-4]
    else:
        return None
    
    try:
        result = subprocess.run(
            ['gh', 'api', f'repos/{repo}'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('stargazers_count', None)
    except Exception:
        pass
    
    return None

def update_stars():
    """Update stars in github_projects.json"""
    with open('awesomelist/github_projects.json', encoding='utf-8') as f:
        data = json.load(f)
    
    updated = 0
    for category in data['categories']:
        for project in category['projects']:
            if 'github.com' in project.get('url', ''):
                stars = get_stars(project['url'])
                if stars and stars != project.get('stars'):
                    print(f"  {project['name']}: {project.get('stars', '?')} -> {stars}")
                    project['stars'] = stars
                    project['last_updated'] = time.strftime('%Y-%m-%d')
                    updated += 1
    
    if updated > 0:
        with open('awesomelist/github_projects.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f'\nUpdated {updated} projects')
    else:
        print('No updates needed')

if __name__ == '__main__':
    print('Updating GitHub stars...')
    update_stars()
