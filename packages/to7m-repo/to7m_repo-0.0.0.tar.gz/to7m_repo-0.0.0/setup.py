from pathlib import Path
import setuptools


repo_dir = Path(__file__).parent

setuptools.setup(
    name="to7m_repo",
    version="0.0.0",
    author="to7m",
    author_email="mail@to7m.lol",
    description="My own repository management software.",
    long_description=(repo_dir / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/to7m/to7m_repo.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["to7m_context>=0.0.0,<1",
                      "to7m_convenience>=0.0.0,<1",
                      "to7m_qt>=0.0.0,<1"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    py_modules=[path.stem for path in (repo_dir / "src").iterdir()
                if path.suffix == ".py" and path.is_file()],
    python_requires=">=3.10",
)
