from setuptools import setup, find_packages

setup(name="messenger_server_with_gui",
      version="0.0.2",
      description="Messenger Server",
      author="Nataly Komarova",
      author_email="shadowx110@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )