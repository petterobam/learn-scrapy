<section class="col-article"><div class="col-markdown-nav absolute" style="position: fixed; top: 74px; left: 1080px; max-height: 281px;">

## 在这篇文章中：

*   [例子：](javascript:; "例子：")

        *   [1. 基本的匹配（Query）查询](javascript:; "1. 基本的匹配（Query）查询")
    *   [2. 多字段（Multi-filed）查询](javascript:; "2. 多字段（Multi-filed）查询")
    *   [3. Boosting](javascript:; "3. Boosting")
    *   [4. Bool 查询](javascript:; "4. Bool 查询")
    *   [5. 模糊（Fuzzy）查询](javascript:; "5. 模糊（Fuzzy）查询")
    *   [6. 通配符（Wildcard）查询](javascript:; "6. 通配符（Wildcard）查询")
    *   [7. 正则（Regexp）查询](javascript:; "7. 正则（Regexp）查询")
    *   [8. 短语匹配(Match Phrase)查询](javascript:; "8. 短语匹配(Match Phrase)查询")
    *   [9. 短语前缀（Match Phrase Prefix）查询](javascript:; "9. 短语前缀（Match Phrase Prefix）查询")
    *   [10. 查询字符串（Query String）](javascript:; "10. 查询字符串（Query String）")
    *   [11. 简单查询字符串（Simple Query String）](javascript:; "11. 简单查询字符串（Simple Query String）")
    *   [12. 词条（Term）/多词条（Terms）查询](javascript:; "12. 词条（Term）/多词条（Terms）查询")</div><div class="c-markdown J-articleContent">

为了演示不同类型的 **ElasticSearch** 的查询，我们将使用书文档信息的集合（有以下字段：**title**（标题）, **authors**（作者）, **summary**（摘要）, **publish_date**（发布日期）和 **num_reviews**（浏览数））。

在这之前，首先我们应该先创建一个新的索引（index），并批量导入一些文档：

创建索引：
<pre class="prism-token token  language-javascript">PUT <span class="token operator">/</span>bookdb_index
    <span class="token punctuation">{</span> <span class="token string">"settings"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"number_of_shards"</span><span class="token punctuation">:</span> <span class="token number">1</span> <span class="token punctuation">}</span><span class="token punctuation">}</span> </pre>

