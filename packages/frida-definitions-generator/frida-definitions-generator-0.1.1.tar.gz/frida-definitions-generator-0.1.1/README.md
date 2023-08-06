Frida Definitions Generator
===========================

Generate TypeScript definitions for a given APK file or unpacked APK directory.

NOTICE: you will need to install the nightly version of LIEF until they release
a version with the Dalvik fields fix. The installation command will look
something like this:

    $ python3 -m pip install --extra-index-url https://lief-project.github.io/packages frida-definitions-generator

After you've installed the program you should have an executable named
`frida-definitions-generator` that you can run like this:

    $ frida-definitions-generator --type java /path/to/apk > app.d.ts

This will output all the classes from the APK as Frida TypeScript definitions
into the piped file. You can also pass a directory of the unzipped APK instead
of the APK itself.
