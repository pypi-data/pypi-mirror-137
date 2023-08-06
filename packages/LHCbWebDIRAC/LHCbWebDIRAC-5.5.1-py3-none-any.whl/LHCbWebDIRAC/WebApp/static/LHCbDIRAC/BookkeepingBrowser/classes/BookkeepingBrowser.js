/*****************************************************************************\
* (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/
/*
 * This is the WUI of the LHCb Bookkeeping system.
 */
Ext.define("LHCbDIRAC.BookkeepingBrowser.classes.BookkeepingBrowser", {
  extend: "Ext.dirac.core.Module",
  requires: [
    "Ext.panel.Panel",
    "Ext.dirac.utils.DiracAjaxProxy",
    "LHCbDIRAC.BookkeepingBrowser.classes.BookkeepingTreeItemModel",
    "Ext.dirac.utils.DiracGridPanel",
    "Ext.dirac.utils.DiracPagingToolbar",
    "Ext.dirac.utils.DiracJsonStore",
    "LHCbDIRAC.BookkeepingBrowser.classes.SaveForm",
    "LHCbDIRAC.BookkeepingBrowser.classes.BookkeepingAddBookmarks",
    "LHCbDIRAC.BookkeepingBrowser.classes.FileHistoryPanel",
    "LHCbDIRAC.BookkeepingBrowser.classes.ProcessingPassViewer",
    "LHCbDIRAC.BookkeepingBrowser.classes.LookupWindow",
    "Ext.grid.filters.Filters",
  ],
  loadState: function (data) {
    var me = this;
    me.treePanel.setLoading("Loading Bookkeeping path...");
    var expandedNodes = Ext.JSON.decode(data.expandedNodes);
    var paths = [];
    if (expandedNodes) {
      me.__serializeExpansionAction("", expandedNodes[""], paths);
    }
    // TODO implement a tree widget which saves the state data.
    var selectNode = function () {
      if (data.currentPosition) {
        me.treePanel.getSelectionModel().select(data.currentPosition);
      }
      me.treePanel.setLoading(false);
    };
    me.expandPath(paths, null, null, selectNode);
  },
  getStateData: function () {
    var me = this;
    var oReturn = {};
    oReturn.expandedNodes = Ext.JSON.encode(me.expansionState);
    var selModel = me.treePanel.getSelectionModel();
    if (selModel) {
      var position = selModel.getCurrentPosition();
      if (position) {
        oReturn.currentPosition = position.row;
      }
    }
    oReturn.selectedValues = me.__getSelectedData();
    return oReturn;
  },
  fullpath: "",
  prefix: "sim+std:/",
  expansionState: {},
  initComponent: function () {
    var me = this;

    me.launcher.title = "LHCb Bookkeeping browser";
    me.launcher.maximized = false;

    if (GLOBAL.VIEW_ID == "desktop") {
      var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

      me.launcher.width = oDimensions[0];
      me.launcher.height = oDimensions[1];

      me.launcher.x = 0;
      me.launcher.y = 0;
    }

    Ext.apply(me, {
      stateId: "bk-main-panel",
      stateful: true,
      layout: "border",
      bodyBorder: false,
      defaults: {
        collapsible: true,
        split: true,
      },
    });

    me.callParent(arguments);
  },
  buildUI: function () {
    var me = this;

    me.treeStore = Ext.create("Ext.data.TreeStore", {
      model: "LHCbDIRAC.BookkeepingBrowser.classes.BookkeepingTreeItemModel",
      fields: ["text", "selection", "fullpath", "level"],
      scope: me,
      proxy: {
        type: "ajax",
        url: "BookkeepingBrowser/getNodes",
      },
      root: {
        text: "/",
        id: "/",
        expanded: false,
      },
      folderSort: true,
      sorters: [
        {
          property: "text",
          direction: "ASC",
        },
      ],
      listeners: {
        beforeload: function (store, operation, eOpts) {
          var me = this;
          store.proxy.extraParams = me.__getSelectedData();
        },
        collapse: function (oNode, eOpts) {
          var data = oNode.getData();
          me.fullpath = data.fullpath;
          me.__setBkPathTextField(data.fullpath);
          me.__oprUnsetPathAsExpanded(data.fullpath, true);
        },
        expand: function (oNode, eOpts) {
          var data = oNode.getData();
          me.fullpath = data.fullpath;
          me.__setBkPathTextField(data.fullpath);
          me.__oprPathAsExpanded(data.fullpath, true);
        },
        scope: me,
      },
    });

    me.treeContextMenu = Ext.create("Ext.menu.Menu", {
      fullpath: "",
      parent: me,
      items: [
        {
          text: "Add bookmark",
          handler: function () {
            var me = this;
            me.parentMenu.parent.fullpath = me.parentMenu.fullpath;
            var path = me.parentMenu.parent.prefix + me.parentMenu.fullpath;
            me.parentMenu.parent.addBookmark(path);
          },
        },
        {
          text: "More info",
          handler: function () {
            var me = this;
            me.parentMenu.parent.getContainer().body.mask("Wait ...");
            if (me.parentMenu.method == "getProcessingPass") {
              var pview = Ext.create("LHCbDIRAC.BookkeepingBrowser.classes.ProcessingPassViewer", {
                url: GLOBAL.BASE_URL + me.parentMenu.parent.applicationName + "/processingpass",
                params: {
                  stepName: me.parentMenu.text,
                },
              });
              var window = me.parentMenu.parent.getContainer().createChildWindow("ProcessingPass view" + me.parentMenu.text, false, 900, 500);
              window.add(pview);
              // Todo: this can be removed after ext-6.2.0;
              window.show().removeCls("x-unselectable");
              me.parentMenu.parent.getContainer().body.unmask();
            } else if (me.parentMenu.method == "getFileTypes") {
              me.parentMenu.parent.getContainer().body.mask("Wait ...");
              var sel = me.parentMenu.selection;
              sel["FileType"] = me.parentMenu.text;
              var pview = Ext.create("LHCbDIRAC.BookkeepingBrowser.classes.ProcessingPassViewer", {
                url: GLOBAL.BASE_URL + me.parentMenu.parent.applicationName + "/stepmetadata",
                params: {
                  bkQuery: Ext.JSON.encode(sel),
                },
              });
              var window = me.parentMenu.parent.getContainer().createChildWindow("ProcessingPass view" + me.parentMenu.text, false, 900, 500);
              window.add(pview);
              // Todo: this can be removed after ext-6.2.0;
              window.show().removeCls("x-unselectable");
            } else if (me.parentMenu.method == "getConditions") {
              var sel = me.parentMenu.selection;
              sel["ConditionDescription"] = me.parentMenu.text;
              Ext.Ajax.request({
                url: GLOBAL.BASE_URL + me.parentMenu.parent.applicationName + "/conditions",
                method: "POST",
                params: {
                  bkQuery: Ext.JSON.encode(sel),
                },
                success: function (response) {
                  var jsonData = Ext.JSON.decode(response.responseText);
                  if (jsonData["success"] == "true") {
                    if (jsonData["CondType"] == "sim") {
                      var tplMarkup = [
                        "<b>SimId:</b> {SimId}<br/>",
                        "<b>Description:</b> {Description}<br/>",
                        "<b>BeamCondition:</b> {BeamCondition}<br/>",
                        "<b>BeamEnergy:</b> {BeamEnergy}<br/>",
                        "<b>Generator:</b> {Generator}<br/>",
                        "<b>MagneticField:</b> {MagneticField}<br/>",
                        "<b>DetectorCondition:</b> {DetectorCondition}<br/>",
                        "<b>Luminosity:</b> {Luminosity}<br/>",
                        "<b>G4settings:</b> {G4settings}<br/>",
                      ];
                    } else {
                      var tplMarkup = [
                        "<b>DaqperiodId:</b> {DaqperiodId}<br/>",
                        "<b>Description:</b> {Description}<br/>",
                        "<b>BeamCondition:</b> {BeamCondition}<br/>",
                        "<b>BeanEnergy:</b> {BeanEnergy}<br/>",
                        "<b>MagneticField:</b> {MagneticField}<br/>",
                        "<b>VELO:</b> {VELO}<br/>",
                        "<b>IT:</b> {IT}<br/>",
                        "<b>TT:</b> {TT}<br/>",
                        "<b>OT:</b> {OT}<br/>",
                        "<b>RICH1:</b> {RICH1}<br/>",
                        "<b>RICH2:</b> {RICH2}<br/>",
                        "<b>SPD_PRS:</b> {SPD_PRS}<br/>",
                        "<b>ECAL:</b> {ECAL}<br/>",
                        "<b>HCAL:</b> {HCAL}<br/>",
                        "<b>MUON:</b> {MUON}<br/>",
                        "<b>L0:</b> {L0}<br/>",
                        "<b>HLT:</b> {HLT}<br/>",
                        "<b>VeloPosition:</b> {VeloPosition}<br/>",
                      ];
                    }
                    me.parentMenu.parent
                      .getContainer()
                      .oprPrepareAndShowWindowTpl(tplMarkup, jsonData["result"], "Condition description " + me.parentMenu.text);
                  } else {
                    GLOBAL.APP.CF.alert(jsonData["error"], "Error");
                  }
                },
              });
            }
            me.parentMenu.parent.getContainer().body.unmask();
          },
        },
        {
          text: "Show path",
          handler: function () {
            var me = this;
            GLOBAL.APP.CF.alert(me.parentMenu.fullpath, "info");
          },
        },
      ],
    });

    me.treePanel = Ext.create("Ext.tree.Panel", {
      title: "Bookkeeping tree",
      stateful: true,
      stateId: "bk-tree-panel",
      layout: "fit",
      store: me.treeStore,
      leadingBufferZone: 10000,
      listeners: {
        itemclick: function (aa, record, item, index, e, eOpts) {
          var me = this;
          if (record.data.level == "FileTypes") {
            me.__setBkPathTextField(record.data.fullpath);
            var store = me.grid.getStore();
            if (me.grid.store) {
              me.grid.store.currentPage = 1;
              me.bkQuery = record.get("selection");
              me.bkQuery["FileType"] = record.get("text");
              me.grid.store.proxy.extraParams = me.__getSelectedData();
              me.grid.store.proxy.extraParams["fullpath"] = record.get("fullpath");
              me.grid.store.load();
            }
          }
        },
        beforecellcontextmenu: function (table, td, cellIndex, record, tr, rowIndex, e, eOpts) {
          e.preventDefault();
          me.treeContextMenu.fullpath = record.get("fullpath");
          me.treeContextMenu.selection = record.get("selection");
          me.treeContextMenu.method = record.get("method");
          me.treeContextMenu.text = record.get("text");
          me.treeContextMenu.showAt(e.getXY());
          return false;
        },
        scope: me,
      },
    });

    var oPanelButtons = new Ext.create("Ext.toolbar.Toolbar", {
      dock: "bottom",
      layout: {
        pack: "center",
      },
      items: [],
    });

    me.oMenuButton = new Ext.button.Button({
      text: "Simulation Condition",
      value: "Configuration",
      menu: [
        {
          text: "Simulation Condition",
          handler: function (item) {
            var me = this;
            me.oMenuButton.setText(item.text);
            me.oMenuButton.value = "Configuration";
            me.__refreshTree();
          },
          scope: me,
        },
        {
          text: "EventType",
          handler: function (item) {
            var me = this;
            me.oMenuButton.setText(item.text);
            me.oMenuButton.value = "Event type";
            me.__refreshTree();
          },
          scope: me,
        },
        {
          text: "Run lookup",
          handler: function (item) {
            var me = this;
            me.oMenuButton.setText(item.text);
            me.oMenuButton.value = "Runlookup";
            var win = Ext.create("LHCbDIRAC.BookkeepingBrowser.classes.LookupWindow", {
              title: "Run lookup",
              url: GLOBAL.BASE_URL + me.applicationName + "/runs",
            });
            win.show();
            win.on("okPressed", function () {
              var runs = win.form.getValues();
              var jsonData = {
                expanded: true,
                text: "/",
                children: [],
              };
              var rootNode = me.treeStore.getRootNode();
              // remove all child node.
              rootNode.removeAll();
              for (var key in runs) {
                for (var i = 0; i < runs[key].length; i++) {
                  var node = {
                    text: "/" + runs[key][i],
                    id: "/" + runs[key][i],
                  };
                  jsonData["children"].push(node);
                }
              }
              me.treePanel.setRootNode(jsonData);
              win.onCancel();
            });
          },
          scope: me,
        },
        {
          text: "Production lookup",
          handler: function (item) {
            me.oMenuButton.setText(item.text);
            me.oMenuButton.value = "Productions";
            var win = Ext.create("LHCbDIRAC.BookkeepingBrowser.classes.LookupWindow", {
              title: "Production lookup",
              url: GLOBAL.BASE_URL + me.applicationName + "/productions",
            });
            win.show();
            win.on("okPressed", function () {
              var runs = win.form.getValues();
              var jsonData = {
                expanded: true,
                text: "/",
                children: [],
              };
              var rootNode = me.treeStore.getRootNode();
              // remove all child node.
              rootNode.removeAll();
              for (var key in runs) {
                for (var i = 0; i < runs[key].length; i++) {
                  var node = {
                    text: "/" + runs[key][i],
                    id: "/" + runs[key][i],
                  };
                  jsonData["children"].push(node);
                }
              }
              me.treePanel.setRootNode(jsonData);
              win.onCancel();
            });
          },
          scope: me,
        },
      ],
    });

    oPanelButtons.add(me.oMenuButton);

    me.advButton = new Ext.form.field.Checkbox({
      boxLabel: "Advanced",
      name: "advQuery",
      inputValue: "std",
      checked: false,
      handler: function () {
        var me = this;
        if (me.advButton.getValue()) {
          me.advButton.inputValue = "adv";
        } else {
          me.advButton.inputValue = "std";
        }
        me.__refreshTree();
      },
      scope: me,
    });
    oPanelButtons.add(me.advButton);

    me.btnRefresh = new Ext.Button({
      text: "Refresh",
      margin: 3,
      iconCls: "dirac-icon-refresh",
      handler: function () {
        me.__refreshTree();
      },
      scope: me,
    });
    oPanelButtons.add(me.btnRefresh);

    me.treePanel.addDocked(oPanelButtons);

    var oProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
      url: "BookkeepingBrowser/getdataquality",
    });

    var dataQualitystore = new Ext.data.JsonStore({
      proxy: oProxy,
      fields: ["name", "value"],
    });

    me.dataQuality = new Ext.grid.Panel({
      title: "Data quality",
      height: 200,
      width: 400,
      layout: "fit",
      store: dataQualitystore,
      columns: [
        {
          flex: 1,
          text: "Name",
          dataIndex: "name",
        },
        {
          xtype: "checkcolumn",
          text: "Value",
          dataIndex: "value",
        },
      ],
      listeners: {
        expand: function (p, eOpts) {
          dataQualitystore.load();
        },
      },
    });

    var bookmarksProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
      url: "BookkeepingBrowser/getBookmarks",
    });
    var bookmarksStore = new Ext.data.JsonStore({
      proxy: bookmarksProxy,
      fields: ["name", "value"],
    });

    me.bookmarksPanel = new Ext.grid.Panel({
      title: "Bookmarks",
      height: 200,
      width: 400,
      layout: "fit",
      store: bookmarksStore,
      columns: [
        {
          flex: 1,
          text: "Name",
          dataIndex: "name",
          width: 30,
        },
        {
          menuDisabled: true,
          sortable: false,
          xtype: "actioncolumn",
          width: 20,
          items: [
            {
              iconCls: "toolbar-other-close",
              tooltip: "Remove bookmark",
              handler: function (grid, rowIndex, colIndex) {
                var rec = me.bookmarksPanel.getStore().getAt(rowIndex);
                var message = "Do you want to delete the " + rec.get("name") + " bookmarks?";
                Ext.MessageBox.confirm("Confirm", message, function (button) {
                  if (button === "yes") {
                    var path = rec.get("value");
                    var title = rec.get("name");
                    Ext.Ajax.request({
                      url: "BookkeepingBrowser/deleteBookmark",
                      params: {
                        title: title,
                        path: path,
                      },
                      success: function (response) {
                        var value = Ext.JSON.decode(response.responseText);
                        if (value.success == "false") {
                          GLOBAL.APP.CF.alert(value.error, "error");
                        } else {
                          GLOBAL.APP.CF.alert(value.result, "info");
                          me.bookmarksPanel.getStore().load();
                        }
                      },
                      failure: function (response, opts) {
                        GLOBAL.APP.CF.showAjaxErrorMessage(response);
                      },
                    });
                  }
                });
              },
            },
          ],
        },
        {
          text: "Value",
          dataIndex: "value",
          hidden: true,
        },
      ],
      listeners: {
        expand: function (p, eOpts) {
          bookmarksStore.load();
        },
        cellclick: function (td, cellIndex, record, tr, rowIndex, e, eOpts) {
          var value = tr.get("value");
          var serialisedPath = me.__prepareExpandPath(value);

          var disableLoading = function () {
            me.treePanel.setLoading(false);
          };
          me.treePanel.expand();
          me.treePanel.setLoading(true);
          me.expandPath(serialisedPath, null, null, disableLoading);
        },
      },
    });

    me.leftPanel = Ext.create("Ext.panel.Panel", {
      region: "west",
      floatable: false,
      stateful: true,
      stateId: "bk-left-panel",
      margins: "0",
      width: 350,
      minWidth: 230,
      maxWidth: 850,
      bodyPadding: 5,
      scrollable: true,
      layout: "accordion",
      items: [me.treePanel, me.dataQuality, me.bookmarksPanel],
      oprLoadGridData: function () {
        me.grid.store.reload();
      },
    });
    me.dataFields = [
      {
        name: "Name",
      },
      {
        name: "EventStat",
      },
      {
        name: "FileSize",
      },
      {
        name: "RunNumber",
      },
      {
        name: "PhysicStat",
      },
      {
        name: "CreationDate",
        type: "date",
        dateFormat: "Y-m-d H:i:s",
      },
      {
        name: "JobStart",
        type: "date",
        dateFormat: "Y-m-d H:i:s",
      },
      {
        name: "JobEnd",
        type: "date",
        dateFormat: "Y-m-d H:i:s",
      },
      {
        name: "WorkerNode",
      },
      {
        name: "FileType",
      },
      {
        name: "EvtTypeId",
      },
      {
        name: "DataqualityFlag",
      },
      {
        name: "TCK",
        type: "string",
      },
    ];

    var oProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
      url: "BookkeepingBrowser/getFiles",
    });

    me.dataStore = Ext.create("Ext.dirac.utils.DiracJsonStore", {
      proxy: oProxy,
      fields: me.dataFields,
      scope: me,
      pagesize: 500,
    });

    me.dataStore.on("load", function (records, successful, eOpts) {
      var proxy = records.getProxy();
      if (proxy) {
        var reader = proxy.getReader();
        if (reader) {
          var extraParameters = reader.rawData.ExtraParameters;
          if (extraParameters) {
            var globalStatistics = extraParameters.GlobalStatistics;
            if (globalStatistics) {
              me.statisticsSet.items.getAt(me.statisticsSet.items.findIndex("name", "fsize")).setRawValue(globalStatistics["Files Size"]);
              me.statisticsSet.items.getAt(me.statisticsSet.items.findIndex("name", "luminosity")).setRawValue(globalStatistics["Luminosity"]);
              me.statisticsSet.items.getAt(me.statisticsSet.items.findIndex("name", "nbfiles")).setRawValue(globalStatistics["Number of Files"]);
              me.statisticsSet.items.getAt(me.statisticsSet.items.findIndex("name", "nbevents")).setRawValue(globalStatistics["Number of Events"]);
            }
            var selection = extraParameters.Selection;
            if (selection) {
              me.fullpath = selection.fullpath;
              me.selectionSet.items.getAt(me.selectionSet.items.findIndex("name", "cName")).setRawValue(selection.ConfigName);
              me.selectionSet.items.getAt(me.selectionSet.items.findIndex("name", "cVersion")).setRawValue(selection.ConfigVersion);
              me.selectionSet.items.getAt(me.selectionSet.items.findIndex("name", "conditions")).setRawValue(selection.ConditionDescription);
              me.selectionSet.items.getAt(me.selectionSet.items.findIndex("name", "procpass")).setRawValue(selection.ProcessingPass);
              me.selectionSet.items.getAt(me.selectionSet.items.findIndex("name", "etype")).setRawValue(selection.EventType);
              me.selectionSet.items.getAt(me.selectionSet.items.findIndex("name", "ftype")).setRawValue(selection.FileType);
            }
          }
        }
      }
    });

    var pagingToolbar = Ext.create("Ext.dirac.utils.DiracPagingToolbar", {
      dataStore: me.dataStore, // TODO: make sure we are using correct
      // store ...
      store: me.dataStore,
      scope: me,
    });

    var oColumns = {
      "#": {
        properties: {
          width: 50,
          sortable: false,
          locked: true,
          renderer: function (a, b, c, rowIndex, d, ds) {
            return me.__pageRowNumber(ds, rowIndex);
          },
          hideable: false,
          fixed: true,
          menuDisabled: true,
        },
      },
      "File Name": {
        dataIndex: "Name",
        properties: {
          width: 520,
        },
      },
      "Event Stat": {
        dataIndex: "EventStat",
      },
      "File Size": {
        dataIndex: "FileSize",
      },
      "Run number": {
        dataIndex: "RunNumber",
      },
      "Physics statistics": {
        dataIndex: "PhysicStat",
        properties: {
          hidden: true,
        },
      },
      "Creation Date": {
        dataIndex: "CreationDate",
        properties: {
          renderer: Ext.util.Format.dateRenderer("Y-m-d H:i:s"),
        },
      },
      "Job Start": {
        dataIndex: "JobStart",
        properties: {
          renderer: Ext.util.Format.dateRenderer("Y-m-d H:i:s"),
        },
      },
      "Job End": {
        dataIndex: "JobEnd",
        properties: {
          renderer: Ext.util.Format.dateRenderer("Y-m-d H:i:s"),
        },
      },
      "Worker Node": {
        dataIndex: "WorkerNode",
        properties: {
          hidden: true,
        },
      },
      "File Type": {
        dataIndex: "FileType",
        properties: {
          hidden: true,
        },
      },
      "Event Type Id": {
        dataIndex: "EvtTypeId",
        properties: {
          hidden: true,
        },
      },
      "Data Quality": {
        dataIndex: "DataqualityFlag",
        properties: {
          hidden: true,
        },
      },
      Tck: {
        dataIndex: "TCK",
        properties: {
          hidden: false,
          filter: "list",
        },
      },
    };

    // BookkeepingPath

    me.bBar = {};
    me.bBar.addButton = Ext.create("Ext.button.Button", {
      handler: function () {
        var text = me.bBar.BKPath.getRawValue();
        me.addBookmark(text);
      },
      iconCls: "dirac-icon-plus",
      minWidth: "20",
      tooltip: "Add the path in the left text field to your bookmarks",
    });
    me.bBar.BKPath = new Ext.form.TextField({
      allowBlank: false,
      enableKeyEvents: true,
      flex: 1,
    });

    var handleExpand = function () {
      var value = me.bBar.BKPath.getValue();
      if (value.search(":/") < 0) value = "sim+std:/" + value;
      var serialisedPaths = me.__prepareExpandPath(value);
      me.expandPath(serialisedPaths);
    };
    me.bBar.BKPath.on("keypress", function (object, e) {
      var keyCode = e.getKey();
      if (keyCode == e.ENTER) {
        handleExpand();
      }
    });

    me.bBar.goButton = Ext.create("Ext.button.Button", {
      iconCls: "bk-icon-go",
      handler: function () {
        handleExpand();
      },
      tooltip: "Loading the demanded location could take time",
      text: "Go",
      minWidth: 50,
    });
    // end
    me.bBar.btoolbar = Ext.create("Ext.toolbar.Toolbar", {
      items: [me.bBar.addButton, me.bBar.BKPath, me.bBar.goButton],
    });

    var menuitems = {
      Visible: [
        {
          text: "JobInfo",
          handler: me.getJobInfo,
          properties: {
            tooltip: "Get information about the job that produced this LFN",
          },
        },
        {
          text: "-",
        }, // separator
        {
          text: "GetAncestors",
          handler: me.getAncestors,
          properties: {
            tooltip: "Click to show the attributtes of the selected job.",
          },
        },
        {
          text: "Logging information",
          handler: me.getLoggingInfo,
          properties: {
            tooltip: "Shows the attributes of the selected job.",
          },
        },
      ],
    };

    me.contextGridMenu = Ext.create("Ext.dirac.utils.DiracApplicationContextMenu", {
      menu: menuitems,
      scope: me,
    });

    me.grid = Ext.create("Ext.dirac.utils.DiracGridPanel", {
      oColumns: oColumns,
      tbar: pagingToolbar,
      bbar: me.bBar.btoolbar,
      pagingToolbar: pagingToolbar,
      store: me.dataStore,
      scope: me,
      stateful: true,
      stateId: "bk-datagrid",
      contextMenu: me.contextGridMenu,
      plugins: "gridfilters",
    });

    me.selectionSet = Ext.create("Ext.form.FieldSet", {
      xtype: "fieldset",
      labelAlign: "top",
      autoHeight: true,
      columnWidth: 0.5,
      defaultType: "textfield",
      items: [
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "Configuration Name",
          name: "cName",
          readOnly: true,
          flex: 1,
        },
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "Configuration Version",
          name: "cVersion",
          readOnly: true,
        },
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "Simulation/DataTaking Conditions",
          name: "conditions",
          readOnly: true,
        },
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "Processing pass",
          name: "procpass",
          readOnly: true,
        },
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "Event Type",
          name: "etype",
          readOnly: true,
        },
        {
          anchor: "90%",
          labelAlign: "top",
          fieldLabel: "FileType",
          name: "ftype",
          readOnly: true,
        },
      ],
    });

    me.statisticsSet = Ext.create("Ext.form.FieldSet", {
      xtype: "fieldset",
      autoHeight: true,
      defaultType: "textfield",
      items: [
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "Number Of Files",
          name: "nbfiles",
          readOnly: true,
        },
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "Number Of Events",
          name: "nbevents",
          readOnly: true,
        },
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "Luminosity",
          name: "luminosity",
          readOnly: true,
        },
        {
          labelAlign: "top",
          anchor: "90%",
          fieldLabel: "File(s) Size",
          name: "fsize",
          readOnly: true,
        },
      ],
    });

    me.infoPanel = Ext.create("Ext.panel.Panel", {
      title: "Statistics:",
      region: "east",
      scrollable: true,
      collapsible: true,
      split: true,
      margins: "2 0 2 0",
      cmargins: "2 2 2 2",
      bodyStyle: "padding: 5px",
      width: 200,
      labelAlign: "top",
      minWidth: 200,
      items: [me.selectionSet, me.statisticsSet],
    });

    var saveToolbar = new Ext.create("Ext.toolbar.Toolbar", {
      dock: "bottom",
      layout: {
        pack: "center",
      },
      items: [
        {
          iconCls: "dirac-icon-save",
          xtype: "button",
          text: "Save",
          handler: function () {
            if (me.grid.getStore().getCount() > 0) {
              var saveform = Ext.create("LHCbDIRAC.BookkeepingBrowser.classes.SaveForm", {
                scope: me,
                bkQuery: me.bkQuery,
              });
              saveform.show();
            } else {
              GLOBAL.APP.CF.alert("No files are selected...", "info");
            }
          },
        },
      ],
    });
    me.bBar.BKPath.setRawValue(me.prefix);
    me.infoPanel.addDocked(saveToolbar);
    me.add([me.leftPanel, me.grid, me.infoPanel]);
  },
  __refreshTree: function () {
    var me = this;
    me.treePanel.store.load();
  },
  __getSelectedData: function () {
    var me = this;
    var oDataQualityStore = me.dataQuality.getStore();
    var qualities = {};
    for (var i = 0; i < oDataQualityStore.count(); i++) {
      var record = oDataQualityStore.getAt(i);
      qualities[record.data.name] = record.data.value;
    }
    var filters = [];

    // The actual record filters are placed on the Store.
    me.grid
      .getStore()
      .getFilters()
      .each(function (filter) {
        var values = filter.getValue();
        for (var i = 0; i < values.length; i++) {
          filters.push(values[i]);
        }
      });

    var extraParams = {
      type: me.advButton.inputValue,
      tree: me.oMenuButton.value,
      dataQuality: Ext.JSON.encode(qualities),
      TCK: filters,
    };
    return extraParams;
  },
  __pageRowNumber: function (ds, rowIndex) {
    var i = 0;
    try {
      i = ds.lastOptions.params.start;
    } catch (e) {}
    if (isNaN(i)) {
      i = 0;
    }
    return rowIndex + i + 1;
  },
  __oprUnsetPathAsExpanded: function (sPath) {
    var me = this;
    var oParts = sPath.split("/");

    // The first element is always empty
    var oTemp = me.expansionState;
    var oStartIndex = 0;

    if (sPath == "/") oStartIndex = 1;

    for (var i = oStartIndex; i < oParts.length; i++) {
      if (oParts[i] in oTemp) {
        if (i == oParts.length - 1) {
          delete oTemp[oParts[i]];
        } else {
          oTemp = oTemp[oParts[i]];
        }
      }
    }
  },

  __oprPathAsExpanded: function (sPath, bInsertIntoStructure) {
    var me = this;
    var oParts = sPath.split("/");

    // The first element is always empty
    var oTemp = me.expansionState;
    var oFound = true;

    var oStartIndex = 0;

    if (sPath == "/") oStartIndex = 1;

    for (var i = oStartIndex; i < oParts.length; i++) {
      if (oParts[i] in oTemp) {
        oTemp = oTemp[oParts[i]];
      } else {
        oFound = false;

        if (bInsertIntoStructure) {
          oTemp[oParts[i]] = {};
        }

        break;
      }
    }

    return oFound;
  },
  expandPath: function (path, field, separator, callback, scope) {
    var me = this,
      current = me.treeStore.getRootNode(),
      index = 0,
      view = me.treePanel.getView(),
      keys,
      expander;
    field = field || me.treeStore.getRootNode().idProperty;
    separator = separator || "/";
    if (Ext.isEmpty(path)) {
      Ext.callback(callback, scope || me, [false, null]);
      return;
    }
    if (current.get(field) != path[0]) {
      Ext.callback(callback, scope || me, [false, current]);
      return;
    }
    me.treePanel.getSelectionModel().select(current);
    expander = function () {
      if (++index === path.length) {
        Ext.callback(callback, scope || me, [true, current]);
        return;
      }
      var node = current.findChild(field, path[index]);
      // me.treePanel.getSelectionModel().select(node);
      if (!node) {
        if (index > path.length) {
          Ext.callback(callback, scope || me, [false, current]);
          return;
        } else {
          node = me.__findNode(current, path[index], field);
        }
      }
      current = node;
      current.expand(false, expander);
    };
    current.expand(false, expander);
  },
  __findNode: function (node, path, field) {
    var me = this;
    var parentNode = node.parentNode;
    var node = parentNode.findChild(field, path);
    if (node) {
      return node;
    } else {
      return me.__findNode(parentNode, path, field);
    }
  },
  __serializeExpansionAction: function (sPathToLevel, oLevel, oColector) {
    var me = this;
    oColector.push(sPathToLevel.length == 0 ? "/" : sPathToLevel);

    for (var sChild in oLevel) {
      me.__serializeExpansionAction(sPathToLevel + "/" + sChild, oLevel[sChild], oColector);
    }
  },
  __setBkPathTextField: function (path) {
    var me = this;
    var data = me.__getSelectedData();
    var tree = data.tree == "Configuration" ? "sim" : "evt";
    me.prefix = tree + "+" + data.type + ":/";
    me.bBar.BKPath.setRawValue(me.prefix + path);
  },
  addBookmark: function (path) {
    var me = this;
    var addBookmarkForm = Ext.create("LHCbDIRAC.BookkeepingBrowser.classes.BookkeepingAddBookmarks", {
      bkkBrowser: me,
    });
    addBookmarkForm.show();
  },
  __prepareExpandPath: function (value) {
    var me = this;
    var prefix = value.split(":/");
    var tree = prefix[0].split("+")[0] == "sim" ? "Configuration" : "Event type";
    var type = prefix[0].split("+")[1];
    var path = prefix[1];
    if (type == "adv") {
      me.advButton.setValue(true);
    } else {
      me.advButton.setValue(false);
    }

    me.oMenuButton.setText(tree);
    me.oMenuButton.value = tree;

    var paths = path.split("/");
    var serialisedPaths = [];
    var previous = "";
    for (var i = 0; i < paths.length; i++) {
      if (paths[i] == "") {
        serialisedPaths.push("/");
      } else {
        previous += "/" + paths[i];
        serialisedPaths.push(previous);
      }
    }
    return serialisedPaths;
  },
  getJobInfo: function () {
    var me = this;

    var lfn = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "Name");
    me.getContainer().body.mask("Wait ...");
    Ext.Ajax.request({
      url: GLOBAL.BASE_URL + me.applicationName + "/jobinfo",
      method: "POST",
      params: {
        lfn: lfn,
      },
      scope: me,
      failure: function (response) {
        me.getContainer().body.unmask();
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
      success: function (response) {
        me.getContainer().body.unmask();
        var jsonData = Ext.JSON.decode(response.responseText);

        if (jsonData["success"] == "true") {
          me.getContainer().oprPrepareAndShowWindowGrid(
            jsonData["result"],
            "JobInfo for :" + lfn,
            ["name", "value"],
            [
              {
                text: "Name",
                flex: 1,
                sortable: true,
                dataIndex: "name",
              },
              {
                text: "Value",
                flex: 1,
                sortable: true,
                dataIndex: "value",
              },
            ]
          );
        } else {
          GLOBAL.APP.CF.alert(jsonData["error"], "error");
        }
      },
    });
  },
  getAncestors: function () {
    var me = this;
    var lfn = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "Name");
    var fileHistory = Ext.create("LHCbDIRAC.BookkeepingBrowser.classes.FileHistoryPanel", {
      applicationName: me.applicationName,
    });
    fileHistory.loadData(lfn);

    var window = me.getContainer().createChildWindow("Files history " + lfn, false, 900, 500);
    window.add(fileHistory);
    window.show().removeCls("x-unselectable"); // Todo: this can be removed
    // after ext-6.2.0;
    fileHistory.on("closeFileHistory", function () {
      filehistory.current = -1;
      window.close();
    });
  },
  getLoggingInfo: function () {
    var me = this;
    var lfn = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "Name");
    Ext.Ajax.request({
      url: GLOBAL.BASE_URL + me.applicationName + "/logfile",
      params: {
        lfn: lfn,
      },
      scope: me,
      success: function (response) {
        var me = this;
        var response = Ext.JSON.decode(response.responseText);

        if (response["success"] == "true") {
          window.open("http://lhcb-logs.cern.ch/storage" + response["result"], "Log file", "width=400,height=200");
        } else {
          GLOBAL.APP.CF.alert(response["error"], "error");
        }
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
});
