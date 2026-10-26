// Minimal stand-in for the Tizen APIs HomeShelf uses, for browser previews only.
// App names are the ones the reference TV returns; icons live on the TV and
// are not available here, so tiles show their labels only.
// ?focus=<appId> preselects a tile, as if HomeShelf had stored it earlier.
(function () {
  "use strict";
  var APPS = {
    "9Ur5IzDKqV.TizenYouTube": "YouTube",
    "cg2m3QSB89.7tv": "Joyn",
    "RN1MCdNq8t.Netflix": "Netflix",
    "MCmYXNxgcu.DisneyPlus": "Disney+"
  };
  var focus = /[?&]focus=([^&]+)/.exec(location.search);
  try {
    if (focus) localStorage.setItem("homeshelf.focusAppId", decodeURIComponent(focus[1]));
  } catch (e) { /* storage unavailable: first tile is focused */ }

  function info(id) {
    if (!APPS[id]) throw new Error("NotFoundError: " + id);
    return { id: id, name: APPS[id], iconPath: "", show: true, categories: [] };
  }

  window.tizen = {
    application: {
      getAppInfo: info,
      getAppsInfo: function (ok) { ok(Object.keys(APPS).map(info)); },
      getCurrentApplication: function () {
        return {
          appInfo: { id: "HmShlf0001.HomeShelf" },
          exit: function () { console.log("[mock] exit"); },
          getRequestedAppControl: function () { return null; }
        };
      },
      launch: function (id) { console.log("[mock] launch " + id); }
    },
    tvinputdevice: {
      registerKeyBatch: function () {}
    }
  };
})();
