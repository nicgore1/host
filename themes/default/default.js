// --- Specific Theme Functions -----------------------------------------------

function hostRedirect() {
  "use strict";
  // For DNS Usage
  // var redirect = "https://cthugha.thegate.network/";
  // location.replace(redirect);
}

function defaultHomepages() {
  "use strict";
  if (location.hostname === "www.playstation.com" || location.hostname === "manuals.playstation.net") {
    return true;
  }
  return;
}

function myAlert(type, message, wait) {
  "use strict";
  if (wait === undefined) {
    wait = 3000;
  }
  var alertID = "alert-" + uuid();
  var alertString = "<div class=\"alert alert-" + type + " alert-dismissible fade collapse\" id=\"" + alertID + "\" role=\"alert\">";
  alertString += message;
  alertString += "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">";
  alertString += "<span aria-hidden=\"true\">&times;</span>";
  alertString += "</button>";
  alertString += "</div>";
  $("#alertBox").append(alertString);
  $("#" + alertID).collapse("show");
  // # TODO: Calculate top
  // $("#alert-" + randomID).css("top", ($(".alert").length));
  sleep(wait).then(function() {
    $("#" + alertID).alert("close");
    // TODO: Shift remaining alerts up
  });
}

function newsAlert() {
  "use strict";
  var news = getJson("/news");
  var date = getStorage("newsDate");
  if (news !== undefined &&
     (date === undefined || news.Date > date) &&
      news.Message !== undefined &&
      news.Severity !== undefined) {
    if (autoloadCookie() !== undefined) {
      alert(news.Message);
    } else {
      myAlert(news.Severity, news.Message, 604800000);
    }
    setStorage("newsDate", news.Date, typeof(1));
  }
}

function buildCategoryButtons() {
  "use strict";
  var buttonString = "";
  var buttonCount = 0;
  var categories = getCategories();

  if (categories !== undefined) {
    $.each(categories, function(i, field) {
      if (field === "No Categories Found" || field === "I/O Error on Host") {
        return;
      }
      if (navigator.onLine && isCategoryCacheable(field)) {
        buttonString += "<div class=\"btn-group\">";
        buttonString += "<button class=\"btn btn-primary btn-custom-main\" onclick=\"loadPage('Exploit Selection', '" + field + "');\">" + field + "</button>";
        buttonString += "<button type=\"button\" class=\"btn btn-primary btn-custom-dropdown dropdown-toggle dropdown-toggle-split\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\"></button>";
        buttonString += "<div class=\"dropdown-menu\">";
        buttonString += "<a class=\"dropdown-item\" href=\"#\" onclick=\"myCategoryMeta('" + field + "');\">About</a>";
        buttonString += "<div class=\"dropdown-divider\"></div>";
        buttonString += "<a class=\"dropdown-item\" href=\"#\" onclick=\"cacheCategory('" + field + "');\">Cache</a>";
        buttonString += "</div>";
        buttonString += "</div>";
        buttonCount += 1;
        if (buttonCount % 3 === 0) {
          buttonString += "<br>";
        }
      } else if ((navigator.onLine && !isCategoryCacheable(field)) || (!navigator.onLine && isCategoryCacheable(field))) {
        buttonString += "<div class=\"btn-group\">";
        buttonString += "<button class=\"btn btn-primary btn-custom-main\" onclick=\"loadPage('Exploit Selection', '" + field + "');\">" + field + "</button>";
        buttonString += "<button type=\"button\" class=\"btn btn-primary btn-custom-dropdown dropdown-toggle dropdown-toggle-split\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\"></button>";
        buttonString += "<div class=\"dropdown-menu\">";
        buttonString += "<a class=\"dropdown-item\" href=\"#\" onclick=\"myCategoryMeta('" + field + "');\">About</a>";
        buttonString += "</div>";
        buttonString += "</div>";
        buttonCount += 1;
        if (buttonCount % 3 === 0) {
          buttonString += "<br>";
        }
      }
    });
    buttonString += "<div class=\"btn-group\">";
    buttonString += "<button class=\"btn btn-primary btn-custom-main btn-custom-full\" onclick=\"cacheAll();\">[Cache All]</button>";
    buttonString += "</div>";
    return buttonString;
  }
  return;
}

