import Speech
import SwiftUI

@main
struct FCAIApp: App {
    @StateObject var recorder = Recorder() // Use an ObservableObject to manage recording state and recognized text
    
    var body: some Scene {
        WindowGroup {
            ContentView(recorder: recorder) // Pass the recorder to ContentView
        }
    }
}
