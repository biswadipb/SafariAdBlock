import Foundation

/// Hands Safari the compiled-at-build-time filter list (EasyList converted by tools/update_blocklist.sh).
class ContentBlockerRequestHandler: NSObject, NSExtensionRequestHandling {
    func beginRequest(with context: NSExtensionContext) {
        guard let url = Bundle.main.url(forResource: "blockerList", withExtension: "json"),
              let attachment = NSItemProvider(contentsOf: url) else {
            context.completeRequest(returningItems: nil, completionHandler: nil)
            return
        }
        let item = NSExtensionItem()
        item.attachments = [attachment]
        context.completeRequest(returningItems: [item], completionHandler: nil)
    }
}
