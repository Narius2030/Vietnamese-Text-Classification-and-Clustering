# Vietnamese-Text-Classification-and-Clustering

## Introduction
> ### Text classification
- In Text Classification task, I apply natural language processing techniques first for normalizing text and then I design a neural network using `LSTM` for learning the features of each paragraph
- I choose `Softmax activation` function for classification in the final layer, the number of the unit in this layer are equal to the number of class I want to predict
> ### Text clustering
- In the Text Clustering task, I implement `Word2Vec (skip-gram)` for finding the relationships among words. 
- Then, I embed word for the whole paragraphs and calculate the `mean vectors` which represent for `embedded paragraphs`
- Finally, I calculate the `Cosine similarity` to estimate the similar among paragraphs so that I can cluster similar paragraphs into groups

### Buil Model
> ### Text classification
```python
drop_out = 0.2
output_unit = topic_size
embedding_size = 128

model = models.Sequential([
  layers.Embedding(vocab_size, embedding_size),
  layers.BatchNormalization(),
  layers.LSTM(64, return_sequences=True),
  layers.LSTM(64),
  layers.Dropout(drop_out),
  layers.Dense(9, activation='relu'),
  layers.Dense(9, activation='relu'),
  layers.Dense(9, activation='relu'),
  layers.Dense(9, activation='relu'),
  layers.Dense(units=output_unit, activation='softmax')
])
```
```markdown
___________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding (Embedding)       (None, None, 128)         4699392   
                                                                 
 batch_normalization (Batch  (None, None, 128)         512       
 Normalization)                                                  
                                                                 
 lstm (LSTM)                 (None, None, 64)          49408     
                                                                 
 lstm_1 (LSTM)               (None, 64)                33024     
                                                                 
 dropout (Dropout)           (None, 64)                0         
                                                                 
 dense (Dense)               (None, 9)                 585       
                                                                 
 dense_1 (Dense)             (None, 9)                 90        
                                                                 
 dense_2 (Dense)             (None, 9)                 90        
                                                                 
 dense_3 (Dense)             (None, 9)                 90        
                                                                 
 dense_4 (Dense)             (None, 7)                 70        
                                                                 
=================================================================
Total params: 4783261 (18.25 MB)
Trainable params: 4783005 (18.25 MB)
Non-trainable params: 256 (1.00 KB)
_________________________________________________________________
```

>### Text clustering
```python
# Calculate sentence embeddings by averaging word embeddings
mean_sentence_embedding = mean_vector_embedding(question_embeddings)
mean_post_embedding = mean_embedded_posts(post_embeddings)
```
```python
# Calculate similarity (cosine similarity)
similarity_score = cosine_similarity([mean_sentence_embedding], mean_post_embedding)
```
- Example with a short sentence
```python
question = '''Với CLB Hà Lan, tiền đạo cánh người Brazil đạt tỷ lệ ghi bàn và kiến tạo kỳ vọng là 0,58, chỉ xếp thứ 14 nếu đặt ở Ngoại hạng Anh. 
Ngoài ra, Antony cũng được "thổi phồng" nhờ chơi cho CLB vượt trội về tài chính và lực lượng so với phần còn lại của giải vô địch Hà Lan.'''
```
![image](https://github.com/Narius2030/Vietnamese-Text-Classification-and-Clustering/assets/94912102/cb19553b-5e8a-4c5d-b717-f8c438da6a9e)

- Visualize the relationship among words

![image](https://github.com/Narius2030/Vietnamese-Text-Classification-and-Clustering/assets/94912102/e6a9263b-ddad-479c-a4ee-8dcd9d861180)

- Visualize the relationship among paragraphs

![image](https://github.com/Narius2030/Vietnamese-Text-Classification-and-Clustering/assets/94912102/fb77ecfe-f9b6-4747-aabe-6aca71750894)


