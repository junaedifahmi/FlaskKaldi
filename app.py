from flask import Flask, Response, render_template
import os
from record_sound import RecordingVoice
import json
import timeit

app = Flask(__name__)


silent = False
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/decode')
def decode():
    def process():
        while not silent:
            record()
            data = json.dumps(
                {
                    'value': get_decode(),
                 }
            )
            yield f"data:{data}\n\n"
            # time.sleep()

    return Response(process(), mimetype='text/event-stream')


def record():
    r = RecordingVoice()
    return r.record()


def get_decode():
    model = '/media/juunnn/EXOLyxion1/Intership/FlaskKaldi'
    command = "~/kaldi/src/onlinebin/online-wav-gmm-decode-faster " \
              "--rt-min=0.3 --rt-max=0.5 --max-active=4000 --beam=12.0 --acoustic-scale=0.0769 " \
              "scp:./model/wav1.scp ./model/final.mdl ./model/HCLG.fst ./model/words.txt " \
              "'1:2:3:4:5' ark,t:./model/trans.txt ark,t:./model/ali.txt"
    dec = os.popen(command)
    return dec.read()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)



