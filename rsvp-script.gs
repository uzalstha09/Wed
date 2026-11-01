// Paste this into Extensions > Apps Script of your RSVP Google Sheet, then Deploy > New deployment > Web app
// Execute as: Me   |   Who has access: Anyone
function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName('RSVP') || ss.insertSheet('RSVP');
    if (sh.getLastRow() === 0) {
      sh.appendRow(['Time', 'Name', 'Wedding', 'Reception', 'Guests', 'Invitation', 'Language', 'Name in link']);
    }
    var p = e.parameter;
    sh.appendRow([new Date(), p.name || '', p['attend-j'] || '', p['attend-r'] || '', p.guests || '', p.page || '', p.lang || '', p['link-name'] || '']);
    return ContentService.createTextOutput('{"ok":true}').setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}
