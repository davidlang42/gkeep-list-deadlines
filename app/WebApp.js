const EMAIL_ADDRESS = Session.getEffectiveUser().getEmail();

function doGet(e) {
  const action = e.parameter.action;
  if(action == "lookup") {
    return doLookup(e);
  } else if (action == "email") {
    return doEmail(e);
  } else if (action == "set") {
    return doSet(e);
  } else if (Session.getActiveUser().getEmail() == EMAIL_ADDRESS) {
    return doAdmin(e);
  } else {
    return doError(e, "Invalid action: " + action);
  }
}

function doError(e, reason) {
  GmailApp.sendEmail(EMAIL_ADDRESS, "Error: GKeepListDeadlines", reason + "\n\n" + JSON.stringify(e))
  return ContentService.createTextOutput(reason);
}

function doSuccess(done) {
  return ContentService.createTextOutput(done);
}