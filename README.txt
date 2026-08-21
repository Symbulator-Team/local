Symbulator 9 — offline version
================================

This is a self-contained copy of Symbulator 9. Everything runs inside
your own browser -- there is no server, and once it has loaded, it
keeps working with no internet connection at all.

RUNNING FOR THE FIRST TIME
----------------------------

Browsers won't run this correctly if you just double-click index.html
(they block some of what it needs when opened as a plain file).
Extract the contents of this file if you haven't already, then use one
of the two options below to run it for the first time. This is done
according to your operating system:

Option A -- double-click to start (easiest):

  * Windows:  double-click  start.bat
  * macOS:    double-click  start.command
              (macOS may warn that the file is from an unidentified
              developer the first time. Right-click it, choose "Open",
              then confirm. After that it opens normally.)
  * Linux:    open a terminal in this folder and run  sh start.sh

  This will start a small local web server and open Symbulator 9 in
  your browser automatically. Leave that window open while you use
  the software.

Option B -- do it by hand:

  1. Open a terminal (or Command Prompt) in this folder.
  2. Run:   python3 -m http.server 8000
            (on Windows, try  python  instead of  python3  if that
            command isn't found)
  3. Open   http://localhost:8000/   in your browser.

INSTALL AS AN APP
-------------------

Once Symbulator 9 is open in your browser, you can install it as an
app. On a computer, look for an "Install" icon in the address bar; if
you don't see one, open the browser's menu and choose "Install
Symbulator 9". Follow the prompt, and it opens like any other app from
then on, with no internet needed and no more running start scripts.
Once you've finished this first session, you can close that window --
the installed app runs on its own from now on.

Installing on a phone or tablet is a different route. This ZIP needs
Python on a computer, so it is not a phone option at all. To install
on a phone, visit https://install.symbulator.com instead and install
from there. There is no install icon in the address bar on mobile --
that is a desktop-only feature. In Chrome on Android, open the browser
menu (the three dots, top right) and choose the install entry, which
reads "Install app", "Install and create shortcut" or "Add to Home
Screen" depending on the version. On iPhone and iPad, use Safari's
Share button and choose "Add to Home Screen". If you don't see the
entry yet, tap the page once and give it a few seconds -- browsers
wait until you have actually used a page before offering to install it.

Once you've installed it as an app, you can delete the ZIP and the
unzipped folder -- the installed app now runs entirely from your
browser's own storage and won't need them again. It's still worth
keeping the ZIP somewhere safe, though, in case you ever need to
reinstall (for example, if you clear your browser's site data, switch
browsers, or move to a different computer).

UPDATING TO A NEWER VERSION
-----------------------------

If a newer version of Symbulator 9 comes out, download the new ZIP.
To install it cleanly, first remove the current app -- when
uninstalling, check "Remove this app's data from Chrome" -- then
repeat the install process above with the new ZIP. If you'd rather not
reinstall, you can instead try forcing a full reload: press
Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac) -- though a clean
reinstall is the more reliable fix.

REQUIREMENTS
-------------

This process requires Python 3 only, to run the one-time local server
above -- get it free from https://python.org if you don't already have
it. Nothing else needs installing: the maths engine itself (Python,
SymPy, and the symbulator package) is bundled in the vendor/ folder
and runs entirely inside your browser.

MORE INFORMATION
------------------

Symbulator 9: https://symbulator.com
Source code and licence (MIT): https://github.com/Symbulator
