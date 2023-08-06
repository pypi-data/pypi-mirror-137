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
Ext.define("LHCbDIRAC.BookkeepingSimDescription.classes.BookkeepingSimDescription", {
  extend: "Ext.dirac.core.Module",
  requires: [
    "Ext.dirac.utils.DiracBaseSelector",
    "Ext.grid.Panel",
    "LHCbDIRAC.BookkeepingSimDescription.classes.SimulationEditor",
    "Ext.dirac.utils.DiracApplicationContextMenu",
  ],
  loadState: function (data) {},

  getStateData: function () {
    var data = {};
    return data;
  },
  initComponent: function () {
    var me = this;

    (me.launcher.title = "Bookkeeping ConditionDescriptions"), (me.launcher.maximized = false);

    if (GLOBAL.VIEW_ID == "desktop") {
      var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

      me.launcher.width = oDimensions[0];
      me.launcher.height = oDimensions[1];

      me.launcher.x = 0;
      me.launcher.y = 0;
    }

    Ext.apply(me, {
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

    var textFields = {
      SimId: {
        name: "Simulation condition Id",
        type: "Number",
      },
      SimDescription: {
        name: "Simulation Condition Description",
        type: "originalText",
      },
    };

    var selectors = {
      Visible: "Visible",
    };
    var map = [["Visible", "Visible"]];

    me.leftPanel = Ext.create("Ext.dirac.utils.DiracBaseSelector", {
      scope: me,
      textFields: textFields,
      hasTimeSearchPanel: false,
      datamap: map,
      cmbSelectors: selectors,
      url: "BookkeepingSimDescription/getSelectionData",
      collapsed: true,
    });

    var oProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
      url: GLOBAL.BASE_URL + "BookkeepingSimDescription/getData",
    });

    me.dataFields = [
      {
        name: "SimId",
      },
      {
        name: "SimDescription",
      },
      {
        name: "BeamCond",
      },
      {
        name: "BeamEnergy",
      },
      {
        name: "Generator",
      },
      {
        name: "MagneticField",
      },
      {
        name: "DetectorCond",
      },
      {
        name: "Luminosity",
      },
      {
        name: "G4settings",
      },
      {
        name: "Visible",
      },
    ];
    me.dataStore = Ext.create("Ext.dirac.utils.DiracJsonStore", {
      proxy: oProxy,
      fields: me.dataFields,
      scope: me,
    });

    var oColumns = {
      Id: {
        dataIndex: "SimId",
        properties: {
          width: 60,
        },
      },
      SimDescription: {
        dataIndex: "SimDescription",
        properties: {
          flex: 1,
        },
      },
      Visible: {
        dataIndex: "Visible",
      },
    };

    var toolButtons = {
      Protected: [
        {
          // "text" : "New",
          handler: me.__oprSimualtionConditions,
          arguments: ["new", ""],
          properties: {
            tooltip: "Click to create a new simulation condition",
            iconCls: "dirac-icon-plus",
          },
          property: "BookkeepingManagement",
        },
        {
          // "text" : "Edit",
          handler: me.__oprSimualtionConditions,
          arguments: ["edit", ""],
          properties: {
            tooltip: "Click to edit the selected condition",
            iconCls: "dirac-icon-edit",
          },
          property: "BookkeepingManagement",
        },
        {
          // "text" : "Delete",
          handler: me.__oprSimualtionConditions,
          arguments: ["delete", ""],
          properties: {
            tooltip: "Click to delete the selected condition",
            iconCls: "dirac-icon-delete",
          },
          property: "BookkeepingManagement",
        },
      ],
    };

    var pagingToolbar = Ext.create("Ext.dirac.utils.DiracPagingToolbar", {
      toolButtons: toolButtons,
      dataStore: me.dataStore,
      scope: me,
    });

    var menuitems = {
      Visible: [
        {
          text: "Window view",
          handler: me.__oprSimualtionConditions,
          arguments: ["windowview"],
          properties: {
            tooltip: "Click to view in a window the simulation condition",
          },
        },
        {
          text: "View",
          handler: me.__oprSimualtionConditions,
          arguments: ["view"],
          properties: {
            tooltip: "Click to view the simulation condition",
            iconCls: "dirac-icon-text",
          },
        },
      ],
      Protected: [
        {
          text: "Edit",
          handler: me.__oprSimualtionConditions,
          arguments: ["edit"],
          properties: {
            tooltip: "Click to edit the simulation condition",
            iconCls: "dirac-icon-edit",
          },
          property: "BookkeepingManagement",
        },
        {
          text: "New",
          handler: me.__oprSimualtionConditions,
          arguments: ["new"],
          properties: {
            tooltip: "Click to create a new simulation condition",
            iconCls: "dirac-icon-plus",
          },
          property: "BookkeepingManagement",
        },
        {
          text: "Delete",
          handler: me.__oprSimualtionConditions,
          arguments: ["delete"],
          properties: {
            tooltip: "Click to Delete the simulation condition",
            iconCls: "dirac-icon-delete",
          },
          property: "BookkeepingManagement",
        },
      ],
    };

    me.contextGridMenu = Ext.create("Ext.dirac.utils.DiracApplicationContextMenu", {
      menu: menuitems,
      scope: me,
      dynamicShow: true,
    });
    me.grid = Ext.create("Ext.dirac.utils.DiracGridPanel", {
      store: me.dataStore,
      oColumns: oColumns,
      tbar: pagingToolbar,
      pagingToolbar: pagingToolbar,
      stateful: true,
      stateId: "BookkeepingSimGrid",
      contextMenu: me.contextGridMenu,
      plugins: [
        {
          ptype: "rowexpander",
          rowBodyTpl: new Ext.XTemplate(
            "<b>BeamCond:</b> {BeamCond}<br/>",
            "<b>BeamEnergy:</b> {BeamEnergy}<br/>",
            "<b>Generator:</b> {Generator} <b>MagneticField:</b> {MagneticField}<br/> <b>DetectorCond:</b> {DetectorCond}<br/>",
            "<b>Luminosity:</b> {Luminosity}<br/>",
            "<b>G4settings:</b> {G4settings}<br/>"
          ),
        },
      ],
      scope: me,
    });

    me.leftPanel.setGrid(me.grid);

    var viewStore = Ext.create("Ext.data.Store", {
      fields: me.dataFields,
    });
    var tpl = new Ext.XTemplate(
      '<tpl for=".">',
      '<div style="margin-bottom: 10px;" class="dataset-statistics">',
      "<b>SimId:</b> {SimId}<br/>",
      "<b>SimDescription:</b> {SimDescription}<br/>",
      "<b>BeamCond:</b> {BeamCond}<br/>",
      "<b>BeamEnergy:</b> {BeamEnergy}<br/>",
      "<b>Generator:</b> {Generator} <b>MagneticField:</b> {MagneticField}<br/> <b>DetectorCond:</b> {DetectorCond}<br/>",
      "<b>Luminosity:</b> {Luminosity}<br/>",
      "<b>G4settings:</b> {G4settings}<br/>",
      "<b>Visible:</b> {Visible}<br/>",
      "</div>",
      "</tpl>"
    );
    me.conditionview = new Ext.panel.Panel({
      region: "east",
      scrollable: true,
      collapsible: true,
      split: true,
      margins: "2 0 2 0",
      cmargins: "2 2 2 2",
      bodyStyle: "padding: 5px",
      width: 600,
      labelAlign: "top",
      minWidth: 200,
      hidden: true,
      items: [me.simulationForm],
      listeners: {
        collapse: function (panel, eOpts) {
          panel.hide();
        },
      },
      items: new Ext.view.View({
        tpl: tpl,
        store: viewStore,
        itemSelector: "div.dataset-statistics",
        autoHeight: true,
      }),
      bodyStyle: "padding: 5px",
    });

    me.simulationForm = Ext.create("LHCbDIRAC.BookkeepingSimDescription.classes.SimulationEditor", {
      title: "Add new simulation condition",
      scope: me,
    });
    me.editor = Ext.create("Ext.panel.Panel", {
      title: "Simulation editor:",
      region: "east",
      scrollable: true,
      collapsible: true,
      split: true,
      margins: "2 0 2 0",
      cmargins: "2 2 2 2",
      bodyStyle: "padding: 5px",
      width: 600,
      labelAlign: "top",
      minWidth: 200,
      hidden: true,
      items: [me.simulationForm],
      listeners: {
        collapse: function (panel, eOpts) {
          panel.hide();
        },
      },
    });
    me.add([me.leftPanel, me.grid, me.editor, me.conditionview]);
  },
  __oprSimualtionConditions: function (action) {
    var me = this;
    if (action == "edit") {
      var simid = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "SimId");
      if (simid == "") {
        GLOBAL.APP.CF.alert("Please select a simulation condition by clicking one of the row in the Grid panel!", "error");
        return;
      } else {
        me.simulationForm.setTitle("Edit simulation condition:");
        me.simulationForm.getForm().load({
          url: "BookkeepingSimDescription/editSimulation",
          params: {
            SimId: simid,
          },
        });
        me.editor.expand();
        me.editor.show();
      }
    } else if (action == "new") {
      me.simulationForm.getForm().reset();
      me.simulationForm.setTitle("Add new simulation condition");
      me.editor.expand();
      me.editor.show();
    } else if (action == "delete") {
      var simid = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "SimId");
      if (simid == "") {
        GLOBAL.APP.CF.alert("Please select a simulation condition by clicking one of the row in the Grid panel!", "error");
        return;
      } else {
        var message = "Do you want to delete the " + simid + "?";
        Ext.MessageBox.confirm("Confirm", message, function (button) {
          if (button === "yes") {
            Ext.Ajax.request({
              url: "BookkeepingSimDescription/simulationdelete",
              params: {
                SimId: simid,
              },
              success: function (response) {
                var value = Ext.JSON.decode(response.responseText);
                if (value.success == "false") {
                  GLOBAL.APP.CF.alert(value.error, "error");
                } else {
                  GLOBAL.APP.CF.alert(value.result, "info");
                  me.grid.getStore().load();
                }
              },
              failure: function (response, opts) {
                GLOBAL.APP.CF.showAjaxErrorMessage(response);
              },
            });
          }
        });
      }
      return;
    } else if (action == "view") {
      var data = me.grid.getSelectionModel().getSelection()[0].data;
      me.conditionview.items.getAt(0).getStore().loadData([data]);
      me.conditionview.expand();
      me.conditionview.show();
    } else if (action == "windowview") {
      var tpl = [
        "<b>SimId:</b> {SimId}<br/>",
        "<b>SimDescription:</b> {SimDescription}<br/>",
        "<b>BeamCond:</b> {BeamCond}<br/>",
        "<b>BeamEnergy:</b> {BeamEnergy}<br/>",
        "<b>Generator:</b> {Generator}<br/>",
        "<b>MagneticField:</b> {MagneticField}<br/>",
        "<b>DetectorCond:</b> {DetectorCond}<br/>",
        "<b>Luminosity:</b> {Luminosity}<br/>",
        "<b>G4settings:</b> {G4settings}<br/>",
        "<b>Visible:</b> {Visible}<br/>",
      ];
      var data = me.grid.getSelectionModel().getSelection()[0].data;
      me.getContainer().oprPrepareAndShowWindowTpl(tpl, data, "SimID " + data.SimId);
    }
  },
});
