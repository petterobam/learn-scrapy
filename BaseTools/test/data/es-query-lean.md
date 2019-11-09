
1. query string search
2. query DSL
3. query filter
4. full-text search
5. phrase search
6. highlight search

## query string search

1. took：耗费了几毫秒
1. timed_out：是否超时，这里是没有
1. _shards：数据拆成了5个分片，所以对于搜索请求，会打到所有的primary shard（或者是它的某个replica shard也可以）
1. hits.total：查询结果的数量，3个document
1. hits.max_score：score的含义，就是document对于一个search的相关度的匹配分数，越相关，就越匹配，分数也高
1. hits.hits：包含了匹配搜索的document的详细数据

搜索全部

```json
GET /nginx/log_base/_search

结果如下：
{
  "took" : 18,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 143405,
    "max_score" : 1.0,
        “hits”: [
            {
                "_index" : "nginx",
                "_type" : "log_base",
                "_id" : "swZwhmwB82qtm9SxinXv",
                "_score" : 10.191514,
                "_source" : {
                    "ip" : "10.95.30.42",
                    "timestamp" : "17/Jul/2019:00:00:29 +0800",
                    "url" : "GET /v-dist/static/js/vendor.min.js HTTP/1.1",
                    "status" : "200",
                    "bytes" : "782353"
                }
            },
            {...},
            {...}
        ]
    }
}
```

query string search 的由来，因为 search 参数都是以 http 请求的 query string 来附带的

搜索商品名称中包含yagao的商品，而且按照售价降序排序：

```json
# 查询 所有字段 包含 10.95 的数据集
GET /bookdb_index/book/_search?q=10.95
# 查询 ip 包含 10.95.30.42 的数据集
GET nginx/log_base/_search?q=ip:10.95.30.42
# 使用 sort 功能需要定义 timestamp 属性 fielddata=true 有可排序功能
# 出现该错误是因为 5.x 之后，Elasticsearch对排序、聚合所依据的字段用单独的数据结构（fielddata）缓存到内存里了，
# 但是在text字段上默认是禁用的，如果有需要单独开启，这样做的目的是为了节省内存空间。
GET nginx/log_base/_search?q=ip:10.95.30.42&sort=timestamp:desc
# 使用 _mapping 查看结构定义
GET nginx/_mapping/log_base
# 改变某个属性结构
PUT nginx/_mapping/log_base
{
  "properties": {
    "timestamp":{
      "type": "text",
      "fielddata": true
    }
  }
}
```

适用于临时的在命令行使用一些工具，比如curl，快速的发出请求，来检索想要的信息；

但是如果查询请求很复杂，是很难去构建的在生产环境中，几乎很少使用 query string search

## query DSL

<p>DSL：Domain Specified Language，特定领域的语言
http request body：请求体，可以用json的格式来构建查询语法，比较方便，可以构建各种复杂的语法，比query string search肯定强大多了</p>

**查询所有**

```
GET nginx/log_base/_search
{
    "query": { "match_all": {} }
}
```

**查询 ip 包含 ，同时按照价格降序排序**

```json
GET nginx/log_base/_search
{
  "query" : {
    "match" : {
      "ip" : "10.95.30.42"
    }
  },
  "sort": [
    { "timestamp": "desc" }
  ]
}
```

**分页查询**

```json
# from：从第几个开始，es 从 0 开始计数的
# size：往后查询 100 个
GET nginx/log_base/_search
{
  "query": { "match_all": {} },
  "from": 1,
  "size": 100
}
```

**指定要查询展示的属性**

```json
GET nginx/log_base/_search
{
    "query": { "match_all": {} },
    "_source": ["ip", "status"]
}
```

更加适合生产环境的使用，可以构建复杂的查询

## query filter

**结果集里面过滤**

```json
GET nginx/log_base/_search
{
  "query": {
    "bool": {
      "must": {
        "match":{
          "ip" : "10.95.30.42" 
        }
      }, 
      "filter": {
        "match":{
          "status" : "302" 
        }
      }
    }
  }
}
```

## full-text search（全文检索）

```json
GET nginx/log_base/_search
{
  "query" : {
    "match" : {
      "url" : ".js"
    }
  }
}
```

## phrase search（短语搜索）

跟全文检索相对应，相反，全文检索会将输入的搜索串拆解开来，去倒排索引里面去一一匹配，只要能匹配上任意一个拆解后的单词，就可以作为结果返回
phrase search，要求输入的搜索串，必须在指定的字段文本中，完全包含一模一样的短语（空格等其他非数字字母分隔开的字符），才可以算匹配，才能作为结果返回

```json
GET nginx/log_base/_search
{
  "query" : {
    "match_phrase" : {
      "ip" : "10.94.53.32"
    }
  }
}
```

## highlight search（高亮搜索结果）

```json
GET nginx/log_base/_search
{
  "query" : {
    "match" : {
      "ip" : "10.94.53.32"
    }
  },
  "highlight": {
    "fields" : {
      "ip" : {}
    }
  }
}

{
  "took" : 295,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 29977,
    "max_score" : 1.5757076,
    "hits" : [
      {
        "_index" : "nginx",
        "_type" : "log_base",
        "_id" : "yAZwhmwB82qtm9SxinXv",
        "_score" : 1.5757076,
        "_source" : {
          "ip" : "10.94.53.32",
          "timestamp" : "17/Jul/2019:00:01:20 +0800",
          "url" : "GET /v-dist/static/css/app.min.css HTTP/1.1",
          "status" : "200",
          "bytes" : "217190"
        },
        "highlight" : {
          "ip" : [
            "<em>10.94.53.32</em>"
          ]
        }
      },
      {...}
    ]
  }
}
```
