"""docx'i LibreOffice ile açar, içindekiler dahil tüm dizinleri günceller ve PDF'e aktarır."""
import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue

src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])


def pv(n, v):
    p = PropertyValue()
    p.Name, p.Value = n, v
    return p


proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore",
                         "--accept=socket,host=127.0.0.1,port=2002;urp;"])
ctx = None
local = uno.getComponentContext()
resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
for _ in range(60):
    try:
        ctx = resolver.resolve("uno:socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext")
        break
    except Exception:
        time.sleep(1)
smgr = ctx.ServiceManager
desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(src), "_blank", 0, (pv("Hidden", True),))
for _ in range(2):  # iki tur: sayfa numaraları içindekiler eklendikten sonra oturur
    idx = doc.getDocumentIndexes()
    for i in range(idx.getCount()):
        idx.getByIndex(i).update()
    doc.refresh()
fields = doc.getTextFields()
fields.refresh()
pages = doc.getCurrentController().getPropertyValue("PageCount")
doc.storeToURL(uno.systemPathToFileUrl(out), (
    pv("FilterName", "writer_pdf_Export"),
    pv("FilterData", uno.Any("[]com.sun.star.beans.PropertyValue", tuple([
        pv("ExportBookmarks", True), pv("EmbedStandardFonts", True), pv("UseTaggedPDF", True)]))),
))
doc.close(True)
try:
    desktop.terminate()
except Exception:
    pass
proc.wait(timeout=60)
print("pages", pages, out)
