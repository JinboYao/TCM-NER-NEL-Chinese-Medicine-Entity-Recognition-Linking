#  Research on Named Entity Recognition and Named Entity Linking in Traditional Chinese Medicine Manuals

![Python](https://img.shields.io/badge/language-Python%203.7-blue.svg)
![Keras](https://img.shields.io/badge/framework-Keras%202.3.1-green.svg)
![TensorFlow](https://img.shields.io/badge/framework-TensorFlow%201.14-blue.svg)
![Neo4j](https://img.shields.io/badge/database-Neo4j%203.39-green.svg)
![Fedora](https://img.shields.io/badge/OS-Fedora%2036-blue.svg)


## 1. Data Sources and Description

### 1.1 Named Entity Recognition Data Source

This study utilized open-source Traditional Chinese Medicine (TCM) manual data from the [Ali Tianchi competition](https://tianchi.aliyun.com/competition/entrance/531824/introduction) for Named Entity Recognition (NER) tasks.

### 1.2 Named Entity Linking Data Source

For the Named Entity Linking (NEL) task, we collected data from the [Chinese Medicine website](https://tianchi.aliyun.com/competition/entrance/531824/introduction) using web scraping techniques, obtaining over a thousand records related to Chinese medicine. Additionally, symptom-related data was acquired from an open knowledge graph.

## 2. Text Analysis

### 2.1 Text Length Analysis

![Text Length Analysis](https://img2.imgtp.com/2024/02/04/jTpMm1Nr.png)

### 2.2 Tokenization Analysis

In the process of Named Entity Recognition for TCM manuals, we focused on the tokenization effectiveness of professional terms such as the names of Chinese medicinal herbs and symptoms.

![Tokenization Analysis 1](https://img2.imgtp.com/2024/02/04/U59rrgGj.png)

![Tokenization Analysis 2](https://img2.imgtp.com/2024/02/04/5sew9oNm.png)

### 2.3 Frequency Analysis

The frequency analysis results are illustrated in the following figure.

![Frequency Analysis](https://img2.imgtp.com/2024/02/04/ymy5gOsi.png)

## 3. Named Entity Recognition Model

We employed the ALBERT_BiLSTM_CRF model, combining the ALBERT pre-trained model with a Bidirectional Long Short-Term Memory network (BiLSTM) and a Conditional Random Field (CRF) layer.

![NER Model](https://img2.imgtp.com/2024/02/04/UPtXLDrM.png)

## 4. Named Entity Linking

![Entity Linking](https://img2.imgtp.com/2024/02/04/0FE5fmFd.png)

## 5. Experimental Results

### 5.1 Experimental Environment

| Tool                    | Version                      |
| ----------------------- | ---------------------------- |
| Operating System        | Fedora 36                    |
| GPU                     | NVIDIA GTX1650               |
| RAM                     | 8GB                          |
| Frameworks              | Keras 2.3.1, TensorFlow 1.14 |
| Programming Language    | Python 3.7                   |
| Development Environment | Anaconda, Spyder, Jupyter    |
| Database                | Neo4j 3.39                   |

### 5.2 ALBERT_BiLSTM_CRF Model Architecture

![Model Architecture](https://img2.imgtp.com/2024/02/04/Hycr4apB.png)

### 5.3 Computational Results Showcase

![Computational Results](https://img2.imgtp.com/2024/02/04/6TxayCBW.png)

### 5.4 Loss and Accuracy Metrics

![Loss and Accuracy Metrics](https://img2.imgtp.com/2024/02/04/FGfyMGVN.png)

### 5.5 Linking Results Example

![Linking Results](https://img2.imgtp.com/2024/02/04/ool6hr7I.png)

The detailed description covers data sources, text analysis, model architecture, and experimental results, facilitating a comprehensive understanding and replication of the research process.
