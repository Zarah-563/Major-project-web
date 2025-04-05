from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np

# Define the function to predict cancer type based on skin disease
def predict_cancer_type(disease_label):
    cancer_types = {
        0: 'Melanocytic nevi',
        1: 'Melanoma',
        2: 'Benign keratosis-like lesions',
        3: 'Basal cell carcinoma',
        4: 'Actinic keratoses',
        5: 'Vascular lesions',
        6: 'Dermatofibroma'
    }

    # Mapping disease labels to cancer types
    if 'Melanoma' in disease_label:
        return 1  # Melanoma
    elif 'Basal Cell Carcinoma' in disease_label or 'Actinic Keratosis' in disease_label:
        return 3  # Basal cell carcinoma
    elif 'Seborrheic Keratoses' in disease_label:
        return 2  # Benign keratosis-like lesions
    elif 'Actinic Keratosis' in disease_label:
        return 4  # Actinic keratoses
    else:
        return None  # No cancer prediction

# Main function to predict skin disease and cancer type
def predict(path):
    # Load the trained model
    loaded_model = load_model("derma.h5")  # Use the path where you saved your trained model

    # Function to preprocess the image for prediction
    def preprocess_image(image_path):
        img = image.load_img(image_path, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize the image
        return img_array

    # Preprocess the input image
    processed_image = preprocess_image(path)

    # Make predictions
    predictions = loaded_model.predict(processed_image)

    # Class labels for skin diseases
    class_labels = [
        'Acne and Rosacea Photos', 
        'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions',
        'Atopic Dermatitis Photos',
        'Bullous Disease Photos',
        'Cellulitis Impetigo and other Bacterial Infections',
        'Eczema Photos',
        'Exanthems and Drug Eruptions',
        'Hair Loss Photos Alopecia and other Hair Diseases',
        'Herpes HPV and other STDs Photos',
        'Invalid Image',
        'Light Diseases and Disorders of Pigmentation',
        'Lupus and other Connective Tissue diseases',
        'Melanoma Skin Cancer Nevi and Moles',
        'Nail Fungus and other Nail Disease',
        'Normal Skin',
        'Poison Ivy Photos and other Contact Dermatitis',
        'Psoriasis pictures Lichen Dermatosis and related diseases',
        'Scabies Lyme Disease and other Infestations and Bites',
        'Seborrheic Keratoses and other Benign Tumors',
        'Systemic Disease',
        'Tinea Ringworm Candidiasis and other Fungal Infections',
        'Urticaria Hives',
        'Vascular Tumors',
        'Vasculitis Photos',
        'Viral infections',
        'Warts Molluscum'
    ]
    
    # Get the predicted class index
    predicted_class_index = np.argmax(predictions)
    predicted_class_label = class_labels[predicted_class_index]

    # Now predict the cancer type based on the predicted skin disease
    cancer_prediction = predict_cancer_type(predicted_class_label)

    # If cancer type is predicted, map it to the cancer type label
    if cancer_prediction is not None:
        cancer_types = {
            0: 'Melanocytic nevi',
            1: 'Melanoma',
            2: 'Benign keratosis-like lesions',
            3: 'Basal cell carcinoma',
            4: 'Actinic keratoses',
            5: 'Vascular lesions',
            6: 'Dermatofibroma'
        }
        cancer_label = cancer_types[cancer_prediction]
        print(f"Predicted Cancer Type: {cancer_label}")
    else:
        print("No Cancer Prediction.")

    print("Predicted Skin Disease Class:", predicted_class_label)

    return predicted_class_label, cancer_label if cancer_prediction is not None else None