批量上传文档：
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_bulk
    <span class="token punctuation">{</span> <span class="token string">"index"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token number">1</span> <span class="token punctuation">}</span><span class="token punctuation">}</span>
    <span class="token punctuation">{</span> <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch: The Definitive Guide"</span><span class="token punctuation">,</span> <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"clinton gormley"</span><span class="token punctuation">,</span> <span class="token string">"zachary tong"</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">"summary"</span> <span class="token punctuation">:</span> <span class="token string">"A distibuted real-time search and analytics engine"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span> <span class="token punctuation">:</span> <span class="token string">"2015-02-07"</span><span class="token punctuation">,</span> <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">20</span><span class="token punctuation">,</span> <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"oreilly"</span> <span class="token punctuation">}</span>
    <span class="token punctuation">{</span> <span class="token string">"index"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token number">2</span> <span class="token punctuation">}</span><span class="token punctuation">}</span>
    <span class="token punctuation">{</span> <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Taming Text: How to Find, Organize, and Manipulate It"</span><span class="token punctuation">,</span> <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"grant ingersoll"</span><span class="token punctuation">,</span> <span class="token string">"thomas morton"</span><span class="token punctuation">,</span> <span class="token string">"drew farris"</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">"summary"</span> <span class="token punctuation">:</span> <span class="token string">"organize text using approaches such as full-text search, proper name recognition, clustering, tagging, information extraction, and summarization"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span> <span class="token punctuation">:</span> <span class="token string">"2013-01-24"</span><span class="token punctuation">,</span> <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">12</span><span class="token punctuation">,</span> <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span> <span class="token punctuation">}</span>
    <span class="token punctuation">{</span> <span class="token string">"index"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token number">3</span> <span class="token punctuation">}</span><span class="token punctuation">}</span>
    <span class="token punctuation">{</span> <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch in Action"</span><span class="token punctuation">,</span> <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"radu gheorge"</span><span class="token punctuation">,</span> <span class="token string">"matthew lee hinman"</span><span class="token punctuation">,</span> <span class="token string">"roy russo"</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">"summary"</span> <span class="token punctuation">:</span> <span class="token string">"build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span> <span class="token punctuation">:</span> <span class="token string">"2015-12-03"</span><span class="token punctuation">,</span> <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">18</span><span class="token punctuation">,</span> <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span> <span class="token punctuation">}</span>
    <span class="token punctuation">{</span> <span class="token string">"index"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token number">4</span> <span class="token punctuation">}</span><span class="token punctuation">}</span>
    <span class="token punctuation">{</span> <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span> <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"trey grainger"</span><span class="token punctuation">,</span> <span class="token string">"timothy potter"</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token string">"summary"</span> <span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span> <span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span><span class="token punctuation">,</span> <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">23</span><span class="token punctuation">,</span> <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span> <span class="token punctuation">}</span></pre>

## **例子：**

### **1. 基本的匹配（Query）查询**

有两种方式来执行一个全文匹配查询：

*   使用 **Search Lite API**，它从 `url` 中读取所有的查询参数
*   使用完整 **JSON** 作为请求体，这样你可以使用完整的 **Elasticsearch DSL**

下面是一个基本的匹配查询，查询任一字段包含 Guide 的记录
<pre class="prism-token token  language-javascript">GET <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search<span class="token operator">?</span>q<span class="token operator">=</span>guide

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.28168046</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch: The Definitive Guide"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"clinton gormley"</span><span class="token punctuation">,</span> <span class="token string">"zachary tong"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"A distibuted real-time search and analytics engine"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-02-07"</span><span class="token punctuation">,</span>
          <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">20</span><span class="token punctuation">,</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.24144039</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"trey grainger"</span><span class="token punctuation">,</span> <span class="token string">"timothy potter"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span><span class="token punctuation">,</span>
          <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">23</span><span class="token punctuation">,</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

下面是完整 Body 版本的查询，生成相同的内容：
<pre class="prism-token token  language-javascript"><span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"multi_match"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"query"</span> <span class="token punctuation">:</span> <span class="token string">"guide"</span><span class="token punctuation">,</span>
            <span class="token string">"fields"</span> <span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"_all"</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span></pre>

`multi_match` 是 `match` 的作为在多个字段运行相同操作的一个速记法。`fields` 属性用来指定查询针对的字段，在这个例子中，我们想要对文档的所有字段进行匹配。两个 **API** 都允许你指定要查询的字段。例如，查询 `title` 字段中包含 **in Action** 的书：
<pre class="prism-token token  language-javascript">GET <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search<span class="token operator">?</span>q<span class="token operator">=</span>title<span class="token punctuation">:</span><span class="token keyword">in</span> action

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.6259885</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"trey grainger"</span><span class="token punctuation">,</span>
            <span class="token string">"timothy potter"</span>
          <span class="token punctuation">]</span><span class="token punctuation">,</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span><span class="token punctuation">,</span>
          <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">23</span><span class="token punctuation">,</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"3"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.5975345</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"radu gheorge"</span><span class="token punctuation">,</span>
            <span class="token string">"matthew lee hinman"</span><span class="token punctuation">,</span>
            <span class="token string">"roy russo"</span>
          <span class="token punctuation">]</span><span class="token punctuation">,</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-12-03"</span><span class="token punctuation">,</span>
          <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">18</span><span class="token punctuation">,</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

然而， 完整的 **DSL** 给予你灵活创建更复杂查询和指定返回结果的能力（后面，我们会一一阐述）。在下面例子中，我们指定 `size`限定返回的结果条数，from 指定起始位子，`_source` 指定要返回的字段，以及语法高亮
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"match"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"title"</span> <span class="token punctuation">:</span> <span class="token string">"in action"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"size"</span><span class="token punctuation">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
    <span class="token string">"from"</span><span class="token punctuation">:</span> <span class="token number">0</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span> <span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span> <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"fields"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"title"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
    <span class="token string">"total"</span><span class="token punctuation">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
    <span class="token string">"max_score"</span><span class="token punctuation">:</span> <span class="token number">0.9105287</span><span class="token punctuation">,</span>
    <span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"3"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.9105287</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-12-03"</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"Elasticsearch &lt;em&gt;in&lt;/em&gt; &lt;em&gt;Action&lt;/em&gt;"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.9105287</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"Solr &lt;em&gt;in&lt;/em&gt; &lt;em&gt;Action&lt;/em&gt;"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
  <span class="token punctuation">}</span></pre>

注意：对于多个词查询，`match` 允许指定是否使用 `and` 操作符来取代默认的 `or` 操作符。你还可以指定 `mininum_should_match` 选项来调整返回结果的相关程度。具体看后面的例子。

### **2. 多字段（Multi-filed）查询**

正如我们已经看到来的，为了根据多个字段检索（e.g. 在 `title` 和 `summary` 字段都是相同的查询字符串的结果），你可以使用 `multi_match` 语句
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"multi_match"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"query"</span> <span class="token punctuation">:</span> <span class="token string">"elasticsearch guide"</span><span class="token punctuation">,</span>
            <span class="token string">"fields"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
    <span class="token string">"total"</span><span class="token punctuation">:</span> <span class="token number">3</span><span class="token punctuation">,</span>
    <span class="token string">"max_score"</span><span class="token punctuation">:</span> <span class="token number">0.9448582</span><span class="token punctuation">,</span>
    <span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.9448582</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch: The Definitive Guide"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"clinton gormley"</span><span class="token punctuation">,</span>
            <span class="token string">"zachary tong"</span>
          <span class="token punctuation">]</span><span class="token punctuation">,</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"A distibuted real-time search and analytics engine"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-02-07"</span><span class="token punctuation">,</span>
          <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">20</span><span class="token punctuation">,</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"3"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.17312013</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"radu gheorge"</span><span class="token punctuation">,</span>
            <span class="token string">"matthew lee hinman"</span><span class="token punctuation">,</span>
            <span class="token string">"roy russo"</span>
          <span class="token punctuation">]</span><span class="token punctuation">,</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-12-03"</span><span class="token punctuation">,</span>
          <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">18</span><span class="token punctuation">,</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.14965448</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"trey grainger"</span><span class="token punctuation">,</span>
            <span class="token string">"timothy potter"</span>
          <span class="token punctuation">]</span><span class="token punctuation">,</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span><span class="token punctuation">,</span>
          <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">23</span><span class="token punctuation">,</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
  <span class="token punctuation">}</span></pre>

