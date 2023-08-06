# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['buildgraph']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'buildgraph',
    'version': '0.0.4',
    'description': 'Tools for building',
    'long_description': '# Build Graph\n\n## Installing\n\nInstall with `pip install buildgraph`\n\nImport with `from buildgraph import BaseStep, buildgraph`\n\n\n## Introduction\n\n\nBuild Graph provides a set of tools to run build steps in order of their dependencies.\n\nBuild graphs can be constructed by hand, or you can let the library construct the graph for you.\n\nIn the following examples, we\'ll be using this step definition:\n```python\nclass Adder(BaseStep):\n    """\n    Returns its input plus 1\n    """\n    def execute(self, n):\n        new = n + 1\n        print(new)\n        return new\n```\n\n## Manual construction\n\n### Defining steps\n\nSteps are defined by constructing a step definition and binding the required arguments.\n\n```python\n# This will create a single \'Adder\' step with input 5\na = Adder(5)\n```\n\nStep arguments can be other steps:\n\n```python\n# This will provide the output from step a as input to step b\na = Adder(0).alias("a")  # Set an alias to identify the steps\nb = Adder(a).alias("b")\n```\n\nTo run the steps, we pick the last step in the graph and call its `run` method.\n\n```python\n...\nresult = b.run()\nprint(result)  # 2\n```\n\nA step from anywhere in the graph can be run, but only that step\'s dependencies will be executed.\n\n```python\nprint(a.run())  # 1 - Step b won\'t be run\n```\n\n\n### Side dependencies\n\nSometimes you\'ll need to run a step `a` before step `b`, but `a`\'s output won\'t be used by `b`.\n\n```python\nclass Printer(BaseStep):\n    def execute(self, msg):\n        print(msg)\n\np = Printer("Hi")\na = Adder(0).alias("a")\nb = Adder(a).alias("b").after(p)  # This ensures b will run after p\nb.run()\n```\n\nThe `after(*steps)` method specified steps that must be run first. If multiple steps are provided it doesn\'t enforce an ordering between those steps.\n\n\n### Detatched steps\n\nIf a step is defined but not listed as a dependency it won\'t be run:\n\n```python\na = Adder(0).alias("a")\nb = Adder(1).alias("b")\nb.run()  # This won\'t run a\n```\n\nYou can check which steps will be run with the `getExecutionOrder` and `printExecutionOrder` methods.\n\n\n### Circular dependencies\n\nBuildgraph will check for loops in the graph before running it and will raise an exception if one is detected.\n\n\n## Automatic construction\n\nThe `@buildgraph` decorator builds a graph where every node is reachable from the final node.\n\n```python\n@buildgraph()\ndef addergraph():\n    a = Adder(0)\n    b = Adder(1)\n    c = Adder(2)\n\naddergraph().run()  # This will run all 3 steps\n```\n\nIf the steps don\'t have dependencies the execution order isn\'t guaranteed, but generally the steps that are defined first will be run first unless another dependency enforces a different order.\n\n### Parameterised graphs\n\nGraphs can take input which will be used to construct it\n\n```python\n@buildgraph()\ndef loopinggraph(loops):\n    a = Adder(0)\n    for i in range(loops-1):\n        a = Adder(a)\n    return a\n\nlooponce = loopinggraph(1)\nlooponce.run()  # 1\n\nloopmany = loopinggraph(5)\nloopmany.run()  # 5\n```\n\n\n### Returning from a graph\n\nGraphs can return results from a step too.\n\n```python\n@buildgraph()\ndef addergraph():\n    a = Adder(0)\n    b = Adder(a)\n    return b\n\nresult = addergraph().run() \nprint(result)  # 1\n```\n\n\n## Extending steps\n\nAll steps must inherit from `BaseStep` and implement an `execute` method.\n\nYou can see example steps from `src/steps.py`. These steps can also be imported and used in code.\n\n### Shared Config\n\nSteps can receive a config object before running that other steps can share.\n\n```python\nclass ConfigStep(BaseStep):\n    def configure(self, config):\n        self.username = config[\'username\']\n\n    def execute(self):\n        print(f"My name is {self.username}")\n\n@buildgraph()\ndef getGraph():\n    ConfigStep()\n    ConfigStep()\n\ngraph = getGraph(config = {"username": "bob"})\ngraph.run()  # Both steps will print \'bob\'\n```\n\n\n## Exception Handling\n\nExceptions thrown inside steps will be caught, printed and the re-raised inside a `StepFailedException` object alongwith the \nstep and the arguments passed the the execute function.\n\nAfter handling an exception execution of further steps will stop.\n\n\n## Type checking\n\nBuildgraph will perform type checking when the graph is built if the `execute` method has type annotations on its parameters.\n\n\n## Configuring buildgraph\n\nBy default buildgraph prints coloured output. You can disable this with `buildgraph.setColor(False)`.\n\n\n## Examples\n\nSee the scripts in `examples/` for examples for more complex graphs.',
    'author': 'ubuntom',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ubuntom/buildgraph',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