function buildEntryButtons(category) {
  "use strict";
  var buttonString = "";
  var buttonCount = 0;
  var entries = getEntries(category);

  if (entries !== undefined) {
    $.each(entries, function(i, field) {
      if (field === "No Entries Found" || field === "I/O Error on Host") {
        return;
      }
      if (navigator.onLine && isCategoryCacheable(category)) {
        buttonString += "<div class=\"btn-group\">";
        buttonString += "<button class=\"btn btn-primary btn-custom-main\" onclick=\"myLoader('" + category + "', '" + field + "');\">" + field + "</button>";
        buttonString += "<button type=\"button\" class=\"btn btn-primary btn-custom-dropdown dropdown-toggle dropdown-toggle-split\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\"></button>";
        buttonString += "<div class=\"dropdown-menu\">";
        buttonString += "<a class=\"dropdown-item\" href=\"#" + category + "\" onclick=\"myEntryMeta('" + category + "', '" + field + "');\">About</a>";
        buttonString += "<a class=\"dropdown-item\" href=\"#" + category + "\" onclick=\"mySetAutoload('" + category + "', '" + field + "');\">Autoload</a>";
        buttonString += "<div class=\"dropdown-divider\"></div>";
        buttonString += "<a class=\"dropdown-item\" href=\"#" + category + "\" onclick=\"cacheEntry('" + category + "', '" + field + "');\">Cache</a>";
        buttonString += "</div>";
        buttonString += "</div>";
        buttonCount += 1;
        if (buttonCount % 3 === 0) {
          buttonString += "<br>";
        }
      } else if ((navigator.onLine && !isCategoryCacheable(category)) || (!navigator.onLine && isEntryAvailableOffline(category, field))) {
        buttonString += "<div class=\"btn-group\">";
        buttonString += "<button class=\"btn btn-primary btn-custom-main\" onclick=\"myLoader('" + category + "', '" + field + "');\">" + field + "</button>";
        buttonString += "<button type=\"button\" class=\"btn btn-primary btn-custom-dropdown dropdown-toggle dropdown-toggle-split\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\"></button>";
        buttonString += "<div class=\"dropdown-menu\">";
        buttonString += "<a class=\"dropdown-item\" href=\"#" + category + "\" onclick=\"myEntryMeta('" + category + "', '" + field + "');\">About</a>";
        buttonString += "<a class=\"dropdown-item\" href=\"#" + category + "\" onclick=\"mySetAutoload('" + category + "', '" + field + "');\">Autoload</a>";
        buttonString += "</div>";
        buttonString += "</div>";
        buttonCount += 1;
        if (buttonCount % 3 === 0) {
          buttonString += "<br>";
        }
      }
    });
    return buttonString;
  }
  return;
}

function loadPage(title, header) {
  "use strict";
  if (title === undefined || header === undefined) {
    title = "Category Selection";
    header = "Categories";
  }

  if (title === "Category Selection") {
    var categoryButtons = buildCategoryButtons();
    if (categoryButtons !== undefined) {
      $(document).attr("title", title + " | Exploit Host by Al Azif");
      $("#title").html(title);
      $("#header").html(header);
      $("#buttons").html(categoryButtons);
    } else {
      myAlert("danger", "Error retrieving categories!");
    }
  } else if (title === "Exploit Selection") {
    var entryButtons = buildEntryButtons(header);
    if (entryButtons !== undefined) {
      history.pushState(null, null, "#" + header);
      $(document).attr("title", title + " | Exploit Host by Al Azif");
      $("#title").html(title);
      $("#header").html(header);
      $("#buttons").html(entryButtons);
    } else {
      myAlert("danger", "Error retrieving entries!");
    }
  } else {
    myAlert("danger", "Theme error");
  }
}

function clearOverlays() {
  "use strict";
  $("#cacheOverlay").hide();
  $("#barText").hide();
  $("#barBack").hide();
  $("#barLoad").hide();
  $("#barLoad").html("");
  $("#barLoad").width("0%");
  $("#exploitOverlay").hide();
  $("#exploitMessage").hide();
  $("#exploitMessage").html("");
  $("#exploitLoader").hide();
}

function showCaching() {
  "use strict";
  $("#cacheOverlay").show();
  $("#barText").show();
  $("#barBack").show();
  $("#barLoad").show();
}

