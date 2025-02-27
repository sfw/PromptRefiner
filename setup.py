from setuptools import setup, find_packages

setup(
    name="PromptRefiner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gradio>=3.0",  # Adjust version based on Modal availability
        "gradio_modal"
    ],
    author="Scott Francis Winder",
    author_email="scott@hackedpodcast.com",
    description="A library for refining prompts using an AI modal with Gradio integration",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/sfw/PromptRefiner",  # Update with your repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)