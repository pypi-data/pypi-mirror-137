from pathlib import Path
import setuptools


repo_dir = Path(__file__).parent

setuptools.setup(
    name="to7m_putil",
    version="0.0.0",
    author="to7m",
    author_email="mail@to7m.lol",
    description="Library for dealing with processes.",
    long_description=(repo_dir / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/to7m/to7m_putil.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["psutil>=5.9.0,<6"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    py_modules=[path.stem for path in (repo_dir / "src").iterdir()
                if path.suffix == ".py" and path.is_file()],
    python_requires=">=3.10",
)
