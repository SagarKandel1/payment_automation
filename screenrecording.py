import os
import base64

def save_recording_to_documents(video_base64, filename="test_evidence.mp4"):
    """Save the screen recording to the user's Documents folder"""
    documents_path = os.path.expanduser("~/Documents")
    if not os.path.exists(documents_path):
        os.makedirs(documents_path)
    file_path = os.path.join(documents_path, filename)
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(video_base64))
    print(f"Screen Recording saved at: {file_path}")
