import subprocess
import cv2
rtmp_url = "rtmp://127.0.0.1:1935/stream/pupils_trace"


path = 0
cap = cv2.VideoCapture(path)
# gather video info to ffmpeg
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'H264')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

# command and params for ffmpeg
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmp_url]

# using subprocess and pipe to fetch frame data
p = subprocess.Popen(command, stdin=subprocess.PIPE)

while(True):
    ret, frame = cap.read() 

    if not ret:
        print("frame read failed")
        break

    # output the frame
    out.write(frame) 
        
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break

    # write to pipe
    p.stdin.write(frame.tobytes())

cap.release()

out.release() 

cv2.destroyAllWindows()