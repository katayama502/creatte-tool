//! Windows only: embed the app icon and version info (VERSIONINFO) into `creatte-tool.exe`.
//!
//! On every other target this does nothing. A missing resource compiler is a warning, so a
//! cross-compile from macOS or Linux still links, unless `CREATTE_TOOL_REQUIRE_WINRES=1` (set
//! by the release packaging) turns it into an error.

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=../../assets/app-icon/creatte-tool.ico");
    println!("cargo:rerun-if-env-changed=CREATTE_TOOL_REQUIRE_WINRES");
    if std::env::var("CARGO_CFG_TARGET_OS").as_deref() != Ok("windows") {
        return;
    }
    let mut res = winresource::WindowsResource::new();
    res.set_icon("../../assets/app-icon/creatte-tool.ico")
        .set("ProductName", "Creatte Tool")
        .set("FileDescription", "Creatte Tool")
        .set("CompanyName", "Creatte")
        .set("LegalCopyright", "Copyright (c) the Creatte Tool authors. MIT OR Apache-2.0.")
        .set("OriginalFilename", "creatte-tool.exe")
        .set("InternalName", "creatte-tool");
    if let Err(e) = res.compile() {
        if std::env::var_os("CREATTE_TOOL_REQUIRE_WINRES").is_some() {
            println!("cargo:warning=embedding Windows resources failed: {e}");
            std::process::exit(1);
        }
        println!("cargo:warning=creatte-tool.exe built without icon/version resources: {e}");
    }
}
