# 使用说明
通过爱企查和FOFA接口获取注册资本大于5000w公司的公网通用系统，方便获得cnvd证书

# 需要有fofa高级会员！！！


# 用法

爱企查 --> 高级搜索 获取注册资本大于5000w企业
导出结果，放入companys.txt文件中
![图片](https://github.com/user-attachments/assets/47e0c009-fa36-4b4c-9d59-ff892a37728c)


将fofa邮箱和apikey填入config.ini文件中

xxx@qq.com

7f59f2xxxxxxxxxxxxxxxx639


python3 main.py

结果输出到result.csv中


结果中第一列为fid="xxxxxx" 该参数可直接放到fofa中搜索

第二列为公司名称

第三列为获取到的前五个标题
![图片](https://github.com/user-attachments/assets/8436ac15-41bf-4e4e-b644-57d6cd679db1)

# 原理说明
通过fofa的查询接口和统计聚合接口获取通用系统

fid：通过FOFA聚合的站点指纹进行查询


第一部分的判断逻辑为fofa搜索到的存活资产大于10，即可保留结果

筛选下来的系统通过fofa的统计聚合api(该接口有调用需间隔5秒)判断fid，如果fid大于10则判断为存在通用系统

当然fofa的fid筛选下来之后还是有很多的误报，会将前5个标题输出到结果中，可自行判断是否为通用系统




