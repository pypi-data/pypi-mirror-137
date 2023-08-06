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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.ProductionRequestManager", {
  extend: "Ext.dirac.core.Module",

  requires: [
    "Ext.panel.Panel",
    "Ext.form.field.Date",
    "Ext.grid.plugin.RowExpander",
    "Ext.dirac.utils.DiracBaseSelector",
    "Ext.dirac.utils.DiracAjaxProxy",
    "Ext.dirac.utils.DiracJsonStore",
    "Ext.dirac.utils.DiracGridPanel",
    "Ext.dirac.utils.DiracPagingToolbar",
    "Ext.dirac.utils.DiracApplicationContextMenu",
    "Ext.dirac.utils.DiracRowExpander",
    "LHCbDIRAC.ProductionRequestManager.classes.ProductionRequestEditor",
    "LHCbDIRAC.ProductionRequestManager.classes.RequestModelWindow",
    "LHCbDIRAC.ProductionRequestManager.classes.Tester",
    "LHCbDIRAC.ProductionRequestManager.classes.SubRequestAdder",
    "LHCbDIRAC.ProductionRequestManager.classes.SubRequestEditor",
    "LHCbDIRAC.ProductionRequestManager.classes.RequestSpliter",
    "LHCbDIRAC.ProductionRequestManager.classes.ProductionManager",
    "LHCbDIRAC.ProductionRequestManager.classes.RequestPriorityEditor",
  ],

  applicationsToOpen: {
    LHCbTransformationMonitor: "LHCbDIRAC.LHCbTransformationMonitor.classes.LHCbTransformationMonitor",
  },
  loadState: function (data) {
    var me = this;
    me.grid.loadState(data);
    me.leftPanel.loadState(data);
    if (data.leftPanelCollapsed) {
      me.leftPanel.collapse();
    }
  },

  getStateData: function () {
    var me = this;
    var oReturn = {
      leftMenu: me.leftPanel.getStateData(),
      grid: me.grid.getStateData(),
      leftPanelCollapsed: me.leftPanel.collapsed,
    };
    return oReturn;
  },

  dataFields: [],
  tplSimMarkup: [
    "<b>ID:</b> {ID}<br/>",
    "<b>Name:</b> {reqName}<br/>",
    "<b>Type:</b> {reqType}<br/>",
    "<b>State:</b> {reqState}<br/>",
    "<b>Priority:</b> {reqPrio}<br/>",
    "<b>Author:</b> {reqAuthor} <b>WG:</b> {reqWG}<br/>",
    "<b>Event type:</b> {eventType} {eventText}<br/>",
    "<b>Number of events:</b> {eventNumber}<br/>",
    "<b>Starting Date:</b> {StartingDate}<br/>",
    "<b>Finalization Date:</b> {FinalizationDate}<br/>",
    "<b>Fast Simulation Type:</b> {FastSimulationType}<br/>",
    "<b>Retention Rate:</b> {RetentionRate}<br/>",
    "{htmlTestState}",
    "<br>",
    "<b>Simulation Conditions:</b> {simDesc}<br/>",
    "<b>Beam:</b> {BeamCond} ",
    "<b>Beam energy:</b> {BeamEnergy} ",
    "<b>Generator:</b> {Generator} ",
    "<b>G4 settings:</b> {G4settings}<br/>",
    "<b>Magnetic field:</b> {MagneticField} ",
    "<b>Detector:</b> {DetectorCond} ",
    "<b>Luminosity:</b> {Luminosity}<br/><br/>",
    "<b>Processing Pass:</b> {pDsc}<br/>",
    "<b>MC Version:</b> {mcConfigVersion}<br/>",
    "{p1Html}{p2Html}{p3Html}{p4Html}",
    "{p5Html}{p6Html}{p7Html}{p8Html}{p9Html}",
    "{p10Html}{p11Html}{p12Html}{p13Html}{p14Html}",
    "{p15Html}{p16Html}{p17Html}{p18Html}{p19Html}<br/>",
    "<b>Inform also:</b> {reqInform}<br/><br/>",
    "<b>Comments</b><br/> {htmlReqComment}<br/>",
  ],

  tplRunMarkup: [
    "<b>ID:</b> {ID}<br/>",
    "<b>Name:</b> {reqName}<br/>",
    "<b>Type:</b> {reqType}<br/>",
    "<b>State:</b> {reqState}<br/>",
    "<b>Priority:</b> {reqPrio}<br/>",
    "<b>Author:</b> {reqAuthor}<br/>",

    "<b>Event type:</b> {eventType} {eventText}<br/>",
    "<b>Number of events:</b> {eventNumber}<br/><br>",

    "<b>Configuration:</b> {configName} <b>version:</b> {configVersion}<br>",
    "<b>Conditions:</b> {simDesc} <b>type:</b> {condType}<br/>",
    "<b>Processing pass:</b> {inProPass}<br/>",
    "<b>Input file type:</b> {inFileType}<br/>",
    "<b>DQ flag:</b> {inDataQualityFlag}<br/>",
    "<b>Input production:</b> {inProductionID}<br/>",
    "<b>TCKs:</b> {inTCKs}<br/><br/>",

    "<b>Processing Pass:</b> {pDsc}<br/>",
    "{p1Html}{p2Html}{p3Html}{p4Html}",
    "{p5Html}{p6Html}{p7Html}{p8Html}{p9Html}",
    "{p10Html}{p11Html}{p12Html}{p13Html}{p14Html}",
    "{p15Html}{p16Html}{p17Html}{p18Html}{p19Html}<br/>",

    "<b>Inform also:</b> {reqInform}<br/><br/>",
    "<b>Comments</b><br/> {htmlReqComment}<br/>",
  ],
  initComponent: function () {
    var me = this;
    var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

    me.launcher.title = "Production Request manager";
    me.launcher.maximized = false;
    me.launcher.width = oDimensions[0];
    me.launcher.height = oDimensions[1] - GLOBAL.APP.MAIN_VIEW.taskbar ? GLOBAL.APP.MAIN_VIEW.taskbar.getHeight() : 0;
    me.launcher.x = 0;
    me.launcher.y = 0;

    Ext.apply(me, {
      layout: "card",
      bodyBorder: false,
    });
    me.dataFields = [
      {
        name: "IdCheckBox",
        mapping: "ID",
      },
      {
        name: "ID",
        type: "auto",
      },
      {
        name: "reqName",
      },
      {
        name: "reqType",
      },
      {
        name: "reqState",
      },
      {
        name: "reqPrio",
      },
      {
        name: "reqAuthor",
      },
      {
        name: "reqWG",
      },
      {
        name: "simCondID",
      },
      {
        name: "simDesc",
      },
      {
        name: "Generator",
      },
      {
        name: "G4settings",
      },
      {
        name: "MagneticField",
      },
      {
        name: "BeamEnergy",
      },
      {
        name: "Luminosity",
      },
      {
        name: "DetectorCond",
      },
      {
        name: "BeamCond",
      },
      {
        name: "configName",
      },
      {
        name: "configVersion",
      },
      {
        name: "condType",
      },
      {
        name: "inProPass",
      },
      {
        name: "inFileType",
      },
      {
        name: "inProductionID",
      },
      {
        name: "inDataQualityFlag",
      },
      {
        name: "inTCKs",
      },
      {
        name: "pID",
      },
      {
        name: "pDsc",
      },
      {
        name: "pAll",
      },
      {
        name: "eventType",
      },
      {
        name: "eventText",
      },
      {
        name: "eventNumber",
      },
      {
        name: "reqComment",
      },
      {
        name: "reqDesc",
      },
      {
        name: "reqInform",
      },
      {
        name: "IsModel",
      },
      {
        name: "mcConfigVersion",
      },
      {
        name: "eventBK",
      },
      {
        name: "EventNumberTotal",
      },
      {
        name: "eventBKTotal",
      },
      {
        name: "progress",
        type: "auto",
      },
      {
        name: "creationTime",
        type: "string",
      },
      {
        name: "lastUpdateTime",
        type: "string",
      },
      {
        name: "TestState",
      },
      {
        name: "TestActual",
      },
      {
        name: "_parent",
        type: "auto",
      },
      {
        name: "_is_leaf",
        type: "bool",
      },
      {
        name: "_master",
        type: "auto",
      },
      {
        name: "StartingDate",
        type: "auto",
      },
      {
        name: "FinalizationDate",
        type: "auto",
      },
      {
        name: "RetentionRate",
        type: "auto",
      },
      {
        name: "FastSimulationType",
        type: "auto",
      },
    ];

    for (var i = 1; i < 20; ++i)
      me.dataFields = me.dataFields.concat([
        {
          name: "p" + i + "App",
          type: "auto",
        },
        {
          name: "p" + i + "Ver",
          type: "auto",
        },
        {
          name: "p" + i + "SConf",
          type: "auto",
        },
        {
          name: "p" + i + "mcTCK",
          type: "auto",
        },
        {
          name: "p" + i + "Opt",
          type: "auto",
        },
        {
          name: "p" + i + "OptF",
          type: "auto",
        },
        {
          name: "p" + i + "IsM",
          type: "auto",
        },
        {
          name: "p" + i + "DDDb",
          type: "auto",
        },
        {
          name: "p" + i + "CDb",
          type: "auto",
        },
        {
          name: "p" + i + "DQT",
          type: "auto",
        },
        {
          name: "p" + i + "EP",
          type: "auto",
        },
        {
          name: "p" + i + "TRP",
          type: "auto",
        },
        {
          name: "p" + i + "Html",
          type: "auto",
        },
        {
          name: "p" + i + "Step",
          type: "auto",
        },
        {
          name: "p" + i + "Name",
          type: "auto",
        },
        {
          name: "p" + i + "Pass",
          type: "auto",
        },
        {
          name: "p" + i + "Vis",
          type: "auto",
        },
        {
          name: "p" + i + "Use",
          type: "auto",
        },
        {
          name: "p" + i + "IFT",
          type: "auto",
        },
        {
          name: "p" + i + "OFT",
          type: "auto",
        },
      ]);
    me.callParent(arguments);
  },

  evtRender: function (val) {
    /* For Ext 3.x: return Ext.util.Format.number(val,"0,000,000"); */
    var s = val + "";
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(s)) s = s.replace(rgx, "$1" + "," + "$2");
    return s;
  },
  renderActual: function (val) {
    if (val == "") return "";
    if (val == "0") return "No";
    return "Yes";
  },
  buildUI: function () {
    var me = this;

    /*
     * Left panel
     */
    var selectors = {
      typeF: "Type",
      stateF: "State",
      authorF: "Author",
      wgF: "WG",
    };

    var textFields = {
      idF: {
        name: "Request ID(s)",
        type: "number",
      },
      modF: {
        name: "modF",
        fieldLabel: "Show models only",
        type: "checkbox",
      },
    };

    var properties = [[]];
    var map = [
      ["typeF", "typeF"],
      ["stateF", "stateF"],
      ["authorF", "authorF"],
      ["wgF", "wgF"],
    ];

    me.leftPanel = Ext.create("Ext.dirac.utils.DiracBaseSelector", {
      scope: me,
      cmbSelectors: selectors,
      textFields: textFields,
      hasTimeSearchPanel: false,
      datamap: map,
      url: "ProductionRequestManager/getSelectionData",
      properties: properties,
    });

    var oProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
      url: GLOBAL.BASE_URL + me.applicationName + "/list",
    });

    me.dataStore = Ext.create("Ext.dirac.utils.DiracJsonStore", {
      autoLoad: true,
      proxy: oProxy,
      fields: me.dataFields,
      remoteSort: false,
      scope: me,
      sorters: [
        {
          property: "ID",
          direction: "DESC",
        },
      ],
    });

    var oColumns = {
      checkBox: {
        dataIndex: "IdCheckBox",
      },
      Id: {
        dataIndex: "ID",
        properties: {
          width: 80,
        },
      },
      Type: {
        dataIndex: "reqType",
      },
      State: {
        dataIndex: "reqState",
      },
      Priority: {
        dataIndex: "reqPrio",
        properties: {
          width: 50,
        },
      },
      Name: {
        dataIndex: "reqName",
        id: "Name",
      },
      StartingDate: {
        dataIndex: "StartingDate",
      },
      FinalizationDate: {
        dataIndex: "FinalizationDate",
      },
      RetentionRate: {
        dataIndex: "RetentionRate",
      },
      FastSimulationType: {
        dataIndex: "FastSimulationType",
      },
      "Sim/Run conditions": {
        dataIndex: "simDesc",
        properties: {
          width: 200,
        },
      },
      "Proc. pass": {
        dataIndex: "pDsc",
        properties: {
          width: 200,
        },
      },
      "Event type": {
        dataIndex: "eventType",
      },
      "Events requested": {
        dataIndex: "EventNumberTotal",
        renderer: me.evtRender,
      },
      "Events in BK": {
        dataIndex: "eventBKTotal",
        renderer: me.evtRender,
      },
      "Progress (%)": {
        dataIndex: "progress",
        properties: {
          align: "right",
        },
      },
      "Created at": {
        dataIndex: "creationTime",
        properties: {
          hidden: true,
        },
      },
      "Last state update": {
        dataIndex: "lastUpdateTime",
        properties: {
          hidden: true,
        },
      },
      Author: {
        dataIndex: "reqAuthor",
        properties: {
          hidden: true,
        },
      },
      WG: {
        dataIndex: "reqWG",
        properties: {
          hidden: true,
        },
      },
      "Event type name": {
        dataIndex: "eventText",
        properties: {
          hidden: true,
        },
      },
      Test: {
        dataIndex: "TestState",
        properties: {
          hidden: true,
        },
      },
      "Test is actual": {
        dataIndex: "TestActual",
        properties: {
          hidden: true,
        },
        renderer: me.renderActual,
      },
    };

    var bulkMenu = Ext.create("Ext.menu.Menu", {
      scope: me,
      items: [
        {
          text: "Sign as " + GLOBAL.USER_CREDENTIALS.group,
          handler: me.__bulkSign,
          scope: me,
        },
        {
          text: "Activate as " + GLOBAL.USER_CREDENTIALS.group,
          handler: me.__bulkActivate,
          scope: me,
        },
        {
          text: "Move to Accepted as " + GLOBAL.USER_CREDENTIALS.group,
          handler: me.__bulkAccepted,
          scope: me,
        },
        {
          text: "Change priority as " + GLOBAL.USER_CREDENTIALS.group,
          handler: me.__bulkPriority,
          scope: me,
        },
        {
          text: "Submit",
          handler: me.__submit,
          scope: me,
        },
      ],
    });

    var toolButtons = {
      Visible: [
        {
          text: "Bulk",
          menu: bulkMenu, // assign menu by instance
          iconCls: "dirac-icon-submit",
          value: "bulkSign",
        },
      ],
      Protected: [
        {
          text: "New Request",
          handler: me.__newRequest,
          properties: {
            tooltip: "Create a new request",
            iconCls: "dirac-icon-plus",
          },
          property: "NormalUser",
        },
      ],
    };

    me.pagingToolbar = Ext.create("Ext.dirac.utils.DiracPagingToolbar", {
      toolButtons: toolButtons,
      store: me.dataStore,
      scope: me,
    });

    // var expanderTplBody = ['<b>Author:</b> {reqAuthor}<br/>',
    // '<b>Beam:</b> {BeamCond} ', '<b>Beam energy:</b> {BeamEnergy} ',
    // '<b>Generator:</b> {Generator} ', '<b>G4 settings:</b> {G4settings}
    // ', '<b>Magnetic field:</b> {MagneticField} ',
    // '<b>Detector:</b> {DetectorCond} ', '<b>Luminosity:</b> {Luminosity}
    // <b>EventType:</b> {eventText} <br/>', '<b>Steps:</b> {pAll} ',
    // '{htmlTestState}'];

    me.contextMenu = Ext.create("Ext.menu.Menu", {
      items: [
        {
          text: "View",
          scope: me,
          handler: me.__viewRequest,
          properties: {
            tooltip: "Click to view the selected request.",
          },
        },
        {
          text: "History",
          scope: me,
          handler: me.__history,
          properties: {
            tooltip: "Show the history of the selected request",
          },
        },
        {
          xtype: "menuseparator",
        },
        {
          text: "Edit",
          scope: me,
          value: "edit",
          handler: me.__edit,
          properties: {
            tooltip: "Edit request",
          },
        },
        /*
         * { "text" : "Test", scope : me, value : "test", "handler" :
         * me.__test, "properties" : { tooltip : "Test request" } },
         */ {
          text: "Sign",
          scope: me,
          value: "sign",
          handler: me.__sign,
          properties: {
            tooltip: "Test request",
          },
        },
        {
          text: "Resurrect",
          scope: me,
          value: "resurrect",
          handler: me.__resurrect,
          properties: {
            tooltip: "Resurrect request",
          },
        },
        {
          text: "Reactivate",
          scope: me,
          value: "reactivate",
          handler: me.__reactivate,
          properties: {
            tooltip: "Resurrect request",
          },
        },
        {
          text: "Confirm",
          scope: me,
          value: "confirm",
          handler: me.__confirm,
          properties: {
            tooltip: "Confirm request",
          },
        },
        {
          text: "Duplicate",
          scope: me,
          handler: me.__duplicate,
          properties: {
            tooltip: "Duplicate request",
          },
        },
        {
          text: "Delete",
          handler: me.__delete,
          scope: me,
          properties: {
            tooltip: "Delete request",
          },
        },
        {
          xtype: "menuseparator",
        },
        {
          text: "Add subrequest",
          handler: me.__addsubrequest,
          scope: me,
          properties: {
            tooltip: "Add subrequest",
          },
        },
        {
          text: "Split",
          handler: me.__split,
          scope: me,
          properties: {
            tooltip: "Split request",
          },
        },
        {
          text: "Remove subrequests",
          handler: me.__removesubrequests,
          scope: me,
          properties: {
            tooltip: "Remove subrequests",
          },
        },
        {
          text: "Productions",
          handler: me.__productions,
          scope: me,
          properties: {
            tooltip: "Show productions",
          },
        },
        {
          text: "Transformation monitor",
          handler: me.__transformations,
          scope: me,
          properties: {
            tooltip: "Open Transformation monitor",
          },
        },
        {
          xtype: "menuseparator",
        },
        {
          text: "Remove from models",
          handler: me.__model,
          scope: me,
          properties: {
            tooltip: "Remove from models",
          },
        },
        {
          text: "Mark as model",
          handler: me.__model,
          scope: me,
          properties: {
            tooltip: "Make as model",
          },
        },
      ],
    });

    me.showGridContextMenu = true;
    me.grid = Ext.create("Ext.dirac.utils.DiracGridPanel", {
      store: me.dataStore,
      oColumns: oColumns,
      pagingToolbar: me.pagingToolbar,
      scope: me,
      region: "center",
      plugins: [
        {
          boolValue: {
            _is_leaf: false,
          },
          ptype: "diracrowexpander",
          rowBodyTpl: ['<div id="expanded-Grid-{ID}"> </div>'],
        },
      ],
      listeners: {
        beforecellcontextmenu: function (oTable, td, cellIndex, record, tr, rowIndex, e, eOpts) {
          e.preventDefault();
          if (!me.showGridContextMenu) {
            me.showGridContextMenu = true;
            return false;
          }
          me.__setupContextMenu(record);
          me.contextMenu.showAt(e.getXY());
          return false;
        },
      },
    });

    me.grid.view.on("expandbody", function (rowNode, record, expandbody) {
      var targetId = "expanded-Grid-" + record.get("ID");
      var isExpanded = false;
      if (Ext.getCmp(targetId + "_grid") != null) {
        Ext.destroy(Ext.getCmp(targetId + "_grid"));
        isExpanded = me.grid.expandedGridPanel.isExpanded;
      }
      if (Ext.getCmp(targetId + "_grid") == null) {
        var params = {
          anode: Ext.JSON.encode([record.data.ID]),
          sort: Ext.encode([
            {
              property: "ID",
              direction: "DESC",
            },
          ]),
        };
        var oProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
          url: GLOBAL.BASE_URL + me.applicationName + "/list",
        });
        oProxy.extraParams = params;
        var expandStore = Ext.create("Ext.dirac.utils.DiracJsonStore", {
          proxy: oProxy,
          fields: me.dataFields,
          dontLoadOnCreation: true,
          scope: me,
          autoLoad: true,
          sorters: [
            {
              property: "ID",
              direction: "DESC",
            },
          ],
        });
        expandStore.on("load", function () {
          me.grid.expandedGridPanel.setLoading(false);
        });
        me.grid.expandedGridPanel = Ext.create("Ext.grid.Panel", {
          // forceFit : true,
          renderTo: targetId,
          isExpanded: isExpanded,
          id: targetId + "_grid",
          store: expandStore,
          viewConfig: {
            stripeRows: true,
            enableTextSelection: true,
          },
          columns: [
            {
              header: "Id",
              sortable: true,
              dataIndex: "ID",
              width: 60,
            },
            {
              header: "Type",
              sortable: true,
              dataIndex: "reqType",
            },
            {
              header: "State",
              sortable: true,
              dataIndex: "reqState",
            },
            {
              header: "Priority",
              sortable: true,
              dataIndex: "reqPrio",
              width: 50,
            },
            {
              header: "Name",
              sortable: true,
              dataIndex: "reqName",
            },
            {
              header: "Sim/Run conditions",
              sortable: true,
              dataIndex: "simDesc",
              width: 200,
            },
            {
              header: "Proc. pass",
              sortable: true,
              dataIndex: "pDsc",
              width: 200,
            },
            {
              header: "Event type",
              sortable: true,
              dataIndex: "eventType",
            },
            {
              header: "Events requested",
              dataIndex: "EventNumberTotal",
              renderer: me.evtRender,
              align: "right",
            },
            {
              header: "Events in BK",
              dataIndex: "eventBKTotal",
              renderer: me.evtRender,
              align: "right",
            },
            {
              header: "Progress (%)",
              dataIndex: "progress",
              align: "right",
            },
            {
              header: "Created at",
              sortable: true,
              dataIndex: "creationTime",
              hidden: true,
            },
            {
              header: "Last state update",
              sortable: true,
              dataIndex: "lastUpdateTime",
              hidden: true,
            },
            {
              header: "Author",
              dataIndex: "reqAuthor",
              hidden: true,
              sortable: true,
            },
            {
              header: "WG",
              dataIndex: "reqWG",
              hidden: true,
              sortable: true,
            },
            {
              header: "Event type name",
              dataIndex: "eventText",
              hidden: true,
            },
            {
              header: "Test",
              dataIndex: "TestState",
              hidden: true,
            },
            {
              header: "Test is actual",
              dataIndex: "TestActual",
              hidden: true,
              renderer: me.renderActual,
            },
          ],
          plugins: [
            {
              ptype: "rowexpander",
              rowBodyTpl: ["<b>EventType:</b> {eventType}<br/>", "<b>Description:</b> {eventText}<br/>", "<b>Test state:</b> {TestState} "],
            },
          ],
          listeners: {
            beforecellcontextmenu: function (table, td, cellIndex, record, tr, rowIndex, e, eOpts) {
              this.isExpanded = true;
              e.preventDefault();
              me.grid.expandedGridPanel = this;
              if (me.contextMenu) {
                var store = me.grid.getStore();
                var originalRequest = store.getAt(
                  store.findBy(function (value, key) {
                    var data = value.getData();
                    if (data.ID == record.data._parent) {
                      return true;
                    }
                    return false;
                  })
                );
                me.showGridContextMenu = false;
                me.__setupContextMenu(originalRequest);
                me.contextMenu.showAt(e.getXY());
              }
              return false;
            },
          },
        });

        rowNode.grid = me.grid.expandedGridPanel;
        me.grid.expandedGridPanel.setLoading("Loading data ...");
        me.grid.expandedGridPanel.getStore().load();
        me.grid.expandedGridPanel.getEl().swallowEvent(["mouseover", "mousedown", "click", "dblclick", "onRowFocus"]);
        me.grid.expandedGridPanel.fireEvent("bind", me.grid.expandedGridPanel, {
          id: record.get("ID"),
        });
      } else {
        me.grid.expandedGridPanel.getStore().reload();
      }
    });

    me.leftPanel.setGrid(me.grid);

    me.browserPanel = new Ext.create("Ext.panel.Panel", {
      layout: "border",
      defaults: {
        collapsible: true,
        split: true,
      },
      items: [me.leftPanel, me.grid],
    });

    me.editPanel = new Ext.create("LHCbDIRAC.ProductionRequestManager.classes.ProductionRequestEditor", {
      requestManager: me,
    });
    me.editPanel.on("saved", me.__onEditorSave, me);
    me.editPanel.on("cancelled", me.__onEditorCancel, me);

    me.subRequestEditor = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.SubRequestEditor", {
      title: "Edit",
      closable: true,
    });

    me.subRequestEditor.on("saved", me.reloadGrid, me);
    me.subRequestEditor.on("Cancelled", me.__onEditorCancel, me);
    me.subRequestEditor.on("close", me.__onEditorCancel, me);

    me.add([me.browserPanel, me.editPanel, me.subRequestEditor]);
  },
  __setupContextMenu: function (record) {
    var me = this;
    me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "confirm")).hide();
    me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "reactivate")).hide();
    me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "resurrect")).hide();
    me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "edit")).hide();
    // me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value",
    // "test")).hide();
    me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "sign")).hide();

    // me.pagingToolbar.items.getAt(me.pagingToolbar.items.findIndex("value",
    // "bulkSign")).hide();

    if (
      (record.get("reqState") == "New" && record.get("reqAuthor") == GLOBAL.USER_CREDENTIALS.username) ||
      Ext.Array.contains(["diracAdmin", "lhcb_admin"], GLOBAL.USER_CREDENTIALS.group) ||
      (record.get("IsModel") && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech")
    ) {
      me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "edit")).show();
      /*
       * if (record.get("reqType") == "Simulation") {
       * me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value",
       * "test")).show(); } else {
       * me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value",
       * "test")).hide(); }
       */
    } else if (
      (record.get("reqState") == "BK Check" && GLOBAL.USER_CREDENTIALS.group == "lhcb_bk") ||
      (record.get("reqState") == "Submitted" && GLOBAL.USER_CREDENTIALS.group == "lhcb_ppg") ||
      (record.get("reqState") == "Submitted" && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") ||
      (record.get("reqState") == "On-hold" && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") ||
      (record.get("reqState") == "Tech OK" && GLOBAL.USER_CREDENTIALS.group == "lhcb_ppg") ||
      (record.get("reqState") == "PPG OK" && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech")
    ) {
      me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "edit")).show();
      /*
       * if (record.get("reqType") == "Simulation") {
       * me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value",
       * "test")).show(); } else {
       * me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value",
       * "test")).hide(); }
       */
    } else if (
      (record.get("reqState") == "Accepted" || record.get("reqState") == "Active" || record.get("reqState") == "Completed") &&
      GLOBAL.USER_CREDENTIALS.group == "lhcb_prmgr"
    ) {
      me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "edit")).show();
      /*
       * if (record.get("reqType") == "Simulation") {
       * me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value",
       * "test")).show(); } else {
       * me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value",
       * "test")).hide(); }
       */
    } else if (record.get("reqState") == "Rejected" && record.get("reqAuthor") == GLOBAL.USER_CREDENTIALS.username) {
      me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "resurrect")).show();
    } else if (
      (record.get("reqState") == "Done" || record.get("reqState") == "Cancelled") &&
      Ext.Array.contains(["diracAdmin", "lhcb_admin"], GLOBAL.USER_CREDENTIALS.group)
    ) {
      me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "reactivate")).show();
    } else if (record.get("reqState") == "BK OK" && record.get("reqAuthor") == GLOBAL.USER_CREDENTIALS.username) {
      me.contextMenu.items.getAt(me.contextMenu.items.findIndex("value", "confirm")).show();
    }
    for (var i = 0; i < me.contextMenu.items.length; i++) {
      var menuitem = me.contextMenu.items.getAt(i);
      switch (menuitem.text) {
        case "Delete":
          if (
            ((record.get("reqState") == "New" || record.get("reqState") == "Rejected") &&
              record.get("reqAuthor") == GLOBAL.USER_CREDENTIALS.username) ||
            Ext.Array.contains(["diracAdmin", "lhcb_admin"], GLOBAL.USER_CREDENTIALS.group) ||
            (record.get("IsModel") && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech")
          ) {
            menuitem.enable();
          } else {
            menuitem.disable();
          }
          break;
        case "Add subrequest":
          if (
            record.get("reqState") == "New" &&
            !record.get("_master") &&
            record.get("reqType") == "Simulation" &&
            (record.get("reqAuthor") == GLOBAL.USER_CREDENTIALS.username || (record.get("IsModel") && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech"))
          ) {
            menuitem.show();
          } else {
            menuitem.hide();
          }
          break;
        case "Split":
          if (
            !record.get("_master") &&
            !record.get("_is_leaf") &&
            (Ext.Array.contains(["diracAdmin", "lhcb_admin"], GLOBAL.USER_CREDENTIALS.group) ||
              ((record.get("reqState") == "Submitted" || record.get("reqState") == "PPG OK" || record.get("reqState") == "On-hold") &&
                GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") ||
              ((record.get("reqState") == "Accepted" || record.get("reqState") == "Active" || record.get("reqState") == "Completed") &&
                GLOBAL.USER_CREDENTIALS.group == "lhcb_prmgr"))
          ) {
            menuitem.show();
          } else {
            menuitem.hide();
          }
          break;
        case "Remove subrequests":
          if (
            record.get("reqState") == "New" &&
            !record.get("_master") &&
            !record.get("_is_leaf") &&
            record.get("reqType") == "Simulation" &&
            record.get("reqAuthor") == GLOBAL.USER_CREDENTIALS.username
          ) {
            menuitem.show();
          } else {
            menuitem.hide();
          }
          break;
        case "Productions":
          if (
            record.get("reqState") == "Active" ||
            record.get("reqState") == "Completed" ||
            record.get("reqState") == "Accepted" ||
            record.get("reqState") == "Done" ||
            record.get("reqState") == "Cancelled"
          ) {
            menuitem.show();
          } else {
            menuitem.hide();
          }
          break;
        case "Transformation monitor":
          if (
            record.get("reqState") == "Active" ||
            record.get("reqState") == "Completed" ||
            record.get("reqState") == "Accepted" ||
            record.get("reqState") == "Done" ||
            record.get("reqState") == "Cancelled"
          ) {
            menuitem.show();
          } else {
            menuitem.hide();
          }
          break;
        case "Remove from models":
          menuitem.hide();
          if (GLOBAL.USER_CREDENTIALS.group == "lhcb_tech" && !record.get("_master")) {
            if (record.get("IsModel")) {
              menuitem.show();
            }
          }
          break;
        case "Mark as model":
          menuitem.hide();
          if (GLOBAL.USER_CREDENTIALS.group == "lhcb_tech" && !record.get("_master")) {
            menuitem.hide();
            if (!record.get("IsModel")) {
              menuitem.show();
            }
          }
          break;
      }
    }
  },
  __onEditorCancel: function () {
    var me = this;

    me.getLayout().setActiveItem(0);
  },

  __onEditorSave: function () {
    var me = this;

    me.getLayout().setActiveItem(0);
    me.grid.getStore().reload();
  },
  __getSelectedValues: function () {
    var me = this;

    var result = {};

    if (me.grid.expandedGridPanel) {
      if (!me.grid.expandedGridPanel.isExpanded) {
        result = {
          data: GLOBAL.APP.CF.getSelectedRecords(me.grid)[0],
          expData: null,
        };
      } else {
        me.grid.expandedGridPanel.isExpanded = false;
        result = {
          data: GLOBAL.APP.CF.getSelectedRecords(me.grid)[0],
          expData: GLOBAL.APP.CF.getSelectedRecords(me.grid.expandedGridPanel)[0],
        };
      }
    } else {
      result = {
        data: GLOBAL.APP.CF.getSelectedRecords(me.grid)[0],
        expData: null,
      };
    }
    return result;
  },

  __viewRequest: function () {
    var me = this;

    var result = me.__getSelectedValues();
    var id = result["data"].get("ID");
    if (result["expData"] != null) {
      id = result["expData"].get("ID");
    }

    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + me.applicationName + "/list",
      method: "POST",
      params: {
        idF: Ext.JSON.encode([id.toString()]), // Ext.JSON.encode([result["data"].get("ID").toString()]),
        sort: Ext.encode([
          {
            property: "ID",
            direction: "DESC",
          },
        ]),
      },
      scope: me,
      success: function (response) {
        me.getContainer().body.unmask();
        var jsonData = Ext.JSON.decode(response.responseText);
        if (jsonData["OK"] == true) {
          var data = jsonData["result"][0];
          var title = "Request";
          if (result["expData"] != null) {
            title = "SubRequest";
            data["htmlTestState"] = "<b>Test state:</b> " + result["expData"].get("TestState") + "<br/>";
            data["eventType"] = result["expData"].get("eventType");
            data["eventText"] = result["expData"].get("eventText");

            data["eventNumber"] = result["expData"].get("eventNumber");
            if (result["expData"].get("reqComment")) {
              var comment = result["expData"].get("reqComment") + "\n" + data["reqComment"];
              data["reqComment"] = comment;
            }
            data["ID"] = result["expData"].get("ID");
          }
          var eol = /\n/g;

          data.htmlReqComment = data.reqComment.replace(eol, "<br/>");

          if (data["reqType"] == "Simulation") {
            me.getContainer().oprPrepareAndShowWindowTpl(me.tplSimMarkup, data, title + " :" + data["ID"]);
          } else {
            me.getContainer().oprPrepareAndShowWindowTpl(me.tplRunMarkup, data, title + " :" + data["ID"]);
          }
        } else {
          GLOBAL.APP.CF.alert(jsonData["error"], "Error");
        }
      },
    });
  },
  __history: function () {
    var me = this;

    var result = me.__getSelectedValues();
    var id = result["data"].get("ID");
    if (result["expData"] != null) {
      id = result["expData"].get("ID");
    }
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + me.applicationName + "/history",
      method: "POST",
      params: {
        RequestID: Ext.JSON.encode(id),
      },
      scope: me,
      success: function (response) {
        me.getContainer().body.unmask();
        var jsonData = Ext.JSON.decode(response.responseText);
        if (jsonData["success"] == "true") {
          me.getContainer().oprPrepareAndShowWindowGrid(
            jsonData["result"],
            "History for request " + id,
            ["TimeStamp", "RequestState", "RequestUser"],
            [
              {
                text: "Time",
                flex: 1,
                sortable: false,
                dataIndex: "TimeStamp",
              },
              {
                text: "State",
                flex: 1,
                sortable: false,
                dataIndex: "RequestState",
              },
              {
                text: "Changed by",
                flex: 1,
                sortable: false,
                dataIndex: "RequestUser",
              },
            ]
          );
        } else {
          GLOBAL.APP.CF.alert(jsonData["error"], "Error");
        }
      },
    });
  },
  __duplicate: function () {
    var me = this;
    var result = me.__getSelectedValues();
    if (result["expData"] != null) {
      GLOBAL.APP.CF.alert("Can not duplicate subrequest of request in progress", "error");
    } else {
      if (result["data"].get("_master")) {
        me.__realDuplicate(result["data"], false);
        return;
      }
      Ext.Msg.show({
        title: "Question",
        msg: "Clear the processing pass in the copy?",
        buttons: Ext.Msg.YESNOCANCEL,
        fn: function (btn) {
          if (btn == "yes") me.__realDuplicate(result["data"], true);
          if (btn == "no") me.__checkAndDuplicate(result["data"]);
        },
        scope: me,
        icon: Ext.MessageBox.QUESTION,
      });
    }
  },
  __realDuplicate: function (r, clearpp) {
    var me = this;
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + me.applicationName + "/duplicate",
      method: "GET",
      params: {
        ID: r.data.ID,
        ClearPP: clearpp,
      },
      scope: me,
      success: function (response) {
        if (response) {
          var jsonData = Ext.JSON.decode(response.responseText);
          if (jsonData.OK) {
            Ext.MessageBox.show({
              title: "Request was successfully duplicated",
              msg: "New Request ID: " + jsonData.Value,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.INFO,
            });
          } else {
            Ext.MessageBox.show({
              title: "Duplicate has failed",
              msg: jsonData.Message,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
          }
        }
        me.grid.getStore().load();
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  __checkAndDuplicate: function (r) {
    var me = this;
    var steps = [];
    var n = 1;
    var data = r.getData();
    while ("p" + n + "Step" in data && data["p" + n + "Step"]) {
      steps.push(data["p" + n + "Step"]);
      ++n;
    }
    if (!steps.length) {
      me.__realDuplicate(r, false);
      return;
    }
    me.DupRec = r;
    me.DupSteps = steps;
    for (n = 0; n < steps.length; ++n) {
      me.ConAdvRequest(
        "step",
        GLOBAL.BASE_URL + "LHCbStepManager/getStep",
        {
          StepId: steps[n],
        },
        me,
        me.__onDupStepLoaded,
        me.__onDupStepFailed
      );
    }
  },
  __delete: function () {
    var me = this;
    var result = me.__getSelectedValues();
    if (!result["data"]) {
      Ext.dirac.system_info.msg("Notification", "No row selected.");
    }
    var id = result["data"].get("ID");
    var isExpandedGrid = false;
    if (result["expData"] != null) {
      id = result["expData"].get("ID");
      isExpandedGrid = true;
    }
    Ext.MessageBox.confirm(
      "Message",
      "Do you really want to delete Request " + id + "?",
      function (btn) {
        if (btn == "yes") me.__realDelRequest(id, isExpandedGrid);
      },
      me
    );
  },
  __realDelRequest: function (id, isExpandedGrid) {
    var me = this;
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + me.applicationName + "/delete",
      method: "GET",
      params: {
        ID: id,
      },
      scope: me,
      success: function (response) {
        if (response) {
          var jsonData = Ext.JSON.decode(response.responseText);
          if (jsonData.OK) {
            Ext.dirac.system_info.msg("Notification", "Production Request: " + id + " .<br/> deleted!");
          } else {
            Ext.dirac.system_info.msg("Error Notification", "Failed to delete " + id + " " + jsonData["Message"]);
          }
        }
        if (isExpandedGrid) {
          me.grid.expandedGridPanel.getStore().load();
        } else {
          me.grid.getStore().load();
        }
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  __newRequest: function () {
    var me = this;

    var win = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.RequestModelWindow"); //better to create a new windows

    win.on(
      "create",
      function (type) {
        var id = parseInt(type);
        if (isNaN(id)) me.viewEditor(null, type);
        else
          me.__realDuplicate(
            {
              data: {
                ID: id,
              },
            },
            false
          );
      },
      me
    );
    win.show();
  },
  getMasterStateAndAuthor: function (r) {
    if (r.data)
      return {
        state: r.data.reqState,
        author: r.data.reqAuthor,
        isModel: r.data.IsModel,
      };
    else
      return {
        state: "Unknown",
        author: "Unknown",
      };
  },

  getRecordMeta: function (r) {
    var m = this.getMasterStateAndAuthor(r);
    m.user = GLOBAL.USER_CREDENTIALS.username;
    m.group = GLOBAL.USER_CREDENTIALS.group;
    return m;
  },
  viewEditor: function (r, type) {
    var me = this;

    if (r && r.expData && r.expData.getData()._master) {
      //If the request has a sub-recuest the _master should be not an empty string
      me.editSubRequest(r.expData);
      return;
    }
    var data = {};
    data.title = "New request";
    data.state = "New";
    data.isModel = false;
    data.type = type;
    var meta = null;
    if (r && r.data) data.type = r.data.get("reqType");
    if (r && r.data && r.data.get("ID")) {
      data.title = "Edit request " + r.data.get("ID");
      data.state = r.data.get("reqState");
      meta = me.getRecordMeta(r.data);
      data.isModel = meta.isModel;
    }

    me.editPanel.getForm().reset();
    me.editPanel.removeProcessingPasses();
    me.editPanel.data = data;
    me.editPanel.setupEditor(data);
    if (r) {
      me.editPanel.loadRecord(meta, r.data);
    }

    if (r && r.data.get("ID")) {
      me.editPanel.Request.setTitle("Request (" + r.data.get("ID") + ")");
      me.editPanel.rID = r.data.get("ID");
    } else {
      me.editPanel.Request.setTitle("Request (New)");
    }
    me.getLayout().setActiveItem(1);
  },

  _getSubRequestPath: function (parent) {
    var me = this;
    var store = me.grid.getStore();
    var path = [];
    while (parent) {
      path.push(parent);
      parent = store
        .getAt(
          store.findBy(function (record, key) {
            var data = record.getData();
            if (data.ID == parent) {
              return true;
            }
            return false;
          })
        )
        .getData();
      if (!parent._master) break;
      parent = parent._parent;
    }
    return path;
  },

  editSubRequest: function (r) {
    var me = this;
    var store = me.grid.getStore();
    var title = "New subrequest";
    if (r.data.ID) title = "Edit subrequest " + r.data.ID;
    me.subRequestEditor.setTitle(title);

    var path = me._getSubRequestPath(r.data._parent);
    me.subRequestEditor.Original.IDs = path;
    store.on("datachanged", me.subRequestEditor.Original.onDataChanged, me.subRequestEditor.Original);

    me.subRequestEditor.parentPath = path;
    store.on(
      "delete",
      function (id) {
        for (var i = 0; i < me.parentPath.length; ++i)
          if (me.parentPath[i] == id) {
            me.onCancel();
            break;
          }
      },
      me.subRequestEditor
    );

    me.getLayout().setActiveItem(2);

    var originalRequest = store.getAt(
      store.findBy(function (record, key) {
        var data = record.getData();
        if (data.ID == r.data._parent) {
          return true;
        }
        return false;
      })
    );

    var setro = false;
    if (originalRequest.get("reqState") != "New") setro = true;

    me.subRequestEditor.loadRecord(r, setro);
    me.subRequestEditor.Original.onDataChanged(store);
  },
  __addsubrequest: function () {
    var me = this;
    var result = me.__getSelectedValues();
    var data = result.data.getData();
    var adder = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.SubRequestAdder", {
      title: "Add subrequests to " + data.ID,
      gridData: data,
    });
    adder.on("saved", me.reloadGridExpandedGrid, me);
    adder.show();
  },
  reloadGridExpandedGrid: function () {
    var me = this;
    me.grid.getStore().reload();
    if (me.grid.expandedGridPanel) me.grid.expandedGridPanel.getStore().reload();
  },
  reloadGrid: function () {
    var me = this;
    me.grid.getStore().reload();
  },
  __split: function () {
    var me = this;
    var result = me.__getSelectedValues();
    var r = result.data;
    var spliter = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.RequestSpliter", {
      title: "Split request " + r.data.ID,
      reqdata: r.data,
    });
    spliter.on("saved", me.reloadGrid, me);
    spliter.show();
  },
  __removesubrequests: function () {
    var me = this;
    var result = me.__getSelectedValues();
    var id = result.data.getData().ID;
    Ext.MessageBox.confirm(
      "Message",
      "Do you really want to delete all Subrequests ?",
      function (btn) {
        if (btn == "yes") me.__realRemoveSubRequests(id);
      },
      me
    );
  },
  __realRemoveSubRequests: function (id) {
    var me = this;
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + me.applicationName + "/list",
      method: "GET",
      params: {
        anode: Ext.JSON.encode([id]),
        sort: Ext.encode([
          {
            property: "ID",
            direction: "DESC",
          },
        ]),
      },
      scope: me,
      success: function (response) {
        if (response) {
          // check that it is really OK... AZ: !! ??
          var str = "";
          try {
            var result = Ext.decode(response.responseText);
            if (!result.OK) str = result.Message;
          } catch (e2) {
            str = "unparsable reply from the portal: " + e2.message;
          }
          if (str) {
            Ext.MessageBox.show({
              title: "Can not get subrequest list",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
        for (var i = 0; i < result.result.length; ++i) me.__realDelRequest(result.result[i].ID);
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  __productions: function () {
    var me = this;
    var result = me.__getSelectedValues();
    var id = result["data"].get("ID");
    if (result["expData"] != null) {
      id = result["expData"].get("ID");
    }
    var win = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.ProductionManager", {
      title: "Productions for request " + id,
      rID: id,
    });
    win.show();
  },
  __transformations: function () {
    var me = this;
    var result = me.__getSelectedValues();
    var r = result.data;
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/productions",
      method: "POST",
      params: {
        RequestID: r.data.ID,
      },
      scope: me,
      success: function (response) {
        if (response) {
          // check that it is really OK... AZ: !! ??
          var str = "";
          try {
            var result = Ext.decode(response.responseText);
            if (!result.OK) str = result.Message;
          } catch (e2) {
            str = "unparsable reply from the portal: " + e2.message;
          }
          if (str) {
            Ext.MessageBox.show({
              title: "Production list failed",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
          if (result.total) {
            var setupdata = {
              data: {
                leftMenu: {
                  transformationId: result.result,
                },
              },
              currentState: result.result.toString(),
            };

            GLOBAL.APP.MAIN_VIEW.createNewModuleContainer({
              objectType: "app",
              moduleName: me.applicationsToOpen["LHCbTransformationMonitor"],
              setupData: setupdata,
            });
          } else Ext.dirac.system_info.msg("Error Notification", "Productions for this request", "No productions associated with this request");
        }
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  __model: function () {
    var me = this;
    var result = me.__getSelectedValues();
    var r = result.data;
    var IsModel = null;
    if (r.data.IsModel) IsModel = 0;
    else IsModel = 1;
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/save",
      method: "POST",
      params: {
        ID: r.data.ID,
        IsModel: IsModel,
      },
      scope: me,
      success: function (response) {
        if (response) {
          // check that it is really OK... AZ: !! ??
          var str = "";
          try {
            var result = Ext.decode(response.responseText);
            if (!result.OK) str = result.Message;
          } catch (e2) {
            str = "unparsable reply from the portal: " + e2.message;
          }
          if (str) {
            Ext.MessageBox.show({
              title: "Changing model flag has failed",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
        me.reloadGrid();
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  __edit: function () {
    var me = this;
    var result = me.__getSelectedValues();
    me.viewEditor(result);
  },
  __test: function () {
    var me = this;
    var result = me.__getSelectedValues();

    var win = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.Tester", {
      title: "Test for request " + result.data.get("ID"),
      pData: result.data.getData(),
    });
    win.show();
  },
  __sign: function () {
    var me = this;
    var result = me.__getSelectedValues();
    me.viewEditor(result, result.data.getData("reqType"));
  },
  __resurrect: function () {
    var me = this;
    var result = me.__getSelectedValues();
    var data = result.data.getData();
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/save",
      method: "POST",
      params: {
        ID: data.ID,
        reqState: "New",
      },
      scope: me,
      success: function (response) {
        if (response) {
          // check that it is really OK... AZ: !! ??
          var str = "";
          try {
            var result = Ext.decode(response.responseText);
            if (!result.OK) str = result.Message;
          } catch (e2) {
            str = "unparsable reply from the portal: " + e2.message;
          }
          if (str) {
            Ext.MessageBox.show({
              title: "Resurrecting has failed",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
        me.grid.getStore().reload();
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  __reactivate: function () {
    var me = this;
    var result = me.__getSelectedValues();
    var r = result.data;
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/save",
      method: "POST",
      params: {
        ID: r.data.ID,
        reqState: "Active",
      },
      scope: me,
      success: function (response) {
        if (response) {
          // check that it is really OK... AZ: !! ??
          var str = "";
          try {
            var result = Ext.decode(response.responseText);
            if (!result.OK) str = result.Message;
          } catch (e2) {
            str = "unparsable reply from the portal: " + e2.message;
          }
          if (str) {
            Ext.MessageBox.show({
              title: "Reactivation has failed",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
        me.reloadGrid();
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  __confirm: function () {
    var me = this;
    var result = me.__getSelectedValues();
    me.viewEditor(result);
  },
  ConAdvRequest: function (opname, url, params, scope, success, failure) {
    var conn = new Ext.data.Connection();
    conn.request({
      url: url,
      method: "GET",
      params: params,
      scope: scope,
      success: function (response) {
        var result = "";
        if (response) {
          // check that it is really OK... AZ: !! ??
          var str = "";
          try {
            result = Ext.decode(response.responseText);
            if (!result.OK) str = result.Message;
          } catch (e2) {
            str = "unparsable reply from the portal: " + e2.message;
          }
          if (str) {
            if (failure) failure.call(scope, opname, str);
            else
              Ext.MessageBox.show({
                title: opname + " fail",
                msg: str,
                buttons: Ext.MessageBox.OK,
                icon: Ext.MessageBox.ERROR,
              });
            return;
          }
        }
        success.call(scope, result.result);
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  __onDupStepFailed: function (opname, msg) {
    var me = this;
    me.DupRec = "";
    me.DupSteps = "";
    Ext.MessageBox.show({
      title: "Processing Duplicate has failed",
      msg: msg,
      buttons: Ext.MessageBox.OK,
      icon: Ext.MessageBox.ERROR,
    });
  },
  __onDupStepLoaded: function (s) {
    var me = this;
    if (!me.DupRec) return;
    if (!s) return;
    if (!s.StepId) {
      me.__onDupStepFailed("step", "Step no longer exists in BK");
      return;
    }
    if (s.Usable != "Yes") {
      Ext.Msg.show({
        title: "Do you want to duplicate?",
        msg: "Step is no longer usable (obsolete)",
        buttons: Ext.Msg.YESNO,
        scope: this,
        fn: function (btn) {
          if (btn == "yes") {
            var i;
            var found = false;
            for (i = me.DupSteps.length - 1; i >= 0; --i) if (s.StepId == me.DupSteps[i]) found = true;
            if (!found) return;
            var r = me.DupRec;
            me.DupRec = "";
            me.dupSteps = "";
            me.__realDuplicate(r, false);
          } else {
            return;
          }
        },
        icon: Ext.MessageBox.QUESTION,
      });
    } else {
      var i;
      for (i = me.DupSteps.length - 1; i >= 0; --i) if (s.StepId == me.DupSteps[i]) me.DupSteps.splice(i, 1);
      if (me.DupSteps.length) return;
      var r = me.DupRec;
      me.DupRec = "";
      me.dupSteps = "";
      me.__realDuplicate(r, false);
    }
  },
  getSelectedRecords: function () {
    var me = this;
    var selectedItems = [];

    var elements = Ext.query("#" + me.id + " input.checkrow");
    for (var i = 0; i < elements.length; i++) if (elements[i].checked) selectedItems.push(elements[i].value);
    return selectedItems;
  },
  __bulkSign: function () {
    var me = this;

    var selectedItems = me.getSelectedRecords();
    if (selectedItems.length == 0) {
      Ext.dirac.system_info.msg("Error Notification", "Please select requests!");
      return;
    }

    var records = [];
    var store = me.grid.getStore();
    for (var i = 0; i < selectedItems.length; i++) {
      var record = store.findRecord("ID", selectedItems[i]);
      if (me.__requestcanbesigned(record)) {
        var data = record.getData();
        if (data) {
          data["reqState"] = "Accepted";
          records.push(data);
        }
      } else if (me.__requestBkkCheck(record)) {
        if (GLOBAL.USER_CREDENTIALS.group == "lhcb_bk") {
          Ext.dirac.system_info.msg(
            "Error Notification",
            "You can not use bulk sign for a request with the state BK Check: " +
              selectedItems[i] +
              "\n" +
              "Please unselect this request and right click on the request! You have to click the Sign menu item..."
          );
          return;
        } else {
          Ext.dirac.system_info.msg("Error Notification", "You can not sign this request, because you need lhcb_bk role:  " + selectedItems[i]);
          return;
        }
      } else {
        Ext.dirac.system_info.msg(
          "Error Notification",
          "You can not sign the request: " + selectedItems[i] + "\n" + "Please unselect this request and try again..."
        );
        return;
      }
    }
    me.getContainer().setLoading("Updating the requets...");
    for (var i = 0; i < records.length; i++) {
      Ext.Ajax.request({
        timeout: 120000,
        url: GLOBAL.BASE_URL + me.applicationName + "/save",
        method: "POST",
        params: records[i],
        scope: me,
        failure: function (response, action) {
          GLOBAL.APP.CF.showAjaxErrorMessage(response);
          me.getContainer().setLoading(false);
        },
        success: function (response) {
          me.getContainer().setLoading(false);
          var jsonData = Ext.JSON.decode(response.responseText);
          if (jsonData["success"] == "true") {
            Ext.dirac.system_info.msg("Notification", "The  request " + jsonData["requestId"] + " is accepted!");
            me.reloadGrid();
          } else {
            GLOBAL.APP.CF.alert(jsonData["error"], "Error");
          }
        },
      });
    }
  },
  __requestBkkCheck: function (record) {
    return record.get("reqState") == "BK Check";
  },
  __requestcanbesigned: function (record) {
    return (
      (record.get("reqState") == "Submitted" && GLOBAL.USER_CREDENTIALS.group == "lhcb_ppg") ||
      (record.get("reqState") == "Submitted" && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") ||
      (record.get("reqState") == "On-hold" && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") ||
      (record.get("reqState") == "Tech OK" && GLOBAL.USER_CREDENTIALS.group == "lhcb_ppg") ||
      (record.get("reqState") == "PPG OK" && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech")
    );
  },

  __bulkActivate: function () {
    var me = this;

    var selectedItems = me.getSelectedRecords();
    if (selectedItems.length == 0) {
      Ext.dirac.system_info.msg("Error Notification", "Please select requests!");
      return;
    }

    var records = [];
    var store = me.grid.getStore();
    for (var i = 0; i < selectedItems.length; i++) {
      var record = store.findRecord("ID", selectedItems[i]);
      if (me.__requestcanbeactivated(record)) {
        var data = record.getData();
        if (data) {
          data["reqState"] = "Active";
          records.push(data);
        }
      } else {
        Ext.dirac.system_info.msg(
          "Error Notification",
          "You can not sign the request: " + selectedItems[i] + "\n" + "Please unselect this request and try again..."
        );
        return;
      }
    }
    me.getContainer().setLoading("Updating the requets...");
    for (var i = 0; i < records.length; i++) {
      Ext.Ajax.request({
        timeout: 120000,
        url: GLOBAL.BASE_URL + me.applicationName + "/save",
        method: "POST",
        params: records[i],
        scope: me,
        failure: function (response, action) {
          GLOBAL.APP.CF.showAjaxErrorMessage(response);
          me.getContainer().setLoading(false);
        },
        success: function (response) {
          me.getContainer().setLoading(false);
          var jsonData = Ext.JSON.decode(response.responseText);
          if (jsonData["success"] == "true") {
            Ext.dirac.system_info.msg("Notification", "The  request " + jsonData["requestId"] + " is activated!");
            me.reloadGrid();
          } else {
            GLOBAL.APP.CF.alert(jsonData["error"], "Error");
          }
        },
      });
    }
  },
  __requestcanbeactivated: function (record) {
    return record.get("reqState") == "Accepted";
  },
  __bulkAccepted: function () {
    var me = this;

    var selectedItems = me.getSelectedRecords();
    if (selectedItems.length == 0) {
      Ext.dirac.system_info.msg("Error Notification", "Please select requests!");
      return;
    }

    var records = [];
    var store = me.grid.getStore();
    for (var i = 0; i < selectedItems.length; i++) {
      var record = store.findRecord("ID", selectedItems[i]);
      if (me.__requestcanbeaccepted(record)) {
        var data = record.getData();
        if (data) {
          data["reqState"] = "Accepted";
          records.push(data);
        }
      } else {
        Ext.dirac.system_info.msg(
          "Error Notification",
          "You can not sign the request: " + selectedItems[i] + "\n" + "Please unselect this request and try again..."
        );
        return;
      }
    }
    me.getContainer().setLoading("Updating the requets...");
    for (var i = 0; i < records.length; i++) {
      Ext.Ajax.request({
        timeout: 120000,
        url: GLOBAL.BASE_URL + me.applicationName + "/save",
        method: "POST",
        params: records[i],
        scope: me,
        failure: function (response, action) {
          GLOBAL.APP.CF.showAjaxErrorMessage(response);
          me.getContainer().setLoading(false);
        },
        success: function (response) {
          me.getContainer().setLoading(false);
          var jsonData = Ext.JSON.decode(response.responseText);
          if (jsonData["success"] == "true") {
            Ext.dirac.system_info.msg("Notification", "The  request " + jsonData["requestId"] + " is accepted!");
            me.reloadGrid();
          } else {
            GLOBAL.APP.CF.alert(jsonData["error"], "Error");
          }
        },
      });
    }
  },
  __requestcanbeaccepted: function (record) {
    return record.get("reqState") == "Active";
  },
  __submit: function () {
    var me = this;

    var selectedItems = me.getSelectedRecords();
    if (selectedItems.length == 0) {
      Ext.dirac.system_info.msg("Error Notification", "Please select requests!");
      return;
    }

    var result = me.__getSelectedValues();
    if (result.data == null) {
      Ext.dirac.system_info.msg("Error Notification", "Please select click on a row in the table!");
      return;
    }
    var pData = result.data.data;

    prw = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.PrWorkflow", {
      pData: pData,
      RequestIDs: selectedItems,
    });
    prw.show();
  },
  __prioritycanbechanged: function (record) {
    return true; //record.get("reqState") == "Submitted";
  },
  __bulkPriority: function () {
    var me = this;

    var selectedItems = me.getSelectedRecords();
    if (selectedItems.length == 0) {
      Ext.dirac.system_info.msg("Error Notification", "Please select requests!");
      return;
    }

    var records = [];
    var store = me.grid.getStore();
    for (var i = 0; i < selectedItems.length; i++) {
      var record = store.findRecord("ID", selectedItems[i]);
      if (me.__prioritycanbechanged(record)) {
        var data = record.getData();
        if (data) {
          records.push(data);
        }
      } else {
        Ext.dirac.system_info.msg(
          "Error Notification",
          "You can not sign the request: " + selectedItems[i] + "\n" + "Please unselect this request and try again..."
        );
        return;
      }
    }
    var priorityEditor = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.RequestPriorityEditor");
    priorityEditor.show();
    priorityEditor.on(
      "setClick",
      function (priority) {
        var reqIds = [];
        records.forEach(function (value) {
          reqIds.push(value.ID);
        });
        Ext.MessageBox.confirm(
          "Priority:" + priority,
          "Do you really want to set " + priority + " to the following requests: " + reqIds.join(",") + "?",
          function (btn) {
            if (btn == "yes") {
              me.getContainer().setLoading("Updating the requets...");
              for (var i = 0; i < records.length; i++) {
                records[i]["reqPrio"] = priority;
                Ext.Ajax.request({
                  timeout: 120000,
                  url: GLOBAL.BASE_URL + me.applicationName + "/save",
                  method: "POST",
                  params: records[i],
                  scope: me,
                  failure: function (response, action) {
                    GLOBAL.APP.CF.showAjaxErrorMessage(response);
                    me.getContainer().setLoading(false);
                  },
                  success: function (response) {
                    me.getContainer().setLoading(false);
                    var jsonData = Ext.JSON.decode(response.responseText);
                    if (jsonData["success"] == "true") {
                      Ext.dirac.system_info.msg("Notification", "The  request " + jsonData["requestId"] + " priority has changed!");
                      me.reloadGrid();
                    } else {
                      GLOBAL.APP.CF.alert(jsonData["error"], "Error");
                    }
                  },
                });
              }
            }
          },
          me
        );
      },
      me
    );
  },
});
