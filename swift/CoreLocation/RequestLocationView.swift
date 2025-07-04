//
//  RequestLocationView.swift
//  FreeChaterAI
//
//  Created by Toipot on 2024/02/21.
//

import SwiftUI

struct RequestLocationView: View {
    @EnvironmentObject var locationViewModel: LocationViewModel
    
    var body: some View {
        Button(action: {
            locationViewModel.requestPermission()
        }) {
            Text("位置情報の使用を許可する")
        }
    }
}

struct RequestLocationView_Previews: PreviewProvider {
    static var previews: some View {
        RequestLocationView().environmentObject(LocationViewModel())
    }
}
