import jieba
from snownlp import SnowNLP
import thulac
import pynlpir

def jieba_fun(text):
    # 全模式
    test1 = jieba.cut(text, cut_all=True)
    print("全模式: " + "| ".join(test1))

    # 精确模式
    test2 = jieba.cut(text, cut_all=False)
    print("精确模式: " + "| ".join(test2))

    # 搜索引擎模式
    test3 = jieba.cut_for_search(text)
    print("搜索引擎模式:" + "| ".join(test3))

def snow_fun(text):
    s = SnowNLP(text)
    # 分词
    print(s.words)
    # 情感词性计算
    print("该文本的情感词性为正的概率:" + str(s.sentiments))
    s2 = SnowNLP(text)
    # 文本关键词提取
    print(s2.keywords(10))

def thulac_fun():
    # 默认模式，分词的同时进行词性标注
    test1 = thulac.thulac()
    text1 = test1.cut("杭州西湖风景很好，是旅游胜地！")
    print(text1)

    # 只进行分词
    test2 = thulac.thulac(seg_only=True)
    text2 = test2.cut("杭州西湖风景很好，是旅游胜地！")
    print(text2)

def pynlpir_fun():
    pynlpir.open()
    text1 = "杭州西湖风景很好，是旅游胜地,每年吸引大量前来游玩的游客！"

    # 分词，默认打开分词和词性标注功能
    test1 = pynlpir.segment(text1)
    # print(test1)
    print('1.默认分词模式:\n' + str(test1))

    # 将词性标注语言变更为汉语
    test2 = pynlpir.segment(text1, pos_english=False)
    print('2.汉语标注模式:\n' + str(test2))

    # 关闭词性标注
    test3 = pynlpir.segment(text1, pos_tagging=False)
    print('3.无词性标注模式:\n' + str(test3))

if __name__ == '__main__':
    #text = "【药品商品名称】 田七痛经胶囊(望子隆) 【药品名称】 田七痛经胶囊 【批准文号】 国药准字Z20044161 【成分】 三七、五灵脂、蒲黄、延胡索、川芎、木香、小茴香、冰片。 【剂型】 本品为胶囊剂，内容物为浅灰黄色的粉末；气微香、味微甘。 【规格】 0.4g*10s*2板 【功效】 用于经期腹痛及因寒冷所致的月经失调 【用法用量】 口服，经期或经前5天，一次3～5粒，一日3次，经后可继续服用，一次3～5粒，一日2～3次。 【不良反应】 尚不明确。 【注意事项】 尚不明确。 【相互作用】 如与其他药物同时使用可能会发生药物相互作用，详情请咨询医师或药师。 【药品包装】 每盒装2板，每板10粒。 【制药公司】 云南省玉溪望子隆生物制药有限公司 【43】 非处方药物（甲类）,国家医保目录（乙类） 【注意事项】 1.经期忌生冷饮食、不宜洗凉水澡。 2.服本药时不宜同时服用人参或其制剂。 3.气血亏虚所致的痛经、月经失调不宜选用，其表现为经期或经后小腹隐痛喜按。 4.痛经伴月经失调或伴有其他疾病者，应在医师指导下服用。 5.服药后痛经不减轻，或重度痛经者，应到医院诊治。 6.有生育要求（未避孕）宜经行当日起服用至痛经缓解。 7.按用法用量服用，长期服用应向医师咨询。 8.对本品过敏者禁用，过敏体质者慎用。 9.本品性状发生改变时禁止使用。 【功能主治】 通调气血，止痛调经。用于经期腹痛及因寒所致的月经失调"
    #jieba_fun(text)
    pynlpir_fun()