from setuptools import find_packages, setup

def get_requirements()->list[str]:
    requirement_list:list[str] = []
    
    try:
        with open("requirements.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    
    return requirement_list

print(get_requirements())

setup(
    name='AI-Travel-Planner',
    version='0.1.0',
    author='Gaurav Singh',
    author_email='grv08singh@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)