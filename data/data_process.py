import json

#数据格式转换
if __name__ == '__main__':
    #打开原始数据
    with open('medical_ner_entities.json', 'r', encoding='utf-8') as f:
        data_raw = json.load(f)
    #设置训练集测试机规模 3：1
    train_test_split_size = 0.75
    train_len = int(train_test_split_size * len(data_raw))
    train_set = data_raw[:train_len]
    test_set = data_raw[train_len:]
    #保存训练数据
    with open("train.txt", 'w', encoding='utf-8') as f:
        for line in train_set:
            text = line['text']
            tag = ['O' for i in range(len(text))]
            for item in line['annotations']:
                tag[int(item['start_offset'])] = 'B-' + item['label']
                for index in range(item['start_offset'] + 1, item['end_offset']):
                    index = int(index)
                    tag[index] = 'I-' + item['label']
            for index, value in enumerate(text):
                f.write(value + " " + tag[index] + '\n')
            f.write('\n')
    #保存测试数据
    with open("test.txt", 'w', encoding='utf-8') as f:
        for line in test_set:
            text = line['text']
            tag = ['O' for i in range(len(text))]
            for item in line['annotations']:
                tag[int(item['start_offset'])] = 'B-' + item['label']
                for index in range(item['start_offset'] + 1, item['end_offset']):
                    index = int(index)
                    tag[index] = 'I-' + item['label']
            for index, value in enumerate(text):
                f.write(value + " " + tag[index] + '\n')
            f.write('\n')
    print("训练集共：" + str(len(train_set)) + "条数据")
    print("测试集共：" + str(len(test_set)) + "条数据")
