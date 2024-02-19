function doAdmin(e) {
  var initial_item = e.parameter.item;
  if (initial_item) initial_item = decodeURIComponent(initial_item).toLowerCase();
  const initial_delta = e.parameter.delta;
  var ui = HtmlService.createTemplateFromFile("UI");
  ui.initial_item = initial_item;
  ui.initial_delta = initial_delta;
  ui.cache = getCache();
  return ui.evaluate().setTitle("GKeepListDeadlines").addMetaTag("viewport", "width=200, initial-scale=1.7")
}

// client call
function addDelta(item, delta) {
  if(!item) throw Error("Item cannot be blank.");
  if(!delta) throw Error("Delta cannot be blank.");
  var cache = getCache();
  cache[item] = delta;
  setCache(cache);
  var requests = getRequests();
  requests = requests.filter((r) => !r.match(item));
  setRequests(requests);
  return cache;
}

// client call
function removeDelta(item) {
  if(!item) throw Error("Item cannot be blank.");
  var cache = getCache();
  delete cache[item];
  setCache(cache);
  return cache;
}

// client call
function listDeltas() {
  return getCache();
}