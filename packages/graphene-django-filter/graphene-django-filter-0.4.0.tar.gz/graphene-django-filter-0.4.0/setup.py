# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_django_filter']

package_data = \
{'': ['*']}

install_requires = \
['Django==3.2',
 'anytree>=2.8.0,<3.0.0',
 'django-filter>=21.1,<22.0',
 'django-seed>=0.3.1,<0.4.0',
 'graphene-django>=2.15.0,<3.0.0',
 'graphene==2.1.9',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'stringcase>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'graphene-django-filter',
    'version': '0.4.0',
    'description': 'Advanced filters for Graphene',
    'long_description': '# Graphene-Django-Filter\n[![CI](https://github.com/devind-team/graphene-django-filter/workflows/CI/badge.svg)](https://github.com/devind-team/graphene-django-filter/actions) [![PyPI version](https://badge.fury.io/py/graphene-django-filter.svg)](https://badge.fury.io/py/graphene-django-filter)\n\nThis package contains advanced filters for [graphene-django](https://github.com/graphql-python/graphene-django). The standard filtering feature in Graphene-Django relies on the Django-Filter library and therefore provides a flat API without the ability to use `and` and `or` expressions. This library makes the API nested and adds the `and` and `or` composition by extension of the `DjangoFilterConnectionField` field and the `FilterSet` class.\n# Requirements\n* Python (3.6, 3.7, 3.8, 3.9, 3.10)\n* Graphene-Django (2.15)\n# Features\n## Nested API with the ability to use `and` and `or` expressions\nTo use, simply replace all `DjangoFilterConnectionField` fields with `AdvancedDjangoFilterConnectionField` fields in your queries. Also, if you create custom FilterSets, replace the inheritance from the `FilterSet` class with the inheritance from the `AdvancedFilterSet` class. For example, the following task query exposes an old flat API.\n```python\nimport graphene\nfrom django_filters import FilterSet\nfrom graphene_django import DjangoObjectType\nfrom graphene_django.filter import DjangoFilterConnectionField\n\nclass TaskFilter(FilterSet)\n    class Meta:\n        model = Task\n        fields = {\n            \'name\': (\'exact\', \'contains\'),\n            \'user__email\': (\'exact\', \'contains\'),\n            \'user__last_name\': (\'exact\', \'contains\'),\n        }\n \nclass UserType(DjangoObjectType):\n    class Meta:\n        model = User\n        interfaces = (graphene.relay.Node,)\n        fields = \'__all__\'\n        \nclass TaskType(DjangoObjectType):\n    user = graphene.Field(UserType)\n\n    class Meta:\n        model = Task\n        interfaces = (graphene.relay.Node,)\n        fields = \'__all__\'\n        filterset_class = TaskFilter\n        \nclass Query(graphene.ObjectType):\n    tasks = DjangoFilterConnectionField(TaskType)\n```\nThe flat API in which all filters are applied using the "and" operator looks like this.\n```graphql\n{\n  tasks(\n    name_Contains: "important"\n    user_Email_Contains: "john"\n    user_LastName: "Dou"\n  ){\n    edges {\n      node {\n        id\n        name\n      }\n    }\n  }\n}\n```\nAfter replacing the field class with the `AdvancedDjangoFilterConnectionField` and the `FilterSet` class with the `AdvancedFilterSet` the API becomes nested with support for `and` and `or` expressions.\n```python\nfrom graphene_django_filter import AdvancedDjangoFilterConnectionField, AdvancedFilterSet\n\nclass TaskFilter(AdvancedFilterSet)\n    class Meta:\n        model = Task\n        fields = {\n            \'name\': (\'exact\', \'contains\'),\n            \'user__email\': (\'exact\', \'contains\'),\n            \'user__last_name\': (\'exact\', \'contains\'),\n        }\n\nclass Query(graphene.ObjectType):\n    tasks = AdvancedDjangoFilterConnectionField(TaskType)\n```\nFor example, the following query returns tasks whose names contain the word "important" or the user\'s email address contains the word "john" and the user\'s last name is "Dou". Note that the operators are applied to lookups such as `contains`, `exact`, etc. at the last level of nesting.\n```graphql\n{\n  tasks(\n    filter: {\n      or: [\n        {name: {contains: "important"}}\n        and: [\n          {user: email: {contains: "john"}}\n          {user: lastName: {exact: "Dou"}}\n        ]\n      ]\n    }\n  ){\n    edges {\n      node {\n        id\n        name\n      }\n    }\n  }\n}\n```\nThe same result can be achieved with an alternative query structure because within the same object the `and` operator is always used.\n```graphql\n{\n  tasks(\n    filter: {\n      or: [\n        {name: {contains: "important"}}\n        {\n          user: {\n            email: {contains: "john"}\n            lastName: {exact: "Dou"}\n          }\n        }\n      ]\n    }\n  ){\n    edges {\n      node {\n        id\n        name\n      }\n    }\n  }\n}\n```\nThe filter input type has the following structure.\n```graphql\ninput FilterInputType {\n  and: [FilterInputType]\n  or: [FilterInputType]\n  ...FieldLookups\n}\n```\nFor more examples, see tests.\n',
    'author': 'devind-team',
    'author_email': 'team@devind.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devind-team/graphene-django-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