function showLoader() {
  "use strict";
  $("#exploitOverlay").show();
  $("#exploitLoader").show();
  $("#exploitMessage").show();
}

function exploitDone(message) {
  "use strict";
  $("#exploitLoader").hide();
  $("#exploitMessage").html(message);
  sleep(3000).then(function() {
    if ($("#exploitMessage").html() !== "Waiting..." && $("#exploitMessage").html() !== "Awaiting Payload...") {
      clearFrame();
      clearOverlays();
    }
  });
}

function cacheInterface(callback) {
  "use strict";
  if (callback === "ondownloading") {
    $("#barText").html("Caching...");
    showCaching();
  } else if (callback === "ondownloading-redirect") {
    $("#barText").html("Caching Redirect...");
    showCaching();
  } else if (callback === "ondownloading-theme") {
    $("#barText").html("Caching Theme...");
    showCaching();
  } else {
    clearFrame();
    clearOverlays();
    if (callback === "oncached") {
      myAlert("success", "Cached Successfully");
    } else if (callback === "onupdateready") {
      myAlert("success", "Cache updated");
    } else if (callback === "onnoupdate") {
      myAlert("primary", "No update available");
    } else if (callback === "onerror") {
      myAlert("danger", "Error caching resources");
    } else if (callback === "onobsolete") {
      myAlert("danger", "Manifest returned a 404, cache was deleted");
    } else if (callback === "oncached-redirect" || callback === "onupdateready-redirect" || callback === "onnoupdate-redirect") {
      hostRedirect();
    } else if (callback === "onerror-redirect") {
      myAlert("danger", "Error caching redirect");
    } else if (callback === "onobsolete-redirect") {
      myAlert("danger", "Manifest returned a 404, redirect was deleted");
    } else if (callback === "oncached-theme" || callback === "onnoupdate-theme") {
      // Do Nothing...
    } else if (callback === "onupdateready-theme") {
      setStorage("newsDate", 0, typeof(1));
      location.reload(true);
    } else if (callback === "onerror-theme") {
      myAlert("danger", "Error caching theme resources");
    } else if (callback === "onobsolete-theme") {
      myAlert("danger", "Manifest returned a 404, theme cache was deleted");
    }
  }
}

function cacheProgress(percent) {
  "use strict";
  $("#barLoad").width(percent + "%");
  $("#barLoad").html(percent + "%");
}

function myLoader(category, entry) {
  "use strict";
  showLoader();
  loadEntry(category, entry);
}

function mySetAutoload(category, entry) {
  "use strict";
  setAutoload(category, entry);
  if (isCategoryCacheable(category)) {
    cacheEntry(category, entry);
  }
  // TODO: Wait for cache to complete (Check for alerts?)
  // then loadEntry(category, entry)
}

function myCategoryMeta(category) {
  "use strict";
  var meta = getCategoryMeta(category);

  if (meta === undefined) {
    myAlert("danger", "Unable to retrieve metadata");
    return;
  }

  var title;
  if (meta.Title !== undefined){
    title = meta.Title;
  }

  var device;
  if (meta.Device !== undefined) {
    device = meta.Device;
  }

  var firmware;
  if (meta.Firmware !== undefined) {
    firmware = meta.Firmware;
  }

  var uaMatch = "<span class=\"badge badge-danger\">Mismatch</span>";
  if (checkUAMatch(meta.User_Agents)) {
    uaMatch = "<span class=\"badge badge-success\">Match</span>";
  }

  var lang = getLanguage();
  if (lang === undefined) {
    setLanguage("default");
    lang = "default";
  }

  var notes = meta.Notes[lang];
  if (notes === undefined) {
    notes = meta.Notes.default;
  }
  if (notes === undefined) {
    notes = "";
  }

  var modalBody = "<div class=\"row\"><div class=\"col-sm-3\">Device:</div><div class=\"col-sm-9\">" + device + "</div></div>";
  modalBody += "<div class=\"row\"><div class=\"col-sm-3\">Firmware:</div><div class=\"col-sm-9\">" + firmware + "</div></div>";
  modalBody += "<div class=\"row\"><div class=\"col-sm-3\">UA Match?:</div><div class=\"col-sm-9\">" + uaMatch + "</div></div>";
  modalBody += "<div class=\"row\"><div class=\"col-sm-3\">Notes:</div><div class=\"col-sm-9\">" + notes + "</div></div>";

  $("#metaModalTitle").html(title);
  $("#metaModalBody").html(modalBody);
  $("#metaModal").modal("show");
}

