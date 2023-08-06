import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ServantReasoning",
    version="0.1.0",
    author="酥和侠",
    author_email="hexiaaaaaa@gmail.com",
    description="一个针对nonebot2 a版的从者推理插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suhexia/ServantReasoningGame",
    project_urls={
        "Bug Tracker": "https://github.com/suhexia/ServantReasoningGame/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7.3",
)