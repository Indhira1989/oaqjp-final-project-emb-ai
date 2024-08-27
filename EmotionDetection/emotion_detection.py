import requests
import json

def emotion_detector(text_to_analyze):
    # Check if the input text is blank
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    json_data = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.RequestException as e:
        # Handle exceptions such as network problems, invalid responses, etc.
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    try:
        response_json = response.json()
        # Extract emotions
        emotions = response_json.get('emotionPredictions', [])
        if emotions:
            emotion_data = emotions[0].get('emotion', {})
            # Extract emotion scores
            anger_score = emotion_data.get('anger', 0)
            disgust_score = emotion_data.get('disgust', 0)
            fear_score = emotion_data.get('fear', 0)
            joy_score = emotion_data.get('joy', 0)
            sadness_score = emotion_data.get('sadness', 0)
            
            # Find the dominant emotion
            dominant_emotion = max(emotion_data, key=emotion_data.get, default='unknown')

            # Format the output
            return {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score,
                'dominant_emotion': dominant_emotion
            }
    except (ValueError, KeyError) as e:
        # Handle cases where JSON parsing or key access fails
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Default return in case of unexpected issues
    return {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }
