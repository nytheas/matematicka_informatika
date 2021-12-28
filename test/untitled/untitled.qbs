import qbs.FileInfo

DynamicLibrary {
    Depends { name: "Qt.core" }

    cpp.cxxLanguageVersion: "c++11"
    cpp.defines: [
        "UNTITLED_LIBRARY",

        // You can make your code fail to compile if it uses deprecated APIs.
        // In order to do so, uncomment the following line.
        //"QT_DISABLE_DEPRECATED_BEFORE=0x060000" // disables all the APIs deprecated before Qt 6.0.0
    ]

    files: [
        "untitled.cpp",

    ]

    // Default rules for deployment.
    qbs.installPrefix: ""
    Properties {
        condition: qbs.targetOS.contains("unix")
        install: true
        installDir: "/usr/lib"
    }
}
