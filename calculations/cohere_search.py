import os
import cohere
import ast

try:
    path="COHERE_KEY.txt"
    os.environ["COHERE_KEY"] = open(path, 'r').read()
except:
    print("Please set the GITHUB_KEY environment variable.")


co = cohere.Client(os.environ["COHERE_KEY"])

def search_repositories(search_value, docs, n_results=3):
    results = co.rerank(query=search_value, documents=docs, top_n=n_results, model='rerank-english-v3.0')
    return [result['index'] for result in ast.literal_eval(results.json())['results']]