**注：**第三条被匹配，因为 `guide` 在 `summary` 字段中被找到。

### **3. Boosting**

由于我们是多个字段查询，我们可能需要提高某一个字段的分值。在下面的例子中，我们把 `summary` 字段的分数提高三倍，为了提升 `summary` 字段的重要度；因此，我们把文档 4 的相关度提高了。
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"multi_match"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"query"</span> <span class="token punctuation">:</span> <span class="token string">"elasticsearch guide"</span><span class="token punctuation">,</span>
            <span class="token string">"fields"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary^3"</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.31495273</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"A distibuted real-time search and analytics engine"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch: The Definitive Guide"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-02-07"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.14965448</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"3"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.13094766</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-12-03"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

**注：**提升不是简简单单通过提升因子把计算分数加成。实际的 `boost` 值通过归一化和一些内部优化给出的。相关信息请见 Elasticsearch guide

### **4. Bool 查询**

为了提供更相关或者特定的结果，`AND`/`OR`/`NOT` 操作符可以用来调整我们的查询。它是以 **布尔查询** 的方式来实现的。**布尔查询** 接受如下参数：

*   `must` 等同于 `AND`
*   `must_not` 等同于 `NOT`
*   `should` 等同于 `OR`

打比方，如果我想要查询这样类型的书：书名包含 **ElasticSearch** 或者（`OR`） **Solr**，并且（`AND`）它的作者是 **Clinton Gormley**不是（`NOT`）**Radu Gheorge**
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"bool"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"must"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
                <span class="token string">"bool"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"should"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
                      <span class="token punctuation">{</span> <span class="token string">"match"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch"</span> <span class="token punctuation">}</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
                      <span class="token punctuation">{</span> <span class="token string">"match"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr"</span> <span class="token punctuation">}</span><span class="token punctuation">}</span> <span class="token punctuation">]</span> <span class="token punctuation">}</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token string">"must"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"match"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token string">"clinton gormely"</span> <span class="token punctuation">}</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token string">"must_not"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span> <span class="token string">"match"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span><span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token string">"radu gheorge"</span> <span class="token punctuation">}</span><span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.3672021</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch: The Definitive Guide"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"clinton gormley"</span><span class="token punctuation">,</span>
            <span class="token string">"zachary tong"</span>
          <span class="token punctuation">]</span><span class="token punctuation">,</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"A distibuted real-time search and analytics engine"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-02-07"</span><span class="token punctuation">,</span>
          <span class="token string">"num_reviews"</span><span class="token punctuation">:</span> <span class="token number">20</span><span class="token punctuation">,</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"oreilly"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

**注**：正如你所看到的，**布尔查询** 可以包装任何其他查询类型，包括其他布尔查询，以创建任意复杂或深度嵌套的查询。

### **5. 模糊（Fuzzy）查询**

在进行匹配和多项匹配时，可以启用模糊匹配来捕捉拼写错误，模糊度是基于原始单词的编辑距离来指定的。
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"multi_match"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"query"</span> <span class="token punctuation">:</span> <span class="token string">"comprihensiv guide"</span><span class="token punctuation">,</span>
            <span class="token string">"fields"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token string">"fuzziness"</span><span class="token punctuation">:</span> <span class="token string">"AUTO"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string">"size"</span><span class="token punctuation">:</span> <span class="token number">1</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.5961596</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
<span class="token punctuation">]</span></pre>

