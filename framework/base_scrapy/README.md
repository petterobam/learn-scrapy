## 安装 Scrapy 框架

```bash
pip install Scrapy
```

但是网上都推荐用 Anaconda 安装，初学者建议先安装 Anaconda （请百度安装方法）

```bash
conda install scrapy
或专业点的 ↓
conda install -c conda-forge scrapy
```

我用的是 Python3，双环境，所以

```bash
pip3 install Scrapy
```

## 创建 Scrapy 项目

```bash
scrapy startproject base_scrapy

PS：base_scrapy 为项目名，一般看你自己啦

于是就生成如下目录和文件：

base_scrapy
    ├── base_scrapy
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       ├── __init__.py
    │       └── __pycache__
    └── scrapy.cfg
```