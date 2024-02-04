# -*- coding: utf-8 -*-
import json
import numpy as np
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_accuracy, crf_viterbi_accuracy
from keras.models import Model, Input
from keras.layers import Dense, Bidirectional, Dropout, LSTM, TimeDistributed, Masking
from keras.utils import to_categorical
from seqeval.metrics import classification_report
import matplotlib.pyplot as plt
from albert_zh.extract_feature import BertVector


# 载入数据
def read_data(file_path):
    # 读取数据集
    with open(file_path, "r", encoding="utf-8") as f:
        content = [_.strip() for _ in f.readlines()]
    # 添加原文句子以及该句子的标签
    # 读取空行所在的行号
    index = [-1]
    index.extend([i for i, _ in enumerate(content) if ' ' not in _])
    index.append(len(content))

    # 按空行分割，读取原文句子及标注序列
    sentences, tags = [], []
    for j in range(len(index)-1):
        sent, tag = [], []
        segment = content[index[j]+1: index[j+1]]
        for line in segment:
            sent.append(line.split()[0])
            tag.append(line.split()[-1])
        print(sent)
        print(tag)
        sentences.append(''.join(sent))
        tags.append(tag)
    # 去除空的句子及标注序列，一般放在末尾
    sentences = [_ for _ in sentences if _]
    tags = [_ for _ in tags if _]
    return sentences, tags
# 读取训练集数据
# 将标签转换成id
def label2id():

    train_sents, train_tags = read_data(train_file_path)

    # 标签转换成id，并保存成文件
    unique_tags = []
    for seq in train_tags:
        for _ in seq:
            if _ not in unique_tags:
                unique_tags.append(_)

    label_id_dict = dict(zip(unique_tags, range(1, len(unique_tags) + 1)))

    with open("%s_label2id.json" % event_type, "w", encoding="utf-8") as g:
        g.write(json.dumps(label_id_dict, ensure_ascii=False, indent=2))

def input_data(file_path):
    sentences, tags = read_data(file_path)
    # ALBERT ERCODING
    x = np.array([f(sent) for sent in sentences])
    # 对y值统一长度为MAX_SEQ_LEN
    new_y = []
    for seq in tags:
        num_tag = [label_id_dict[_] for _ in seq]
        if len(seq) < MAX_SEQ_LEN:
            num_tag = num_tag + [0] * (MAX_SEQ_LEN-len(seq))
        else:
            num_tag = num_tag[: MAX_SEQ_LEN]

        new_y.append(num_tag)

    # 将y中的元素编码成ont-hot
    y = np.empty(shape=(len(tags), MAX_SEQ_LEN, len(label_id_dict.keys())+1))

    for i, seq in enumerate(new_y):
        y[i, :, :] = to_categorical(seq, num_classes=len(label_id_dict.keys())+1)

    return x, y


# 构建模型
def build_model(max_para_length, n_tags):
    # Bert 嵌入层
    bert_output = Input(shape=(max_para_length, 312, ), name="bert_output")
    # LSTM 层
    lstm = Bidirectional(LSTM(units=128, return_sequences=True), name="bi_lstm")(bert_output)
    drop = Dropout(0.4, name="dropout")(lstm)
    dense = TimeDistributed(Dense(n_tags, activation="softmax"), name="time_distributed")(drop)
    #CRF层
    crf = CRF(n_tags)
    out = crf(dense)
    model = Model(inputs=bert_output, outputs=out)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.compile(loss=crf.loss_function, optimizer='adam', metrics=[crf.accuracy])
    # 模型结构总结
    model.summary()
    return model

# 模型训练
def train_model(event_type,label_id_dict,train_file_path,test_file_path,MAX_SEQ_LEN,batch_size, epochs):
    # 读取训练集，验证集和测试集数据
    print("使用 ALBERT 对训练集编码")
    train_x, train_y = input_data(train_file_path)
    print("使用 ALBERT 对测试集编码")
    test_x, test_y = input_data(test_file_path)
    print(" ALBERT 编码完成")
    # 模型训练
    model = build_model(MAX_SEQ_LEN, len(label_id_dict.keys())+1)
    history = model.fit(train_x, train_y, validation_data=(test_x, test_y), batch_size=batch_size, epochs=epochs,verbose=1)
    model.save("%s_ner.h5" % event_type)

    # 绘制loss和acc图像
    plt.subplot(2, 1, 1)
    epochs = len(history.history['loss'])
    plt.plot(range(epochs), history.history['loss'], label='loss')
    plt.plot(range(epochs), history.history['val_loss'], label='val_loss')
    plt.legend()
    plt.subplot(2, 1, 2)
    epochs = len(history.history['crf_viterbi_accuracy'])
    plt.plot(range(epochs), history.history['crf_viterbi_accuracy'], label='crf_viterbi_accuracy')
    plt.plot(range(epochs), history.history['val_crf_viterbi_accuracy'], label='val_crf_viterbi_accuracy')
    plt.legend()
    plt.savefig("%s_loss_acc.png" % event_type)
    # 模型在测试集上的表现
    # 预测标签
    y = np.argmax(model.predict(test_x), axis=2)
    pred_tags = []
    for i in range(y.shape[0]):
        pred_tags.append([id_label_dict[_] for _ in y[i] if _])

    # 因为存在预测的标签长度与原来的标注长度不一致的情况，因此需要调整预测的标签
    test_sents, test_tags = read_data(test_file_path)
    final_tags = []
    for test_tag, pred_tag in zip(test_tags, pred_tags):
        if len(test_tag) == len(pred_tag):
            final_tags.append(test_tag)
        elif len(test_tag) < len(pred_tag):
            final_tags.append(pred_tag[:len(test_tag)])
        else:
            final_tags.append(pred_tag + ['O'] * (len(test_tag) - len(pred_tag)))

    # 利用seqeval对测试集进行验证
    print(classification_report(test_tags, final_tags, digits=4))


if __name__ == '__main__':
    batch_size = 16
    epochs = 3
    event_type = "subtask1"
    train_file_path = "./data/train.txt"
    test_file_path = "./data/test.txt"
    MAX_SEQ_LEN = 128  # 输入的文本最大长度
    # 利用ALBERT提取文本特征
    label2id()
    bert_model = BertVector(pooling_strategy="NONE", max_seq_len=MAX_SEQ_LEN)
    f = lambda text: bert_model.encode([text])["encodes"][0]

    # 读取label2id字典
    with open("%s_label2id.json" % event_type, "r", encoding="utf-8") as h:
        label_id_dict = json.loads(h.read())

    id_label_dict = {v: k for k, v in label_id_dict.items()}
    # 模型训练
    train_model(event_type,label_id_dict,train_file_path,test_file_path,MAX_SEQ_LEN,batch_size, epochs)


