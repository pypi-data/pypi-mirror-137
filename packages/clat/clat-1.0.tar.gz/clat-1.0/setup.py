from setuptools import setup
import os

VERSION = "1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="clat",
    description="Command Line Analysis Tools: A collection of tools for doing data analysis.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="CD Clark III",
    url="https://github.com/CD3/clat",
    project_urls={
        "Issues": "https://github.com/CD3/clat/issues",
        "CI": "https://github.com/CD3/clat/actions",
        "Changelog": "https://github.com/CD3/clat/releases",
    },
    license="MIT",
    version=VERSION,
    packages=["clat"],
    entry_points="""
        [console_scripts]
        clat-avg=clat.cli:avg_cmd
        clat-sum=clat.cli:sum_cmd
        clat-rms=clat.cli:rms_cmd
        clat-stddev=clat.cli:stddev_cmd
        clat-unc=clat.cli:unc_cmd
        clat-histogram=clat.cli:histogram_cmd
        clat-plot=clat.cli:plot_cmd
        clat-func=clat.cli:func_cmd
        clat-transform=clat.cli:transform_cmd
    """,
    install_requires=["click","numpy"],
    extras_require={
        "test": ["pytest"]
    },
    tests_require=["clat[test]"],
    python_requires=">=3.6",
)
