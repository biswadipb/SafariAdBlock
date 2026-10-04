import Foundation
import WebKit

// Usage: swift validate.swift blockerList.json
let path = CommandLine.arguments[1]
let json = try! String(contentsOfFile: path, encoding: .utf8)
DispatchQueue.main.async {
    WKContentRuleListStore.default().compileContentRuleList(forIdentifier: "validate", encodedContentRuleList: json) { list, error in
        if let error = error {
            print("INVALID: \(error)")
            exit(1)
        }
        print("OK: WebKit compiled the rule list")
        exit(0)
    }
}
RunLoop.main.run()
