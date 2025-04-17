import Foundation
import Speech
import AVFoundation



class Recorder: ObservableObject {
    @Published var isRecording = false
    @Published var recognizedText = ""
    @Published var synthesizer = AVSpeechSynthesizer()
    
    private let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja_JP"))
    private let audioEngine = AVAudioEngine()
    private let request = SFSpeechAudioBufferRecognitionRequest()
    private var NoSoundTime = 0.0
    private var waitTime = 0.0
    var recognitionTask: SFSpeechRecognitionTask?
    var lastRecognizedText = ""
    
    func requestSpeechAuthorization() {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            if authStatus == .authorized {
                print("Speech recognition authorized")
            } else {
                print("Speech recognition not authorized")
            }
        }
    }
    
    func startRecording() {
        isRecording = true
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.record, mode: .default, options: [])
            try audioSession.setMode(.default)
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            print("Audio session setup error: \(error)")
        }
        
        recognitionTask = recognizer?.recognitionTask(with: request) { [weak self] result, error in
            guard let self = self else { return }
            
            guard let result = result else {
                print("Recognition error: \(error.debugDescription)")
                return
            }
            
            print("recognitionTask")
            
            if result.bestTranscription.formattedString != self.lastRecognizedText {
                print("recognitionTask2")
                if(self.NoSoundTime <= 0.0){
                    print("recognitionTask3")
                    self.NoSoundTime = 0.0
                    self.DetectNoSound()
                }
                self.ResetTime()
                self.lastRecognizedText = result.bestTranscription.formattedString
            }
            if result.isFinal {
                self.recognizedText = result.bestTranscription.formattedString
                // recognizedTextをサーバに送信する
                
                // 録音が終了した直後に再び録音を開始する
                audioEngine.stop()
                request.endAudio()
                self.NoSoundTime = -99999.0
                self.waitTime = 0.0
                recognitionTask = nil
                self.stopRecording()
                self.send2Server(text: self.recognizedText)
                self.lastRecognizedText = ""
                self.recognitionTask = nil
                self.startRecording()
            }
        }
        
        let node = audioEngine.inputNode
        node.removeTap(onBus: 0)
        let recordingFormat = node.outputFormat(forBus: 0)
        if node.inputFormat(forBus: 0) != recordingFormat {
            node.removeTap(onBus: 0)
        }
        node.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { [weak self] buffer, _ in
            guard let self = self else { return }
            
            self.request.append(buffer)
        }
        
        audioEngine.prepare()
        
        do {
            try audioEngine.start()
        } catch {
            print("Audio engine start error: \(error)")
        }
        // Schedule a timer to stop recording if no speech is recognized after 3 seconds
    }
    
    func DetectNoSound(){
        if(NoSoundTime <= -1.0){
            return
        }
        print("DS")
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) { [weak self] in
            guard let self = self else { return }
            
                self.NoSoundTime += 1.0
                self.waitTime += 1.0
                print(self.NoSoundTime)
                print(self.waitTime)
                self.DetectNoSound()
        }
        if (self.NoSoundTime >= 5.0){
            self.NoSoundTime = -99999.0
            self.stopRecording()
            print("no speech")
        }
        if(self.waitTime >= 10.0){
            print("AIからのお話")
            self.send2Server(text: "N0001")
        }
        return
    }
    func ResetTime(){
        self.NoSoundTime = 0.0
    }
    
    func stopRecording() {
        isRecording = false
        audioEngine.stop()
        request.endAudio()
        return
    }
    
    func speak(text: String) {
        let utterance = AVSpeechUtterance(string: text)
        
        // 読み上げる言語を設定（日本語の場合は"ja-JP"）
        utterance.voice = AVSpeechSynthesisVoice(language: "ja-JP")
        utterance.rate = 0.53
        
        synthesizer.speak(utterance)
    }
    
    func send2Server(text: String){
        let url = URL(string: "http://127.0.0.1:8000/analyze/")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let requestBody: [String: String] = ["text": text]
        do {
                print("sended")
                request.httpBody = try JSONSerialization.data(withJSONObject: requestBody, options: [])
            } catch {
                print("Error serializing JSON: \(error)")
                return
            }
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error sending request: \(error)")
                    return
                }
                
                // サーバからの応答を処理する場合はここに追加
                if let httpResponse = response as? HTTPURLResponse {
                    print("Server response: \(httpResponse.statusCode)")
                }
                if let responseData = data, let responseText = String(data: responseData, encoding: .utf8) {
                        print("Server response text: \(responseText)")
                    DispatchQueue.main.async {
                        self.recognizedText = responseText.trimmingCharacters(in: .init(charactersIn: "\""))
                    }
//                    self.speak(text: responseText)
                }
            }
            
            task.resume()
        
    }
    
}
