//
//  RadioObject.swift
//  RadioPi
//
//  Created by Barry Shukla on 4/17/22.
//

import Foundation
import CoreBluetooth

class RadioObject: NSObject, ObservableObject {
    @Published var textMessage = "" {
        didSet {
            if state.submitted && textMessage.count > 0 {
                state.submitted = false
                let valueString = (textMessage as NSString).data(using: String.Encoding.utf8.rawValue)
                if let characteristic = radioCharacteristic {
                    devicePeripheral?.setNotifyValue(true, for: characteristic)
                    print("set notify to true, now writing value")
                    devicePeripheral?.writeValue(valueString!, for: characteristic, type: .withResponse)
                }
            }
        }
    }
    @Published var state: State = State()
    
    private var bluetoothManager: CBCentralManager!
    private var devicePeripheral: CBPeripheral?
    private var radioCharacteristic: CBCharacteristic?
    
    override init() {
        super.init()
        bluetoothManager = CBCentralManager(delegate: self,
                                            queue: nil)
    }
}

extension RadioObject: CBCentralManagerDelegate, CBPeripheralDelegate {
    private static let UserA_NAME = "UserA"
    private static let UserB_NAME = "UserB"
    private static let USER_A_SERVICE_UUID = "0020A7D3-D8A4-4FEA-8174-1736E808C066"
    private static let USER_B_SERVICE_UUID = "0030A7D3-D8A4-4FEA-8174-1736E808C066"
    private static let USER_CHARACTERISTIC_UUID = "0010A7D3-D8A4-4FEA-8174-1736E808C066"
    
    //private static let STATUS_UUID = "0010A7D3-D8A4-4FEA-8174-1736E808C066"
    //private static let RADIO_UUID = "0008A7D3-D8A4-4FEA-8174-1736E808C066"
    
    // when the central manager's state (iPhone) is updated
    // (bluetooth is on off or something else)
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if (central.state == .poweredOn) {
            print("state is powered on")
            let services = [CBUUID(string:RadioObject.USER_A_SERVICE_UUID), CBUUID(string:RadioObject.USER_B_SERVICE_UUID)]
            bluetoothManager.scanForPeripherals(withServices: services)
        }
        else if (central.state == .poweredOff) {
            print("state is powered off")
            bluetoothManager.stopScan()
        }
    }
    
    /* Discovered a peripheral while scanning*/
    func centralManager(_ central: CBCentralManager,
                            didDiscover peripheral: CBPeripheral,
                            advertisementData: [String : Any],
                        rssi RSSI: NSNumber) {
        bluetoothManager.stopScan()
        // peripheral has the same name as what we are scanning for
        if let name = peripheral.name {
            print("discovered a new peripheral. \(name)")
            if (self.state.found_device == false && name == RadioObject.UserA_NAME || name == RadioObject.UserB_NAME || name == "LAMPI b827eb974fee") {
                self.state.found_device = true
                print("PERIPHERAL \(name) HAS BEEN DISCOVERED")
                //let new_name: String = name
                //self.state.messages = "\nNew peripheral \(new_name) found!"
                
                // assign device peripheral and it's delegate
                devicePeripheral = peripheral
                devicePeripheral?.delegate = self
                
                // stop looking for other peripherals and connect to target peripheral
                bluetoothManager.stopScan()
                bluetoothManager.connect(peripheral)
            }
        }
    }
    // central manager has connected to peripheral, scan for services now
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        if let name = peripheral.name {
            self.state.currentUser = name
            peripheral.discoverServices([CBUUID(string:RadioObject.USER_A_SERVICE_UUID),CBUUID(string:RadioObject.USER_B_SERVICE_UUID)])
        }
    }
    
    // discovered a service in that peripheral
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        guard let services = peripheral.services else { return }
        // check the characteristics of each service
        for service in services {
            print("Discovered device service")
            peripheral.discoverCharacteristics(nil, for: service)
        }
    }
    
    // check the characteristics that have been given
    func peripheral(_ peripheral: CBPeripheral,
                    didDiscoverCharacteristicsFor service: CBService,
                    error: Error?) {
        guard let characteristics = service.characteristics else { return }
        
        for characteristic in characteristics {
            // if characteristic is the one we're looking for
            if characteristic.uuid == CBUUID(string: RadioObject.USER_CHARACTERISTIC_UUID) {
                
                print("Found characteristic with UUID: \(RadioObject.USER_CHARACTERISTIC_UUID)")
                radioCharacteristic = characteristic
                devicePeripheral?.readValue(for: characteristic)
                devicePeripheral?.setNotifyValue(true, for: characteristic)
            }
        }
    }
    
    // retrieve the characteristics
    func peripheral(_ peripheral: CBPeripheral,
                    didUpdateValueFor characteristic: CBCharacteristic,
                    error: Error?) {
        
        guard let data = characteristic.value else { print("missing updated value"); return }
        
        if characteristic.uuid == CBUUID(string: RadioObject.USER_CHARACTERISTIC_UUID) {
            radioCharacteristic = characteristic
            self.state.messages = String(data: data, encoding: String.Encoding.utf8) ?? self.state.messages
            print(self.state.messages)
        }
    }
    
    // disconected from peripheral
    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
        self.state.currentUser = "NOT CONNECTED"
        print("Disconnected from peripheral: \(peripheral)")
        let services = [CBUUID(string:RadioObject.USER_A_SERVICE_UUID),CBUUID(string:RadioObject.USER_B_SERVICE_UUID)]
        bluetoothManager.scanForPeripherals(withServices: services)
    }
}


extension RadioObject {
    struct State {
        var currentUser : String = "NOT CONNECTED"
        var messages : String = ""
        var submitted: Bool = false
        let limit: Int = 250
        var found_device = false
    }
}
