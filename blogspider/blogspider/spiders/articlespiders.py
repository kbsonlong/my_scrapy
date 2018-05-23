#coding: utf8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from  blogspider.items import Article

def parse_text(extract_texts, rule_name, attr_name):
    """xpath的提取方式
    @param extract_texts: 被处理的文本数组
    @param rule_name: 规则名称
    @param attr_name: 属性名
    """
    custom_func = "%s_%s" % (rule_name, attr_name)
    if custom_func in globals():
        return globals()[custom_func](extract_texts)
    return '\n'.join(extract_texts).strip() if extract_texts else ""

class ArticleSpider(CrawlSpider):
    name = "article"

    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []

        # 添加`下一页`的规则
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page)))
        # 添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=[rule.allow_url],
            restrict_xpaths=[rule.extract_from]),
            callback='parse_item'))
        self.rules = tuple(rule_list)

        super(ArticleSpider, self).__init__()

    def parse_item(self, response):
        print response.body
        article = Article()
        article["url"] = response.url

        title = response.xpath(self.rule.title_xpath).extract()
        article["title"] = parse_text(title, self.rule.name, 'title')

        body = response.xpath(self.rule.body_xpath).extract()
        article["body"] = parse_text(body, self.rule.name, 'body')

        # author = response.xpath('//span[@class="muted"][2]/a/text()').extract()
        author = response.xpath(self.rule.author_xpath).extract()
        article["author"] = parse_text(author,self.rule.name,'author')

        publish_time = response.xpath(self.rule.publish_time_xpath).extract()
        article["publish_time"] = parse_text(publish_time, self.rule.name, 'publish_time')

        article["source_site"] = self.rule.source_site

        return article