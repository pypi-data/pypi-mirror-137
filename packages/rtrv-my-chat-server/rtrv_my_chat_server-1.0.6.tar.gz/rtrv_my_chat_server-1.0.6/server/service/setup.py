from setuptools import setup, find_packages

setup(name="rtrv_my_chat_server",
      version="1.0.1",
      description="my_chat_server",
      author="RTretyakov",
      author_email="rtretyakov@outlook.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
