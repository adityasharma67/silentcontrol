import socket
import time
import pyautogui
import cv2
import numpy as np
from flask import Flask, render_template_string, Response, request, jsonify
from pynput.mouse import Controller as MouseController

app = Flask(__name__)
mouse = MouseController()

def capture_frame():
    try:
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    except OSError as error:
        print(
            f"Screen capture unavailable: {error}. "
            "Keep the Windows desktop unlocked and connected. Retrying..."
        )
        frame = np.zeros((480, 800, 3), dtype=np.uint8)
        cv2.putText(
            frame,
            "Screen capture unavailable",
            (120, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 180, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "Unlock or reconnect the Windows desktop",
            (95, 270),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        return frame

def generate_frames():
    while True:
        frame = capture_frame()
        
        # Aggiungi il cursore del mouse al frame
        try:
            x, y = mouse.position
            if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        except OSError:
            pass
        
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            time.sleep(0.5)
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.05)

@app.route('/control', methods=['POST'])
def control():
    command = request.get_json(silent=True) or {}
    action = command.get('action')

    if action == 'move':
        screen_width, screen_height = pyautogui.size()
        x = max(0, min(screen_width - 1, int(float(command.get('x', 0)) * screen_width)))
        y = max(0, min(screen_height - 1, int(float(command.get('y', 0)) * screen_height)))
        pyautogui.moveTo(x, y, duration=0.05)
    elif action == 'click':
        pyautogui.click(button=command.get('button', 'left'))
    elif action == 'scroll':
        pyautogui.scroll(int(command.get('amount', 0)))
    elif action == 'key':
        pyautogui.press(command.get('key', ''))
    elif action == 'text':
        pyautogui.write(str(command.get('text', '')), interval=0.01)
    else:
        return jsonify(error='Unknown control action'), 400

    return jsonify(ok=True)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Screen Streaming</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #1f1f1f;
                font-family: 'Courier New', Courier, monospace;
            }
    
            .container {
                max-width: 1300px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                overflow: hidden;
            }
    
            .header {
                padding: 20px;
                background-color: #333;
                color: #fff;
                text-align: center;
            }
    
            .header h1 {
                margin: 0;
                font-size: 24px;
                font-family: 'Arial', sans-serif;
            }
    
            .video-container {
                position: relative;
                overflow: hidden;
            }
    
            .video-container img {
                width: 100%;
                height: auto;
                display: block;
                touch-action: none;
            }

            .controls {
                display: flex;
                gap: 8px;
                padding: 10px;
                background-color: #333;
            }

            .controls input {
                flex: 1;
                min-width: 0;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
    
            .fullscreen-button {
                position: absolute;
                top: 10px;
                right: 10px;
                background-color: #333;
                color: #fff;
                border: none;
                padding: 10px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Arial', sans-serif;
            }
        </style>
        <script>
            function sendControl(command) {
                fetch('/control', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(command)
                });
            }

            document.addEventListener('DOMContentLoaded', () => {
                const screen = document.querySelector('.video-container img');
                let dragging = false;

                function movePointer(event) {
                    const bounds = screen.getBoundingClientRect();
                    sendControl({
                        action: 'move',
                        x: (event.clientX - bounds.left) / bounds.width,
                        y: (event.clientY - bounds.top) / bounds.height
                    });
                }

                screen.addEventListener('pointerdown', event => {
                    dragging = true;
                    screen.setPointerCapture(event.pointerId);
                    movePointer(event);
                });
                screen.addEventListener('pointermove', event => {
                    if (dragging) movePointer(event);
                });
                screen.addEventListener('pointerup', event => {
                    dragging = false;
                    sendControl({action: 'click', button: 'left'});
                });
                screen.addEventListener('contextmenu', event => {
                    event.preventDefault();
                    sendControl({action: 'click', button: 'right'});
                });
                screen.addEventListener('wheel', event => {
                    event.preventDefault();
                    sendControl({action: 'scroll', amount: event.deltaY < 0 ? 3 : -3});
                }, {passive: false});

                document.querySelector('#send-text').addEventListener('click', () => {
                    const input = document.querySelector('#text-input');
                    if (input.value) {
                        sendControl({action: 'text', text: input.value});
                        input.value = '';
                    }
                });

                document.addEventListener('keydown', event => {
                    if (event.target.id === 'text-input') return;
                    event.preventDefault();
                    sendControl({action: 'key', key: event.key});
                });
            });

            function toggleScreenShareFullscreen() {
                const elem = document.querySelector('.video-container img');
    
                if (elem.requestFullscreen) {
                    elem.requestFullscreen();
                } else if (elem.mozRequestFullScreen) {
                    elem.mozRequestFullScreen();
                } else if (elem.webkitRequestFullscreen) {
                    elem.webkitRequestFullscreen();
                } else if (elem.msRequestFullscreen) {
                    elem.msRequestFullscreen();
                }
            }
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Screen Streaming</h1>
            </div>
            <div class="video-container">
                <img src="{{ url_for('video_feed') }}" alt="Screen Stream">
            </div>
            <div class="controls">
                <input id="text-input" type="text" placeholder="Type text on PC">
                <button id="send-text" type="button">Send</button>
            </div>
            <button class="fullscreen-button" onclick="toggleScreenShareFullscreen()">Fullscreen Condivisione Schermo</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Silent Screenshare started. Press Ctrl+C to stop it manually.")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
