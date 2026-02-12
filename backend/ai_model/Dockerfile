FROM tensorflow/serving

# Set the name of the model
ENV MODEL_NAME=acne_model

# Copy the model files to the specialized folder TensorFlow expects
# TensorFlow Serving expects the format: /models/[model_name]/[version_number]
COPY saved_model /models/acne_model
