function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000);
  try {
    var sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    var p = e.parameter;
    sh.appendRow([new Date(), p.name || '', p['attend-j'] || '', p['attend-r'] || '', p.guests || '', p.page || '', p.lang || '', p['link-name'] || '']);
    return ContentService.createTextOutput('{"ok":true}').setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}
