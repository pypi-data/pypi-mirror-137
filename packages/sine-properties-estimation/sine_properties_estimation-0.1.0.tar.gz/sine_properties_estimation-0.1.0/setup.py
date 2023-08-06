import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sine_properties_estimation",
    version="0.1.0",
    author="Lior Israeli",
    author_email="israelilior@gmail.com",
    description="estimate sine frequency, amp, phase and offset from 1D raw data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lisrael1/sine_properties_estimation",
    project_urls={
        "Bug Tracker": "https://github.com/lisrael1/sine_properties_estimation/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'numpy', 'pandas', 'scipy', 'dict_aligned_print',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
