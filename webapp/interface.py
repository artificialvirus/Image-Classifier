app = Flask(__name__)

uncertain_images = ...  # Load your uncertain images here
uncertain_indices = ...  # Load your uncertain indices here
labeled_indices = set()

def get_next_uncertain_image():
    for idx, image in zip(uncertain_indices, uncertain_images):
        if idx not in labeled_indices:
            return image, idx
    return None, None  # No more images to label


def save_label(image_id, label):
    # Save the label to your database
    c.execute('''
              INSERT INTO image_labels (id, label)
              VALUES (?, ?)''', (image_id, label))
    conn.commit()


@app.route('/get_image', methods=['GET'])
def get_image():
    # Assume we have a function `get_next_uncertain_image()` to get the next image for labeling
    image, image_id = get_next_uncertain_image()
    return jsonify({'image': image.tolist(), 'image_id': image_id})

@app.route('/submit_label', methods=['POST'])
def submit_label():
    data = request.json
    image_id = data['image_id']
    label = data['label']
    save_label(image_id, label)  # Save label to the database
    return jsonify({'success': True})

if __name__ == '__main__':
    try:
        app.run(port=5000)
    finally:
        conn.close()  # Close the database connection

