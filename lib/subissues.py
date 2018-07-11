from __future__ import unicode_literals

def list_epics_stories_and_tasks(jira, query):
    print("# JIRA EXPORT\n"+ "## Query: "+query+"\n")
    result = []
    epics = jira.search_issues(query, maxResults=10000,
            fields="issuetype,summary,description,status")
    for epic in epics:
        result.append(_to_string(jira,epic))
        stories = jira.search_issues('"Epic Link" = %s' % epic.key)
        for story in stories:
            result.append(_to_string(jira,story, 1))
            tasks = jira.search_issues('parent = %s' % story.key)
            for task in tasks:
                result.append(_to_string(jira,task, 2))
                    
    return '\n'.join(result)

def _to_string(jira, issue, level=0):
    offset = level * '    '
    offset2 = (level+1) * '    '
    offset3 = (level+2) * '    '
    
    #result = '{0}* {1.key} ({1.fields.status}): {1.fields.summary}'
    result = offset +'* '+ issue.key + '(' + str(issue.fields.status) + '):' + issue.fields.summary
    #if (issue.fields.issuetype.name =='Sub-task' or issue.fields.issuetype.name =='Task'):
    if issue.fields.description:
        result += '\n'+offset2 + '* DESCRIPTION:\n'
        lines = issue.fields.description.splitlines()
        result += '  \n'
        result += '  \n'.join(offset3 + '> ' + 
                (line if not (line.startswith('*') or line.startswith('#')) else '\\' + line)
                for line in lines)

    comments = jira.comments(issue)
    result += '\n\n'+offset2 + '* COMMENTS:'
    for comment in comments:
        result += '  \n' + offset3 + '> by: ' + str(comment.author) +' on '+ str(comment.created) + '\n'
        lines = comment.body.splitlines()
        result += '  \n'.join(offset3 + '> ' + 
                (line if not (line.startswith('*') or line.startswith('#')) else '\\' + line)
                for line in lines)+'\n' 

    print result.encode('utf-8')
