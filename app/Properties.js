const CACHE_PROPERTY = "cache";
const REQUESTS_PROPERTY = "requests";

function getCache() {
  var p = PropertiesService.getScriptProperties();
  var cache = p.getProperty(CACHE_PROPERTY);
  if (cache) {
    return JSON.parse(cache);
  } else {
    return {}; // maps regex to "days until due" (0 means today, -ve means never due)
  }
}

function setCache(cache) {
  var p = PropertiesService.getScriptProperties();
  p.setProperty(CACHE_PROPERTY, JSON.stringify(cache));
}

function getRequests() {
  var p = PropertiesService.getScriptProperties();
  var requests = p.getProperty(REQUESTS_PROPERTY);
  if (requests) {
    return JSON.parse(requests);
  } else {
    return []; // lists of outstanding requests (exact strings, not regex)
  }
}

function setRequests(requests) {
  var p = PropertiesService.getScriptProperties();
  p.setProperty(REQUESTS_PROPERTY, JSON.stringify(requests));
}