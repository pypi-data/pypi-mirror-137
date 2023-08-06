import subprocess
from django.apps import apps

print(f'______________________begin pwd______________________')
print(subprocess.call(['pwd']))
print(f'______________________end pwd______________________')

subprocess.call(['rm', '-rf', 'fixtures'])
subprocess.call(['mkdir', 'fixtures'])

for model in apps.get_models():
    model_str = f'{model._meta.app_label}.{model.__name__}'
    print(f'{model_str}')
    subprocess.call(['mkdir', f'fixtures/{model_str}'])
    print(f'/fixtures/{model_str}')
    print(f'python', 'manage.py', 'dumpdata', '--indent', '2', '--output', f'fixtures/{model_str}/{model_str}.json')
    subprocess.call(['python',
                     'manage.py', 'dumpdata',
                     '--indent', '2',
                     '--output', f'fixtures/{model_str}/{model_str}.json'])


