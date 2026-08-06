from flask import Flask, render_template, request, jsonify
import os
import werkzeug.utils
from insta_uploader import InstaUploader

app = Flask(__name__)

# 업로드 폴더 생성
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 환경 변수 또는 기본값
ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "27646020745040681")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAFlkZA0ZA4cGpiOWYyZAlpBOWJEY0wzS1gyWE54N1RiNnlNQlhhdWg5RktFS1k5bGI3M1YwbXh2ZAFJGa2tfQk1ma3RqVTZAYOWRjVDlSd01pZAEdTUC1ldzdOV19tUTBxOVY4UU9zNmFQdDB3")

uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN)

from calendar_manager import CalendarManager

calendar_mgr = CalendarManager()

@app.route('/')
def index():
    return render_template('index.html', account_id=ACCOUNT_ID)

@app.route('/api/calendar', methods=['GET'])
def get_calendar():
    try:
        posts = calendar_mgr.get_all_posts()
        return jsonify({'success': True, 'posts': posts})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def handle_upload():
    try:
        post_type = request.form.get('post_type', 'image')
        caption = request.form.get('caption', '')
        
        # 1. 단일 이미지
        if post_type == 'image':
            image_url = request.form.get('media_url')
            file = request.files.get('file')
            
            if file and file.filename != '':
                filename = werkzeug.utils.secure_filename(file.filename)
                saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(saved_path)
                image_target = saved_path
            elif image_url:
                image_target = image_url
            else:
                return jsonify({'success': False, 'message': '이미지 URL 또는 파일을 선택해주세요.'}), 400

            result = uploader.upload_image(image_target, caption)
            if 'error' in result:
                return jsonify({'success': False, 'error': result['error']})
            return jsonify({'success': True, 'result': result})

        # 2. 릴스 (동영상)
        elif post_type == 'reels':
            video_url = request.form.get('media_url')
            file = request.files.get('file')
            
            if file and file.filename != '':
                filename = werkzeug.utils.secure_filename(file.filename)
                saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(saved_path)
                video_target = saved_path
            elif video_url:
                video_target = video_url
            else:
                return jsonify({'success': False, 'message': '동영상 URL 또는 파일을 선택해주세요.'}), 400

            result = uploader.upload_reels(video_target, caption)
            if 'error' in result:
                return jsonify({'success': False, 'error': result['error']})
            return jsonify({'success': True, 'result': result})

        # 3. 캐러셀 (다중 이미지)
        elif post_type == 'carousel':
            files = request.files.getlist('files')
            urls_raw = request.form.get('media_urls', '')
            media_list = []
            
            # 파일 우선 처리
            if files and len(files) > 0 and files[0].filename != '':
                for f in files:
                    filename = werkzeug.utils.secure_filename(f.filename)
                    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    f.save(saved_path)
                    media_list.append(saved_path)
            elif urls_raw:
                media_list = [u.strip() for u in urls_raw.split(',') if u.strip()]

            if not media_list:
                return jsonify({'success': False, 'message': '캐러셀 업로드를 위한 최소 2개 이상의 미디어를 선택해주세요.'}), 400

            result = uploader.upload_carousel(media_list, caption)
            if 'error' in result:
                return jsonify({'success': False, 'error': result['error']})
            return jsonify({'success': True, 'result': result})

        else:
            return jsonify({'success': False, 'message': '지원하지 않는 포스트 타입입니다.'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 인스타그램 대시보드 서버 가동 중: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
