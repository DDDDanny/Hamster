<div>
  <p align="center"><img src="HamsterNew.png" style="zoom:20%;width:50%;" /></p>
</div>
<div>
	<p align="center">一个基于PO模型的移动端应用UI自动化测试框架</p>
</div>

---

### 介绍

Hamster是一个基于PO模型的移动端应用UI自动化测试框架。他是基于uiautomator2（服务Android端）和facebook-wda（服务IOS端）来搭建的。为了能够更好的进行元素定位以及解决一些无法定位的元素，我引用了图片识别以及OCR技术来辅助进行元素定位，因为有了它们的加入，Hamster已无所不能💪

### 文件目录

``` txt
├─.gitignore ----------- // Git Ignore
├─Config --------------- // 配置文件
│ └─SysConfig.ini ------ // 系统配置文件
├─Core ----------------- // 核心模块
│ ├─Driver.py ---------- // 驱动器
│ ├─Hamster.py --------- // Core Hamster
│ ├─HamsterIOS.py ------ // Core Hamster IOS
│ └─__init__.py 
├─Data ----------------- // 测试数据
│ └─__init__.py 
├─Images --------------- // 图片信息
│ └─__init__.py 
├─README.md 
├─Report --------------- // 测试报告
│ └─.black 
├─Run.py --------------- // 执行入口
├─Screenshot ----------- // 错误截图
│ └─__init__.py 
├─Test ----------------- // 测试用例PO
│ ├─Page --------------- // Page层
│ │ ├─Demo.py ---------- // Page元素
│ │ ├─EleConfig.ini ---- // 元素定位
│ │ └─__init__.py 
│ ├─Process ------------ // 业务层
│ │ ├─Demo.py ---------- // 业务层代码
│ │ └─__init__.py 
│ ├─TestCase ----------- // 用例层
│ │ ├─__init__.py 
│ │ ├─conftest.py ------ // 业务注册中心
│ │ └─test_Demo.py ----- // 测试用例
│ ├─__init__.py 
│ └─conftest.py -------- // 全局Conftest
├─Utils 
│ ├─CatchError.py ------ // 捕获Error
│ ├─EleAnalysis.py ----- // 元素解析
│ ├─GlobalVal.py ------- // 全局变量
│ ├─ImageDiscern.py ---- // 图片识别
│ ├─Log.py ------------- // Logger
│ ├─OCRDiscern.py ------ // OCR识别
│ ├─ReadConfig.py ------ // 读取配置文件
│ └─__init__.py 
├─conftest.py ---------- // 注册Marks
└─requirements.txt ----- // 依赖包
```

### 元素定位

目前元素定位有三种途径：

1. 通过uiautomator2和facebook-wda提供的元素定位接口进行定位
2. 通过图片识别进行定位（`ImageDiscern.py`）
3. 通过OCR文字识别进行定位（`OCRDiscern.py`）

第一种途径用的是最多的，绝大多数的元素能够被定位到

第二和第三种途径，定位到元素后会返回元素所在的坐标，再通过点击坐标进行点击

### 测试结果

可以通过对pytest来生成的XML文件进行解析获取结果数据，再利用Jinja来生成自己想要的测试报告

### ToDo List

- [ ] 提供默认测试报告
- [ ] 更轻量级
- [ ] ……

### 特别感谢

[uiautomator2](https://github.com/openatx/uiautomator2)

[WDA](https://github.com/openatx/facebook-wda)
