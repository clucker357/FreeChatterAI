//
//  ErrorView.swift
//  FreeChaterAI
//
//  Created by Toipot on 2024/02/21.
//

import SwiftUI

struct ErrorView: View {
    var errorText: String
    
    var body: some View {
        Text(errorText)
    }
}

struct ErrorView_Previews: PreviewProvider {
    static var previews: some View {
        ErrorView(errorText: "エラーメッセージ")
    }
}

