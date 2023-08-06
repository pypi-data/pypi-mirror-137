import setuptools

setuptools.setup(
    name="hyperion_link",
    version="0.0.11",
    author='Michel Gerding',
    author_email="michelgerding@gmail.com",
    description="a connector between hyperion ng json api and python",
    packages=["hyperion_link"],
    url="https://github.com/michelgerding/hyperion-link",
    install_requires=[
        'websocket-client==1.2.3',
        'requests'
    ]
)