from setuptools import setup

setup(
    name='sauronblp', # 패키지 명
    version='1.0.0.0',
    description='blp client for sauron users',
    author='sauron9973',
    author_email='sauron9973@gmail.com',
    url='https://sauron9973.blogspot.com',
    license='MIT', # MIT에서 정한 표준 라이센스 따른다
    py_modules=['sauronblp'], # 패키지에 포함되는 모듈
    python_requires='>=3',
    install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지
    packages=['sauronblp'] # 패키지가 들어있는 폴더들
)