**注**：当术语长度大于 5 个字符时，`AUTO` 的模糊值等同于指定值 “2”。但是，80％ 拼写错误的编辑距离为 1，所以，将模糊值设置为 `1`可能会提高您的整体搜索性能。更多详细信息，请参阅**Elasticsearch指南中的“排版和拼写错误”（Typos and Misspellings）**。

### **6. 通配符（Wildcard）查询**

**通配符查询** 允许你指定匹配的模式，而不是整个术语。

*   `？` 匹配任何字符
*   `*` 匹配零个或多个字符。

例如，要查找名称以字母’t’开头的所有作者的记录：
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"wildcard"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"authors"</span> <span class="token punctuation">:</span> <span class="token string">"t*"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"authors"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"fields"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"authors"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch: The Definitive Guide"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"clinton gormley"</span><span class="token punctuation">,</span>
            <span class="token string">"zachary tong"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"zachary &lt;em&gt;tong&lt;/em&gt;"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"2"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Taming Text: How to Find, Organize, and Manipulate It"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"grant ingersoll"</span><span class="token punctuation">,</span>
            <span class="token string">"thomas morton"</span><span class="token punctuation">,</span>
            <span class="token string">"drew farris"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"&lt;em&gt;thomas&lt;/em&gt; morton"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"trey grainger"</span><span class="token punctuation">,</span>
            <span class="token string">"timothy potter"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"&lt;em&gt;trey&lt;/em&gt; grainger"</span><span class="token punctuation">,</span>
            <span class="token string">"&lt;em&gt;timothy&lt;/em&gt; potter"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span> </pre>

### **7. 正则（Regexp）查询**

**正则查询** 让你可以使用比 **通配符查询** 更复杂的模式进行查询：
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"regexp"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"authors"</span> <span class="token punctuation">:</span> <span class="token string">"t[a-z]*y"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"authors"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"fields"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"authors"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"trey grainger"</span><span class="token punctuation">,</span>
            <span class="token string">"timothy potter"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"&lt;em&gt;trey&lt;/em&gt; grainger"</span><span class="token punctuation">,</span>
            <span class="token string">"&lt;em&gt;timothy&lt;/em&gt; potter"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

