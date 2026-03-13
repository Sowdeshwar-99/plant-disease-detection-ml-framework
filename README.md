# Advanced Machine Learning Framework for Efficient Plant Disease Prediction

This repository contains the implementation and supporting materials for the research paper:

**Advanced Machine Learning Framework for Efficient Plant Disease Prediction**

Authors:
- Aswath M
- Sowdeshwar S
- Saravanan M (Ericsson Research)
- Satheesh K Perepu (Ericsson Research)

Published research:
https://www.researchgate.net/publication/373375522_Advanced_Machine_Learning_Framework_for_Efficient_Plant_Disease_Prediction

---

## Overview

Plant diseases significantly affect agricultural productivity worldwide.  
This project proposes an integrated machine learning framework that combines:

• Deep Learning for plant disease detection  
• Natural Language Processing for analyzing community solutions  
• Concept Drift detection to adapt recommendations across seasons  

The system is built on top of a Twitter-based communication platform where farmers can post plant disease images and receive ranked solutions from the community.

---

## System Architecture

The proposed framework consists of three major components:

1️. Image-based Disease Detection  
  A CNN model (Inception-ResNet-v2) trained on the PlantVillage dataset to classify plant diseases.

2️. NLP-based Solution Ranking  
  User solutions extracted from Twitter replies are processed using NLP techniques and compared using Word Mover’s Distance (WMD).

3️. Concept Drift Detection  
  Seasonal variations are handled using concept drift detection to dynamically switch prediction models.

---

## Dataset

PlantVillage dataset:
https://plantvillage.psu.edu/

Dataset contains images of healthy and diseased plant leaves across multiple crop types.

---

## Technologies Used

Python  
TensorFlow / Keras  
Scikit-Learn  
NLTK  
Gensim  
Tweepy  
Pandas  

---

## Future Improvements

• Real-time mobile application for farmers  
• Integration with IoT agricultural sensors  
• Deployment using cloud-based inference services  
• Support for multiple social media platforms

---
