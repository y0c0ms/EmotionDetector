import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    input_json = {"raw_document": {"text": text_to_analyze}}
    
    try:
        response = requests.post(url, headers=headers, json=input_json)
        response.raise_for_status()
        
        # Parse the JSON response
        response_data = response.json()
        
        # Extract emotions from the response structure
        if 'emotionPredictions' in response_data:
            emotion_data = response_data['emotionPredictions'][0]['emotion']
        elif 'emotion_predictions' in response_data:
            emotion_data = response_data['emotion_predictions'][0]['emotion']
        else:
            emotion_data = response_data
        
        # Extract the required emotions
        emotions = {
            'anger': emotion_data.get('anger', 0.0),
            'disgust': emotion_data.get('disgust', 0.0),
            'fear': emotion_data.get('fear', 0.0),
            'joy': emotion_data.get('joy', 0.0),
            'sadness': emotion_data.get('sadness', 0.0)
        }
        
        # Find the dominant emotion
        dominant_emotion = max(emotions, key=emotions.get)
        emotions['dominant_emotion'] = dominant_emotion
        
        return emotions
        
    except:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }