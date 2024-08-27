"""
This module defines a Flask application for analyzing emotions in text.
It exposes an endpoint '/emotionDetector' that processes POST requests
with a JSON payload containing a text statement. The endpoint returns
the results of the emotion analysis and the dominant emotion.
"""

from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector  # Adjust this import based on your package structure

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_endpoint():
    """
    Analyze emotions in the provided text statement.

    The function receives a JSON payload with a text field, processes
    the text to detect emotions, and returns a formatted response with
    the emotion scores and the dominant emotion. If the text is invalid
    or missing, it returns an error message.

    Returns:
        Response: A JSON response containing either the emotion analysis
                  results or an error message.
    """
    data = request.get_json()  # Parse JSON body
    text_to_analyze = data.get('text', '')

    # Call the emotion_detector function
    result = emotion_detector(text_to_analyze)

    # Check if the result contains None values indicating an error
    if result.get('dominant_emotion') is None:
        return jsonify({'response': 'Invalid text! Please try again!'}), 400

    # Format the response as requested
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']}, "
        f"and 'sadness': {result['sadness']}. The dominant emotion is {result['dominant_emotion']}."
    )

    return jsonify({'response': formatted_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ensure this port is not blocked and is correct
