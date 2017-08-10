# search-url
根据关键词，自动从搜索引擎采集相关网站的真实地址与标题，并且可以自动保存为文件，自动去除重复URL。同时，也可以自定义忽略多条域名。最新百度采集通过，测试时间2017-08-03


# 运行截图

![image](https://github.com/super-l/search-url/blob/master/screenshots1.png)
![image](https://github.com/super-l/search-url/blob/master/screenshots2.png)

Author:superl
--------
Blog:http://www.superl.org/post-searchurl.html
--------
QQ群:199688491
--------
# 使用说明
* 程序主要运用于安全渗透测试项目，以及批量评估各类CMS系统0DAY的影响程度，同时也是批量采集自己获取感兴趣的网站的一个小程序~~
* 测试环境为 Python 2.7.x 如果需要python3版本的，可以自行修改，或者[我的博客](http://www.superl.org)留言

* 目前只可以采集百度搜索引擎的结果。并且每页默认显示50条记录。可自定义输入要采集的页数。

* 如果要采集关键词为“hacker”的相关网站，采集百度结果的前3页，则输入如下：

  * please input keyword:hacker

  * Search Number of pages:3



# 特点
* 获取到的是百度搜索结果的真实URL地址
* 可以忽略不需要的常见网站，如忽略百度翻译，等等所有百度相关结果，给数组添加baidu.com即可。程序已经默认忽略了很多条啦，如

  filter_array1 = ['baidu.com','sina.com.cn','sohu.com','taobao.com','douban.com','163.com','tianya.cn','qq.com','1688.com']

  filter_array2 = ['ganji.com','58.com','baixing.com']

  filter_array3 = ['zhihu.com','weibo.com','iqiyi.com','kugou.com','51.com','youku.com','soku.com','acfun.cn','verycd.com']

  filter_array4 = ['google.cn','youdao.com','iciba.com','cdict.net']

  filter_array5 = ['pconline.com.cn','zcool.com.cn','csdn.net','lofter.com']
  
* 实时显示采集到的网页的【真实URL】以及【标题】。前面的【ID】对应的是当前页百度结果的第X条数据

* 自动保存结果到当前目录的txt文件，文件名为搜索的 关键词.txt 为了方便导入到其他工具，txt文件里面只记录了采集的网址。如果需要同时记录标题，把代码中的注释删除即可

* 自动去除重复记录
* 统计总采集条数（143 found），有效的条数（91 checked），被过滤的条数（52 filter），以及被过滤的重复的URL条数（9 delete）
* 开源，任何人都可以下载使用。由于本人能力有限，如果有好的建议以及修改，也希望能一起完善
* 跨平台，并且无捆绑后门风险。以前网上有的百度URL采集软件大部分为WINDOWS下的可执行文件，并且现在百度更新后无法正常采集。
* 程序会不断更新

# 关于更新
* 由于时间仓促，没有做优化。很多自定义参数也采用了默认值，下一个版本加上自定义参数
* 后免将陆续添加Bing搜索引擎,goole引擎的采集功能，与百度的进行一个合并。如果需求提高，也增加多线程或者多进程扫描
* 如果百度更新导致采集不到内容，可以[我的博客发布页](http://www.superl.org/post-searchurl.html)留言联系我进行修改，本次测试时间为2017-08-03