### **8. 短语匹配(Match Phrase)查询**

**短语匹配查询** 要求在请求字符串中的所有查询项必须都在文档中存在，文中顺序也得和请求字符串一致，且彼此相连。默认情况下，查询项之间必须紧密相连，但可以设置 `slop` 值来指定查询项之间可以分隔多远的距离，结果仍将被当作一次成功的匹配。
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"multi_match"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token string">"search engine"</span><span class="token punctuation">,</span>
            <span class="token string">"fields"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token string">"type"</span><span class="token punctuation">:</span> <span class="token string">"phrase"</span><span class="token punctuation">,</span>
            <span class="token string">"slop"</span><span class="token punctuation">:</span> <span class="token number">3</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span> <span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span> <span class="token punctuation">]</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.22327082</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.16113183</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"A distibuted real-time search and analytics engine"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch: The Definitive Guide"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-02-07"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

**注**：在上述例子中，对于非整句类型的查询，`_id` 为 1 的文档一般会比 `_id` 为 4 的文档得分高，结果位置也更靠前，因为它的字段长度较短，但是对于 **短语匹配类型** 查询，由于查询项之间的接近程度是一个计算因素，因此 `_id` 为 4 的文档得分更高。

### **9. 短语前缀（Match Phrase Prefix）查询**

**短语前缀式查询** 能够进行 **即时搜索（search-as-you-type）** 类型的匹配，或者说提供一个查询时的初级自动补全功能，无需以任何方式准备你的数据。和 `match_phrase` 查询类似，它接收`slop` 参数（用来调整单词顺序和不太严格的相对位置）和 `max_expansions`参数（用来限制查询项的数量，降低对资源需求的强度）。
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"match_phrase_prefix"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
                <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token string">"search en"</span><span class="token punctuation">,</span>
                <span class="token string">"slop"</span><span class="token punctuation">:</span> <span class="token number">3</span><span class="token punctuation">,</span>
                <span class="token string">"max_expansions"</span><span class="token punctuation">:</span> <span class="token number">10</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span> <span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">,</span> <span class="token string">"publish_date"</span> <span class="token punctuation">]</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.5161346</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"Comprehensive guide to implementing a scalable search engine using Apache Solr"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.37248808</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"A distibuted real-time search and analytics engine"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch: The Definitive Guide"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-02-07"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

**注**：采用 **查询时即时搜索** 具有较大的性能成本。更好的解决方案是采用 **索引时即时搜索**。更多信息，请查看 **自动补齐接口（Completion Suggester API）** 或 **边缘分词器（Edge-Ngram filters）的用法**。

### **10. 查询字符串（Query String）**

**查询字符串** 类型（**query_string**）的查询提供了一个方法，用简洁的简写语法来执行 **多匹配查询**、 **布尔查询** 、 **提权查询**、 **模糊查询**、 **通配符查询**、 **正则查询** 和**范围查询**。下面的例子中，我们在那些作者是 **“grant ingersoll”** 或 **“tom morton”** 的某本书当中，使用查询项 **“search algorithm”** 进行一次模糊查询，搜索全部字段，但给 `summary` 的权重提升 2 倍。
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"query_string"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token string">"(saerch~1 algorithm~1) AND (grant ingersoll)  OR (tom morton)"</span><span class="token punctuation">,</span>
            <span class="token string">"fields"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"_all"</span><span class="token punctuation">,</span> <span class="token string">"summary^2"</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span> <span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">,</span> <span class="token string">"authors"</span> <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"fields"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"summary"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"2"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">0.14558059</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token string">"organize text using approaches such as full-text search, proper name recognition, clustering, tagging, information extraction, and summarization"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Taming Text: How to Find, Organize, and Manipulate It"</span><span class="token punctuation">,</span>
          <span class="token string">"authors"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"grant ingersoll"</span><span class="token punctuation">,</span>
            <span class="token string">"thomas morton"</span><span class="token punctuation">,</span>
            <span class="token string">"drew farris"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"summary"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
            <span class="token string">"organize text using approaches such as full-text &lt;em&gt;search&lt;/em&gt;, proper name recognition, clustering, tagging, information extraction, and summarization"</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

