//
//  ContentView.swift
//  StatusPi
//
//  Created by Gopal Shukla on 4/17/22.
//

import SwiftUI

struct ContentView: View {
    @ObservedObject var radioObj = RadioObject()
    var body: some View {
        GeometryReader { geo in
            VStack {
                HStack {
                Text("\(radioObj.state.currentUser)")
                    .bold()
                    .underline()
                    .foregroundColor(.black)
                    .lineLimit(3)
                    .multilineTextAlignment(.leading)
                }
                Text("\(radioObj.state.messages)")
                    .foregroundColor(.black)
                    .lineLimit(20)
                    .multilineTextAlignment(.leading)
                TextField("MESSAGE",
                          text: $radioObj.textMessage)
                    .textFieldStyle(.roundedBorder)
                    .frame(width:geo.size.width, height: geo.size.height*0.3)
                    .onSubmit {
                        guard radioObj.state.submitted == false && radioObj.textMessage.count > 0 else { return }
                        radioObj.state.submitted = true
                    }
            }
        }
        .background(Color.white)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