function myEntryMeta(category, entry) {
  "use strict";
  var meta = getEntryMeta(category, entry);

  if (meta === undefined) {
    myAlert("danger", "Unable to retrieve metadata");
    return;
  }

  var title = "";
  if (meta.Title !== undefined) {
    title = meta.Title;
  }

  var version = "";
  if (meta.Version !== undefined) {
    version = meta.Version;
  }

  var updated = "";
  if (meta.Updated !== undefined) {
    updated = meta.Updated;
  }

  var device = "";
  if (meta.Device !== undefined) {
    device = meta.Device;
  }

  var firmware = "";
  if (meta.Firmware !== undefined) {
    firmware = meta.Firmware;
  }

  var lang = getLanguage();
  if (lang === undefined) {
    setLanguage("default");
    lang = "default";
  }

  var description = meta.Description[lang];
  if (description === undefined) {
    description = meta.Description.default;
  }
  if (description === undefined) {
    description = "";
  }

  var url = "";
  if (meta.URL !== undefined) {
    url = meta.URL;
  }

  var modalBody = "<div class=\"row\"><div class=\"col-sm-3\">Version:</div><div class=\"col-sm-9\">" + version + "</div></div>";
  modalBody += "<div class=\"row\"><div class=\"col-sm-3\">Updated:</div><div class=\"col-sm-9\">" + updated + "</div></div>";
  modalBody += "<div class=\"row\"><div class=\"col-sm-3\">Device:</div><div class=\"col-sm-9\">" + device + "</div></div>";
  modalBody += "<div class=\"row\"><div class=\"col-sm-3\">Firmware:</div><div class=\"col-sm-9\">" + firmware + "</div></div>";
  modalBody += "<div class=\"row\"><div class=\"col-sm-3\">Description:</div><div class=\"col-sm-9\">" + description + "</div></div>";
  modalBody += "<div class=\"row\"><div class=\"col-sm-3\">URL:</div><div class=\"col-sm-9\"><a href=\"" + url + "\">" + url + "</a></div></div>";

  $("#metaModalTitle").html(title);
  $("#metaModalBody").html(modalBody);
  $("#metaModal").modal("show");
}

// --- Handlers ---------------------------------------------------------------

$(window).on("keyup", function(event) {
  "use strict";
  if (event.keyCode === 27) {
    history.replaceState("", document.title, window.location.pathname + window.location.search);
    clearFrame();
    clearOverlays();
    loadPage();
  }
});

// --- Redirects --------------------------------------------------------------

if (location.hostname === "165.227.83.145") {
  location.replace("https://cthugha.thegate.network/");
}

if (location.hostname === "108.61.128.158") {
  location.replace("https://ithaqua.thegate.network/");
}

if (defaultHomepages() !== undefined && !navigator.onLine) {
  hostRedirect();
}

// --- On Ready ---------------------------------------------------------------

$(function() {
  "use strict";
  $("#ifr").attr("src", "/blank.html");

  if (defaultHomepages() !== undefined && navigator.onLine) {
    var country = "xx";
    var myRegexp = /^\/document\/([a-z]{2,5})\/ps4\/index.html$/;
    var match = myRegexp.exec(location.pathname);
    if (match !== null) {
      country = match[1];
    }
    cacheRedirect(country);
  } else if (navigator.onLine) {
    cacheTheme();
  }

  if (navigator.onLine) {
    newsAlert();
  }

  if (window.location.hash) {
    loadPage("Exploit Selection", decodeURIComponent(window.location.hash.substr(1)));
  } else {
    loadPage();
  }

  var autoload = autoloadCookie();
  if (autoload !== undefined) {
    if (!navigator.onLine && (!isCategoryCacheable(autoload.split("/")[0]) || !isEntryAvailableOffline(autoload.split("/")[0], autoload.split("/")[1]))) {
      myAlert("danger", "Could not autoload, payload is online only (Currently running from cache)");
    } else {
      myLoader(autoload.split("/")[0], autoload.split("/")[1]);
    }
  }
});
/*
Copyright (c) 2017-2018 Al Azif, https://github.com/Al-Azif/ps4-exploit-host

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/