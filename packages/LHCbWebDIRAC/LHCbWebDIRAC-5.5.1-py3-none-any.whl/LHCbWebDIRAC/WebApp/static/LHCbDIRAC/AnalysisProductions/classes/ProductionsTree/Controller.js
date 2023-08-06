/*****************************************************************************\
* (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/
Ext.define("LHCbDIRAC.AnalysisProductions.classes.ProductionsTree.Controller", {
  extend: "Ext.app.ViewController",

  alias: "controller.AnalysisProductions.classes.ProductionsTree.Controller",

  updateTreeFilters: function () {
    var store = this.lookupReference("prodList").getStore();
    // Parameters
    var query = this.lookupReference("filterTextField").value || "*";
    var showArchived = this.lookupReference("filterShowArchived").value;

    // Expand all nodes if fitering with text
    if (query.length > 0) {
      store.getRoot().expandChildren(true);
    } else {
      store.getRoot().collapseChildren(true);
    }

    // Accept fnmatch-like patterns when filtering with text
    var pattern = new RegExp(
      query
        .replace(/[|\\{}()[\]^$+*?.]/g, "\\$&")
        .replace(/-/g, "\\x2d")
        .replace("\\*", ".*"),
      "i"
    );

    function filterFn(item) {
      path = item.getPath("name");
      if (item.get("root") === true) return true;
      var visible = true;
      visible &= showArchived || !item.get("archived");
      visible &= pattern.test(path);
      return visible;
    }
    store.getFilters().replaceAll({
      filterFn: filterFn,
    });
  },
});
