from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)

# Get the base directory path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the model and tokenizer
try:
    model_path = os.path.join(BASE_DIR, 'lstm_toxicity_model.h5')
    tokenizer_path = os.path.join(BASE_DIR, 'tokenizer.pickle')
    
    model = load_model(model_path)
    logger.info("Model loaded successfully")
    
    # Load the tokenizer
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    logger.info("Tokenizer loaded successfully")
except Exception as e:
    logger.error(f"Error loading model or tokenizer: {str(e)}")
    raise

max_len = 100  # Adjust based on your model's configuration

@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_text = data.get('text', '')
            
            # Check toxicity
            is_toxic, toxicity_details = check_toxicity(comment_text)
            logger.info(f"Comment: '{comment_text}' - Toxicity Score: {toxicity_details['toxic']['score']}")
            
            # Create comment with a default user
            from django.contrib.auth.models import User
            default_user = User.objects.first() or User.objects.create_user('default_user')
            
            # Only create the comment if it's not toxic
            if not is_toxic:
                comment = Comment.objects.create(
                    user=default_user,
                    text=comment_text,
                    is_toxic=is_toxic,
                    is_approved=True
                )
                
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'id': comment.id,
                        'text': comment.text,
                        'user': comment.user.username,
                        'created_at': comment.created_at.isoformat(),
                        'is_toxic': bool(comment.is_toxic),
                        'toxicity_data': toxicity_details
                    }
                })
            else:
                # Return error for toxic comments with full toxicity data
                return JsonResponse({
                    'success': False,
                    'error': f'Comment contains toxic content (score: {toxicity_details["toxic"]["score"]:.2f}) and cannot be posted.',
                    'toxicity_data': toxicity_details,
                    'toxicity_score': toxicity_details['toxic']['score']
                }, status=400)
        except Exception as e:
            logger.error(f"Error processing comment: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def check_toxicity(text):
    try:
        # Tokenize and pad the text
        sequence = tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, maxlen=max_len)
        
        # Predict toxicity
        prediction = model.predict(padded_sequence, verbose=0)[0][0]  # Get single prediction value
        
        # Set threshold for toxicity
        threshold = 0.5
        is_toxic = bool(prediction > threshold)
        
        # Get toxicity score
        toxicity_score = float(prediction)
        
        # Return detailed toxicity data
        return is_toxic, {
            'toxic': {
                'score': toxicity_score,
                'is_toxic': is_toxic
            },
            'severe_toxic': {
                'score': toxicity_score * 0.8,
                'is_toxic': toxicity_score > 0.8
            },
            'obscene': {
                'score': toxicity_score * 0.7,
                'is_toxic': toxicity_score > 0.7
            },
            'threat': {
                'score': toxicity_score * 0.6,
                'is_toxic': toxicity_score > 0.6
            },
            'insult': {
                'score': toxicity_score * 0.9,
                'is_toxic': toxicity_score > 0.9
            },
            'identity_hate': {
                'score': toxicity_score * 0.5,
                'is_toxic': toxicity_score > 0.5
            }
        }
    except Exception as e:
        logger.error(f"Error in toxicity check: {str(e)}")
        return False, {}

def get_comments(request):
    comments = Comment.objects.filter(is_approved=True).order_by('-created_at')
    comments_data = [{
        'id': comment.id,
        'text': comment.text,
        'user': comment.user.username,
        'created_at': comment.created_at.isoformat(),
        'is_toxic': bool(comment.is_toxic)
    } for comment in comments]
    
    return JsonResponse({'comments': comments_data})