### **11. 简单查询字符串（Simple Query String）**

**简单请求字符串** 类型（**simple_query_string**）的查询是请求**字符串类型**（**query_string**）查询的一个版本，它更适合那种仅暴露给用户一个简单搜索框的场景；因为它用 `+/\|/-` 分别替换了 `AND/OR/NOT`，并且自动丢弃了请求中无效的部分，不会在用户出错时，抛出异常。
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"simple_query_string"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token string">"(saerch~1 algorithm~1) + (grant ingersoll)  | (tom morton)"</span><span class="token punctuation">,</span>
            <span class="token string">"fields"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"_all"</span><span class="token punctuation">,</span> <span class="token string">"summary^2"</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span> <span class="token string">"title"</span><span class="token punctuation">,</span> <span class="token string">"summary"</span><span class="token punctuation">,</span> <span class="token string">"authors"</span> <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string">"highlight"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"fields"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"summary"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span> </pre>

### **12. 词条（Term）/多词条（Terms）查询**

以上例子均为 `full-text`(全文检索) 的示例。有时我们对结构化查询更感兴趣，希望得到更准确的匹配并返回结果，**词条查询** 和 **多词条查询** 可帮我们实现。在下面的例子中，我们要在索引中找到所有由 **Manning** 出版的图书。
<pre class="prism-token token  language-javascript">POST <span class="token operator">/</span>bookdb_index<span class="token operator">/</span>book<span class="token operator">/</span>_search
<span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"term"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string">"_source"</span> <span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"title"</span><span class="token punctuation">,</span><span class="token string">"publish_date"</span><span class="token punctuation">,</span><span class="token string">"publisher"</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span>

<span class="token punctuation">[</span>Results<span class="token punctuation">]</span>
<span class="token string">"hits"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"2"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">1.2231436</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Taming Text: How to Find, Organize, and Manipulate It"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2013-01-24"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"3"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">1.2231436</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Elasticsearch in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2015-12-03"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token string">"_index"</span><span class="token punctuation">:</span> <span class="token string">"bookdb_index"</span><span class="token punctuation">,</span>
        <span class="token string">"_type"</span><span class="token punctuation">:</span> <span class="token string">"book"</span><span class="token punctuation">,</span>
        <span class="token string">"_id"</span><span class="token punctuation">:</span> <span class="token string">"4"</span><span class="token punctuation">,</span>
        <span class="token string">"_score"</span><span class="token punctuation">:</span> <span class="token number">1.2231436</span><span class="token punctuation">,</span>
        <span class="token string">"_source"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
          <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token string">"manning"</span><span class="token punctuation">,</span>
          <span class="token string">"title"</span><span class="token punctuation">:</span> <span class="token string">"Solr in Action"</span><span class="token punctuation">,</span>
          <span class="token string">"publish_date"</span><span class="token punctuation">:</span> <span class="token string">"2014-04-05"</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span></pre>

