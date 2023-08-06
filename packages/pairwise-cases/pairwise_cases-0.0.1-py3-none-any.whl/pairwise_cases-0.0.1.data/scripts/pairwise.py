from PyInquirer import prompt
from examples import custom_style_2
from allpairspy import AllPairs
from tabulate import tabulate

questions = [
    {
        'type': 'input',
        'name': 'count',
        'message': 'How many configs(os, app version, etc.)',
    }
]

answers = prompt(questions, style=custom_style_2)
questions = []
for i in range(0, int(answers['count'])):
    questions.append({
        'type': 'input',
        'name': i,
        'message': f'Config {i + 1} row',        
    })

answers = prompt(questions, style=custom_style_2)    

b = answers.values()
parameters = []
for i in b:
    parameters.append(i.split(','))

print("\nOptimal test cases:\n")

arr = []

for i, pairs in enumerate(AllPairs(parameters)):
    a = []
    a.append(i)
    a.extend(pairs)
    arr.append(a)
    

print(tabulate(arr, tablefmt="grid"))    