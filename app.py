from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load ads from a JSON file
def load_ads():
    with open('ads.json', 'r') as f:
        return json.load(f)

# Log impression to a file
def log_impression(ad_id, ip):
    with open('impressions.log', 'a') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp},{ad_id},{ip}\n")

# Serve an ad
@app.route('/ad', methods=['GET'])
def serve_ad():
    ads = load_ads()
    # Simple logic: pick first active ad (could be randomized later)
    for ad in ads:
        if ad['active']:
            log_impression(ad['id'], request.remote_addr)
            return jsonify({
                'id': ad['id'],
                'content': ad['content'],
                'link': ad['link']
            })
    return jsonify({'error': 'No active ads'}), 404

# Admin page to view/manage ads
@app.route('/admin', methods=['GET'])
def admin_page():
    ads = load_ads()
    return render_template('admin.html', ads=ads)

# Start the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)