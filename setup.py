import codecs  #用於編碼和解碼文本的方法
import os      #提供了許多與操作系統交互的函數
import re      #提供了正則表達式匹配操作。
import setuptools.dist   #用於管理軟體包安裝的工具。

def read(*directories):   #一個或多個目錄作為參數
    pathname = os.path.abspath(os.path.dirname(__file__)) #使用 os.path.abspath 和 os.path.dirname 函數獲取當前文件的絕對路徑
    return codecs.open(os.path.join(pathname, *directories), "r").read()  #使用 os.path.join 函數將 pathname 和 directories 參數連接起來，形成一個新的路徑。然後使用 codecs.open 函數以只讀模式打開該路徑下的文件，並使用 read 方法讀取文件內容。最後，返回讀取到的文件內容。

def find_version(*pathnames):   #接受一個或多個路徑名作為參數
    data = read(*pathnames)
    matched = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", data, re.M)    #使用 re.search 函數在變量 data 中搜索版本字符串。該函數的第一個參數是一個正則表達式，用於匹配版本字符串；第二個參數是要搜索的字符串；第三個參數是匹配模式。如果找到匹配項，則返回一個匹配對象；否則返回 None。匹配對象存儲在變量 matched 中。
    if matched:
        return matched.group(1)  #匹配第一個對象
    raise RuntimeError("Unable to find version string.")

def package_data():
    resources = []
    for root, _, filenames in os.walk(os.path.join("cellprofiler", "data")):
        resources += [
            os.path.relpath(os.path.join(root, filename), "cellprofiler")
            for filename in filenames
        ]

    for root, _, filenames in os.walk(os.path.join("cellprofiler", "gui")):
        resources += [
            os.path.relpath(os.path.join(root, filename), "cellprofiler")
            for filename in filenames
            if ".html" in filename
        ]
    return {"cellprofiler": resources}

setuptools.setup(  #用於設置和安裝 CellProfiler 軟體包
    author="cellprofiler-dev",
    author_email="cellprofiler-dev@broadinstitute.org",
    classifiers=[
        # 類型 :: 物件 :: 型式
        "Development Status :: 5 - Production/Stable", 
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering",
    ],
    entry_points={"console_scripts": ["cellprofiler=cellprofiler.__main__:main"]}, #軟體包的控制台腳本cellprofiler調用 cellprofiler.main 模塊中的 main 函數
    extras_require={
        "build": ["black", "pre-commit", "pyinstaller", "twine"],
        "docs": ["Sphinx>=3.1.1", "sphinx-rtd-theme>=0.5.0"],
        "test": ["pytest>=3.3.2,<4"],
    },  #安裝軟體包時可選的額外要求
    install_requires=[
        "boto3>=1.12.28",
        "cellprofiler-core==5.0.0",
        "centrosome==1.2.1",
        "docutils==0.15.2",
        "h5py~=3.6.0",
        "imageio>=2.5",
        "inflect>=2.1",
        "Jinja2>=2.11.2",
        "joblib>=0.13",
        "mahotas>=1.4",
        "matplotlib==3.1.3",
        "mysqlclient==1.4.6",
        "numpy>=1.20.1",
        "Pillow>=7.1.0",
        "pyzmq~=22.3",
        "sentry-sdk==0.18.0",
        "requests>=2.22",
        "scikit-image>=0.19.2",
        "scikit-learn>=0.20",
        "scipy>=1.4.1",
        "scyjava>=1.6.0",
        "six",
        "tifffile<2022.4.22",
        "wxPython==4.2.0",
    ],
    license="BSD",
    name="CellProfiler",
    package_data=package_data(),
    include_package_data=True,
    packages=setuptools.find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    setup_requires=["pytest"],
    url="https://github.com/CellProfiler/CellProfiler",
    version=find_version("cellprofiler", "__init__.py"),
)
