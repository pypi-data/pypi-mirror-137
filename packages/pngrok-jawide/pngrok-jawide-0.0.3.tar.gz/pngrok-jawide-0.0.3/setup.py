import setuptools

with open("README.md", "r", encoding="utf8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="pngrok-jawide",
  version="0.0.3",
  author="jawide",
  author_email="jawide@qq.com",
  description="这是一个使用python实现的内网穿透服务，完全使用标准库实现",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/jawide/pngrok",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)