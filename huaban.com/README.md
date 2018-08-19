
## 前情提要

最近看到花瓣的一个图集（淡然小笺赋箴言）蛮不错，想用爬虫收集下图集和对应的文字。

## 花瓣网

0. 测试异步爬虫
1. 简单文本模式
2. HTML静态模式


### 测试异步爬虫

花瓣里面的所有图片都是异步加载的，需要模拟浏览器操作，简单学习测试一下 selenium 的使用

代码来源：
作者：疯魔的小咸鱼
链接：https://www.jianshu.com/p/554c6d5af3ca

PS：selenium 安装注意事项

- 问题1：selenium 已经放弃 PhantomJS，了，建议使用火狐或者谷歌无界面浏览器。

    解决方案：selenium 版本降级。
    通过 `pip show selenium` 显示，默认安装版本为 3.14.0。 
    将其卸载 `pip uninstall selenium`，重新安装并指定版本号 `pip install selenium==2.48.0`。 

- 问题2： Unable to start phantomjs with ghostdriver: [WinError 2] 系统找不到指定的文件

    解决方案：下载 phantomjs.exe 到该目录下，或配置 phantomjs.exe 的目录路径到 path 环境变量

测试结果：

![所有小说图片截图](img/huaban-simple-1.png)