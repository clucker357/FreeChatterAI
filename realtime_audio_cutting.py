import wave

import numpy as np
import pyaudio


def recognize_rec():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    PATH = 'tmp.wav'
    # 閾値。これを超えると録音を開始する。
    threshold = 0.15
    # サンプリングレート、マイク性能に依存
    RATE = 16000
    # 録音時間の上限
    RECORD_SECONDS = 1000000000 # second
    # pyaudio
    p = pyaudio.PyAudio()
    # マイクからデータ取得
    stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,input = True, frames_per_buffer = CHUNK)

    all = []
    A = int(RATE) / int(CHUNK) * int(RECORD_SECONDS)

    print("RATE = " + str(RATE))
    print("chunk = " + str(CHUNK))
    print("RECORD_SECONDS = " + str(RECORD_SECONDS))
    print("RATE / chunk * RECORD_SECONDS = " + str(A))
    print("")
    while True:
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype="int16") / 32768.0
        # まずサンプルを取る！
        xmax = x.max()
        # 録音中断までの時間
        STOP_SECONDS = 5 # second
        B = int(RATE / CHUNK * STOP_SECONDS)
        if xmax > threshold:
            n = 0 # 連続して閾値を下回った回数を記録するための変数
            print(B)

            for i in range(0, int(A)): # ←抜けたいfor構文！
                print(n)
                data = stream.read(CHUNK)
                all.append(data)

                x = np.frombuffer(data, dtype="int16") / 32768.0
                xmax = x.max()
                if xmax <= threshold:
                    n += 1
                else:
                    n = 0
                if n == B:
                    break
            data = b''.join(all)

            out = wave.open(PATH,'w')
            out.setnchannels(1) # mono
            out.setsampwidth(2) # 16bits
            out.setframerate(RATE)
            out.writeframes(data)
            out.close()
            break

    stream.close()
    p.terminate()


if __name__ == '__main__':
	print(recognize_rec())
