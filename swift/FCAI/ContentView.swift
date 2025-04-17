import Speech
import SwiftUI

struct ContentView: View {
    @ObservedObject var recorder: Recorder // Receive the recorder instance
    
    var body: some View {
        VStack {
            Text(recorder.recognizedText).padding()
            
            Button(action: {
                if recorder.isRecording {
                    recorder.stopRecording() // Call stopRecording on the recorder
                } else {
                    recorder.startRecording() // Call startRecording on the recorder
                }
            }) {
                Text(recorder.isRecording ? "Stop Recording" : "Start Recording")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
        }
        .padding()
    }
}