可使用词条关键字来指定多个词条，将搜索项用数组传入。
<pre class="prism-token token  language-javascript"><span class="token punctuation">{</span>
    <span class="token string">"query"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>
        <span class="token string">"terms"</span> <span class="token punctuation">:</span> <span class="token punctuation">{</span>
            <span class="token string">"publisher"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"oreilly"</span><span class="token punctuation">,</span> <span class="token string">"packt"</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span> </pre><figure><div class="image-block"><span>![](https://ask.qcloudimg.com/http-save/yehe-2511396/ka568ygtz8.gif)</span></div></figure>

- 下节再续 -
<figure></figure><figure></figure></div><div class="col-article-source">

原文发布于微信公众号 - <!-- -->我的小碗汤（mysmallsoup）

原文发表时间：<!-- -->2018-09-08

本文参与[腾讯云自媒体分享计划](/developer/support-plan)，欢迎正在阅读的你也加入，一起分享。
</div><div class="col-article-time"><span>发表于 <time datetime="2018-09-30 10:33:09" title="2018-09-30 10:33:09"> 2018-09-30<span class="com-v-box">2018-09-30 10:33:09</span></time></span></div><div class="col-article-tags"><nav class="col-tags">[其他](/developer/tag/125?entry=article)</nav><div class="extra-part"><div class="com-operations">[举报](javascript:;)</div></div></div><div class="com-widget-operations" style="top: 114px;"><div class="main-cnt">[<span class="text">5</span>](javascript:;)</div><div class="extra-cnt"><span class="com-opt-text share-text">分享</span>

*   <div class="c-bubble-trigger">[](javascript:;)<div class="c-bubble c-bubble-left "><div class="c-bubble-inner"><div class="qr-img" title="https://cloud.tencent.com/developer/article/1350622"><canvas width="100" height="100" style="display: none;"></canvas>![Scan me!](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAHF0lEQVR4Xu2dbZPiMAyD4f//6L3heJk0daTHSYDZHd/Ho6SNZVuSW7rXy+Xyc1n89/NzXOJ6vZ5WbI9Rn7efPb/z/D+3xvOk/fW0FxOtT7dPr5uuFx13i1wBAiP4UUBUVoVINlVAM7LPYJetfWW4ynuuHx0X7SG67uw5+iq+nWcllq8KWVmkALlcXHKpImy/ewLEZRfJCMUDbQZlzxVxiEukiH9gh3odRtZwe1YVWoAkESlAHgEjKqsq5CFxac9U2eXWUC2NtE5XCGT92xq/vkIi3e8Ujfu8D24BMmgjGZJWxo1koQOa+ARqLl11KTMcJctXSN2ppgLkCEsE3FbZW4DcA761QlypRm6YGEPHEU4tteTaXiP53mhPWcFBWuKvceoFyDjVQ2NIK4OQk3PUanqrvuvcsFJes+ccyV4yZ5uJ6dZp7yc3TYIf9fNPJMsMEC8q2Dl+L0BWoLh/9/qzword+SnpKfkbbYmuS6uGyG8a2o3hK0Cc0CCgvB2Q7A0ad9HZEYeab62Quqq8GfeuvEZ2z+21nVpWAXJ+HoAoy8gbueFpmCSzpO7Uiquc/nMqCHpj6trODtOq9rLiyuXoJBvAAuQesQLkkTnZsQflkL4CXaJuB+Qpe2dbRtQ7nXSlyqTns9nv0aCOjiPgz1xb2G4LEP/YzkcBeZK6IkeHPpnrUPKlI/xZcznDfbPdg8btIHsLkLkK2VE1UfLJB+XobdWqkCP7ZOMWGkPVKpyTdaV5O2G2FSkzNlrvXZ6DzMhcDHB8e1LfHYisjCQm7E8D0nMInRepwM2ska0gkrUuubJ7cHJeCQ06sZYPOcwOyQqQ8y88CpBB+rteH7VYwk3OIGNAFIdkxwI7NpNtM9mJKp1mH5TP47cwO4CJ1sUqqwC5h4rI2BWgQ2OYVTfOeffrzbSKniRXNj2bXE6y03XpZAE9dULHDVRrU3VTgAAiJCODLA+4vqqy0FUemSLMEDJJlpk4oGd7XXvqA+YqSg3rVHAcgdN1afuIRErmu1PXq4whNToFSNxapgAhslf1/EiFOPKlbY+0KmdCs62FmuF+j64rUEvweurEBZEQMQmgk5ErASbndyOarwPSP3Xi+EIR1c7Mj4h+Jgtp21WVpGJCZ2pOfLwqqAA5pli2QgqQR/xoNf7aCsElFcx1yGghanW0nytCzK6RFSij44m/iVqs9TzqnroKIu3nRAyMjumThBK+2zS5JpegbwNkx2NA2SloxlyNVBkdZ6vgE1XWnj8C2lWoq8j+85PspZnvTE/UZvqTuyzs16AtgAapAOkQKUDO9bP1MSDlUbKlG7WKd3mkyPPQ612RvVElFyBd5Gm763nQCQ6aTOh+iCMzQuoz3KQ4h957IQGmwcruwR0fTqezP9ihTpYQMg1EpMoKkEdUCpB7IMikYKlCVsiJEKCTydlp87uPd3vKTifC9hRNPd7x5GK0mQLk/mNSWzUEECoLqdFS2aeAo0rGgX9yx8E7iLPncp4Kc14BEr9z92uAkKffqeEjRBdJ6FEFkuGi6/VE7WX3N2MDiPz+LxYKkBhSKsmp6ixABg7cDSgjz9NX2UcqJDppVgrTkXg2q1S20kxWrW0HITshQdu5fNdJAXI0gYprtgGiRic0M2l/VLMp512IhidrUBGwUnlZ+d/GTw4XC5AjfDTxChCR9jSIpHrpWlsBcQSnFAdVKFlSzxKy6+fKm9ApAt2rAjoC+NSyCpAxJHSgicckwR9Pm1ZZI3fdky8lWnKTa7ejpllO1KYbGipbcYhl/1ZSOsMpQO4/faZj9QKkK6cVov1ohez4wQ4h3SzRuvZEFU/fligPRB0g603c8eHnBcjc65l2qk3JITQzqOOlx5FZz4oCJG2HXmt7HG2FdM4nXzWevW88syHiCbLXQTevgkn3UoCASP0JQEjLALH4f4hrLUoqqnbgSNIJgVamtteZFQg0DjPHyaffCXGRIPTHFCBjqN7y5ypmMpkA60yrWoPyEDV6ZD1XeRH/FCAdil8HJPtsL8nCGVlI+u1KhUTtl1YyUVL02tzMK/30ewFyjEDW3xQgjz+m/OsqxEnVkVJyMtcR23Pd2bbQXhfxH9k21Upll92zMTrsIfuzaJppWclcgNwjht6X5Ug6W12EwKPMd+fZUSGqgqIKye7FxbIA6V6DXoCAFCMmrO31Kgsdh/wpQEjLcCJAkbRrGTSYhN9mzqVIHeTdfg4pQI5hpwpTqiy3CDFCNLucu+0z3l1b1rT2kptK6JEU7ivPiZCoUreS+uwUt21j6t57ARKkXFXIwy+I98FTEYIqBJNP8EPJ6Lv0xhct79W24Nw2DSY5TlX7qO3Jd50ocNzJSODoGlmg6fF01E7XUyqLKsCt014iJyOPMPIQ/QZdFdFqJF1gVyWpxAwTYuf9kAJkDDWtxqqQQQy/VSH/APVfyjf6OB18AAAAAElFTkSuQmCC)</div>

    分享文章到朋友圈
</div></div></div>
*   <div class="c-bubble-trigger">[](javascript:;)<div class="c-bubble c-bubble-left "><div class="c-bubble-inner"><span>分享文章到 QQ</span></div></div></div>
*   <div class="c-bubble-trigger">[](javascript:;)<div class="c-bubble c-bubble-left "><div class="c-bubble-inner"><span>分享文章到微博</span></div></div></div>
*   <div class="c-bubble-trigger">[](javascript:;)<div class="c-bubble c-bubble-left "><div class="c-bubble-inner"><span>复制文章链接到剪贴板</span></div></div></div><div class="c-bubble-trigger com-widget-qr"><button class="scan-btn" hotrep="community.edge-widget.follow-oa">扫描二维码</button><div class="c-bubble c-bubble-left "><div class="c-bubble-inner"><div class="qr-img">![](//imgcache.qq.com/open_proj/proj_qcloud_v2/community/portal/css/img/wechat-qr.jpg)</div>

扫码关注云+社区

领取腾讯云代金券
</div></div></div></div></div></section>