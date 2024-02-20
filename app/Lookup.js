const MS_PER_DAY = 1000 * 60 * 60 * 24;

function doLookup(e) {
  var item = e.parameter.item;
  if (!item) return doError(e, "No item set for lookup.");
  item = decodeURIComponent(item).toLowerCase();
  const list_title = e.parameter.list_title;
  if (!list_title) return doError(e, "No list_title set for lookup.");
  var delta = lookupDelta(item);
  if(delta !== null) {
    // delta found
    if (delta < 0) {
      return doSuccess("-"); // never due
    } else {
      var due = new Date(Date.now() + MS_PER_DAY * delta);
      return doSuccess(formatDate(due));
    }
  } else {
    // delta not found
    requestDelta(item, list_title); // send an email if this item hasn't already been requested
    return doSuccess("");
  }
}

function doSet(e) {
  var item = e.parameter.item;
  if (!item) return doError(e, "No item set for set.");
  item = decodeURIComponent(item).toLowerCase();
  const delta = e.parameter.delta;
  if (!delta) return doError(e, "No delta set for set.");
  var cache = getCache();
  cache[item] = delta;
  setCache(cache);
  var requests = getRequests();
  requests = requests.filter((r) => r != item);
  setRequests(requests);
  if (delta == 1) {
    return doSuccess("'" + item + "' will be due in 1 day.");
  } else if (delta >= 0) {
    return doSuccess("'" + item + "' will be due in " + delta + " days.");
  } else {
    return doSuccess("'" + item + "' will never be due.");
  }
}

function lookupDelta(item) {
  var cache = getCache();
  for(const regex in cache) {
    if (item.match(regex)) {
      return cache[regex];
    }
  }
  return null;
}

function requestDelta(item, list_title) {
  var requests = getRequests();
  if (requests.includes(item)) return; // don't ask again
  requests.push(item);
  sendRequestEmail(requests, list_title);
  setRequests(requests);
}

function sendRequestEmail(requests, list_title) {
  var subject = list_title + " needs deadlines";
  var html = "<p>How long until these items are due?</p>";
  html += "<table border=1 style='border-collapse: collapse;'>";
  var app_url = ScriptApp.getService().getUrl();
  for (const item of requests) {
    var item_url = app_url + "?item=" + encodeURIComponent("^" + item + "$");
    html += "<tr>";
    html += "<td>" + item + "</td>";
    html += "<td><a href='" + item_url + "&action=set&delta=1'>Tomorrow</a></td>";
    html += "<td><a href='" + item_url + "&action=set&delta=7'>Next week</a></td>";
    html += "<td><a href='" + item_url + "&action=set&delta=14'>2 weeks</a></td>";
    html += "<td><a href='" + item_url + "&action=set&delta=30'>Next month</a></td>";
    html += "<td><a href='" + item_url + "'>Custom</a></td>";
    html += "</tr>";
  }
  html += "</table>";
  var thread_id = getRequestEmailThreadId();
  var thread = null;
  if (thread_id) thread = GmailApp.getThreadById(thread_id);
  if (thread) {
    for (const msg of thread.getMessages()) {
      msg.markRead();
    }
    thread.reply("", { htmlBody: html });
  } else {
    GmailApp.sendEmail(EMAIL_ADDRESS, subject, "", { htmlBody: html });
    var draft = GmailApp.createDraft(EMAIL_ADDRESS, subject, "", { htmlBody: html });
    var msg = draft.send();
    var thread = msg.getThread();
    setRequestEmailThreadId(thread.getId());
  }
}

function formatDate(d) {
  return Utilities.formatDate(d, Session.getScriptTimeZone(), "yyyy-MM-dd");
}