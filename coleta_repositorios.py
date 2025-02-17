import requests
import pandas as pd

# Seu token GitHub
TOKEN = 'Colocar o token aqui'
HEADERS = {'Authorization': f'bearer {TOKEN}'}
URL = 'https://api.github.com/graphql'

# Query GraphQL
query = """
{
  search(query: "stars:>1", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        name
        owner {
          login
        }
        createdAt
        primaryLanguage {
          name
        }
        pullRequests(states: MERGED) {
          totalCount
        }
        releases {
          totalCount
        }
        updatedAt
        issues {
          totalCount
        }
        closedIssues: issues(states: CLOSED) {
          totalCount
        }
      }
    }
  }
}
"""

# Fazer a requisição
response = requests.post(URL, json={'query': query}, headers=HEADERS)
if response.status_code == 200:
    data = response.json()['data']['search']['nodes']

    # Processar e salvar dados em CSV
    df = pd.DataFrame([{
        'name': repo['name'],
        'owner': repo['owner']['login'],
        'createdAt': repo['createdAt'],
        'primaryLanguage': repo['primaryLanguage']['name'] if repo['primaryLanguage'] else 'None',
        'mergedPullRequests': repo['pullRequests']['totalCount'],
        'releases': repo['releases']['totalCount'],
        'updatedAt': repo['updatedAt'],
        'issues': repo['issues']['totalCount'],
        'closedIssues': repo['closedIssues']['totalCount']
    } for repo in data])

    df.to_csv('repositorios.csv', index=False)
    print("Dados salvos em repositorios.csv")
else:
    print("Erro na requisição:", response.status_code)
