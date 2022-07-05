<div>
  <p align="center"><img src="Hamster.png" style="zoom:20%;width:50%;" /></p>
</div>
****

#### 文件目录

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
