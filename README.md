# Something-for-api
目前市面上的工具在爬取webpack等前端时总会出现js遗漏问题，导致api接口获取不全，现写了几个小脚本来手动获取，保证api接口获取完整

本工具支持提取js文件、对应目标站点的API以及可能的参数内容

# 使用手册
* jsdownload.py: 修改目标站点以及js文件，通过正则解析js名称，并全部下载

python .\jsdownload.py

* findurl.py: 提取js文件中所有带/的，确保api接口全覆盖

python .\findurl.py outjs-xxx

* fingparam.py: 提取所有可能的参数，便于fuzz

以上均为自己使用时的小脚本，日常使用还是习惯先Packer-Fuzzer，再用jsdownload.py，最后用findurl.py提取路径，丢到bp里面批量跑，可以同时修改请求方法，筛选出可能的攻击路径，希望对各位有所帮助
