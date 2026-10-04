# One-off: adds the Content Blocker extension target to the Xcode project.
require "xcodeproj"
proj_path = "Safari Ad Blocker/Safari Ad Blocker.xcodeproj"
proj = Xcodeproj::Project.open(proj_path)
app = proj.targets.find { |t| t.name == "Safari Ad Blocker" }
name = "Safari Ad Blocker Content Blocker"
t = proj.new_target(:app_extension, name, :osx, "12.0")
group = proj.main_group.new_group(name, name)
swift = group.new_file("ContentBlockerRequestHandler.swift")
group.new_file("Info.plist")
json = group.new_file("blockerList.json")
t.add_file_references([swift])
t.resources_build_phase.add_file_reference(json)
t.build_configurations.each do |c|
  s = c.build_settings
  s["PRODUCT_BUNDLE_IDENTIFIER"] = "com.example.safariadblock.ContentBlocker"
  s["PRODUCT_NAME"] = "$(TARGET_NAME)"
  s["INFOPLIST_FILE"] = "#{name}/Info.plist"
  s["GENERATE_INFOPLIST_FILE"] = "YES"
  s["INFOPLIST_KEY_CFBundleDisplayName"] = name
  s["ENABLE_APP_SANDBOX"] = "YES"
  s["ENABLE_HARDENED_RUNTIME"] = "YES"
  s["CODE_SIGN_STYLE"] = "Automatic"
  s["CURRENT_PROJECT_VERSION"] = "1"
  s["MARKETING_VERSION"] = "1.0"
  s["SWIFT_VERSION"] = "5.0"
  s["SKIP_INSTALL"] = "YES"
  s["MACOSX_DEPLOYMENT_TARGET"] = "12.0"
  s["LD_RUNPATH_SEARCH_PATHS"] = ["$(inherited)", "@executable_path/../Frameworks", "@executable_path/../../../../Frameworks"]
end
t.frameworks_build_phase.clear
app.add_dependency(t)
embed = app.copy_files_build_phases.find { |p| p.name == "Embed Foundation Extensions" }
bf = embed.add_file_reference(t.product_reference, true)
bf.settings = { "ATTRIBUTES" => ["RemoveHeadersOnCopy"] }
proj.save

# xcodeproj doesn't know the newer dstSubfolder attribute and drops it; restore it.
pbx = File.join(proj_path, "project.pbxproj")
text = File.read(pbx)
text.sub!(/(name = "Embed Foundation Extensions";)/, "dstSubfolder = PlugIns;\n\t\t\t\\1")
File.write(pbx, text)
