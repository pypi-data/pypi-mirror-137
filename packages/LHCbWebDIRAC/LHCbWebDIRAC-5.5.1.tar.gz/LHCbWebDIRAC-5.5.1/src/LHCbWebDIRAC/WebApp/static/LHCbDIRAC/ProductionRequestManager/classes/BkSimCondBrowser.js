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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.BkAllSimCond", {
  extend: "Ext.grid.Panel",
  initComponent: function () {
    var me = this;

    me.store = Ext.create("Ext.data.JsonStore", {
      autoLoad: true,
      fields: ["simCondID", "simDesc", "BeamCond", "BeamEnergy", "Generator", "G4settings", "MagneticField", "DetectorCond", "Luminosity"],
      remoteSort: true,
      proxy: {
        type: "ajax",
        url: GLOBAL.BASE_URL + "ProductionRequestManager/bkk_simcond",
        reader: {
          type: "json",
          rootProperty: "result",
        },
      },
    });

    me.pagingBar = Ext.create("Ext.toolbar.Paging", {
      pageSize: 150,
      store: me.store,
      displayInfo: true,
      displayMsg: "Displaying {0} - {1} of {2}",
      emptyMsg: "No conditions are registered",
    });

    me.store.sort("simDesc", "ASC");

    me.store.load({
      params: {
        start: 0,
        limit: me.pagingBar.pageSize,
      },
    });

    Ext.apply(me, {
      columns: [
        {
          header: "Description",
          flex: true,
          sortable: true,
          dataIndex: "simDesc",
        },
      ],
      autoHeight: false,
      autoWidth: true,
      loadMask: true,
      region: "center",
      stripeRows: true,
      dockedItems: [me.pagingBar],
    });
    me.callParent();
  },
});

Ext.define("LHCbDIRAC.ProductionRequestManager.classes.SimCondDetail", {
  extend: "Ext.panel.Panel",
  tplMarkup: [
    "<b>ID:</b> {simCondID}<br/>",
    "<b>Description:</b> {simDesc}<br/>",
    "<b>Beam:</b> {BeamCond}<br/>",
    "<b>Beam energy:</b> {BeamEnergy}<br/>",
    "<b>Generator:</b> {Generator}<br/>",
    "<b>G4 settings:</b> {G4settings}<br/>",
    "<b>Magnetic field:</b> {MagneticField}<br/>",
    "<b>Detector:</b> {DetectorCond}<br/>",
    "<b>Luminosity:</b> {Luminosity}<br/>",
  ],

  initComponent: function () {
    var me = this;
    me.tpl = new Ext.Template(me.tplMarkup);
    me.data = {};
    me.callParent(arguments);
  },

  updateDetail: function (data) {
    var me = this;
    me.data = data;
    me.tpl.overwrite(me.body, me.data);
  },
});

Ext.define("LHCbDIRAC.ProductionRequestManager.classes.BkSimCondBrowser", {
  extend: "Ext.window.Window",

  alias: "widget.bksimcondbrowser",

  plain: true,
  resizable: false,
  modal: true,
  closeAction: "hide",

  initComponent: function () {
    var me = this;

    me.treeStore = Ext.create("Ext.data.TreeStore", {
      fields: ["text", "selection", "fullpath", "level"],
      scope: me,
      proxy: {
        type: "ajax",
        url: "ProductionRequestManager/getSimCondTree",
      },
      root: {
        text: "/",
        id: "/",
        expanded: true,
      },
      folderSort: true,
      sorters: [
        {
          property: "text",
          direction: "ASC",
        },
      ],
    });

    me.treePanel = Ext.create("Ext.tree.Panel", {
      title: "Used",
      stateful: true,
      rootVisible: false,
      layout: "fit",
      store: me.treeStore,
      listeners: {
        itemclick: function (aa, record, item, index, e, eOpts) {
          if (record.data.level == "Simulation Conditions/DataTaking") {
            Ext.Ajax.request({
              url: GLOBAL.BASE_URL + "BookkeepingSimDescription/getData",
              timeout: 120000,
              params: {
                SimDescription: Ext.JSON.encode([record.data.text]),
              },
              success: function (response) {
                var value = Ext.JSON.decode(response.responseText);
                if (value.success == "false") {
                  GLOBAL.APP.CF.alert(value.error, "error");
                } else {
                  if (value.result.length > 0) {
                    var data = value.result["0"];
                    data.simCondID = data.SimId;
                    data.simDesc = data.SimDescription;
                    me.detail.updateDetail(data);
                    me.down("[name=sim-cond-select]").enable();
                  } else {
                    GLOBAL.APP.CF.alert("Please select simulation descriptions under MC directory!", "error");
                  }
                }
              },
              failure: function (response) {
                GLOBAL.APP.CF.showAjaxErrorMessage(response);
              },
            });
          }
        },
      },
      scope: me,
    });

    var list = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.BkAllSimCond", {
      title: "All",
    });
    list.getSelectionModel().on("select", me.onListSelect, me);

    me.detail = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.SimCondDetail", {
      region: "east",
      split: true,
      width: 350,
      minWidth: 200,
      margins: "5 5 5 0",

      title: "Condition details",
      bodyStyle: "padding-left:15px; padding-top:5px",

      html: "<p>Plese select Simulation Condition on the left side</p>",

      buttonAlign: "center",
      buttons: [
        {
          text: "Select",
          name: "sim-cond-select",
          disabled: true,
        },
        {
          text: "Cancel",
          handler: me.close,
          scope: me,
        },
      ],
    });

    Ext.apply(me, {
      title: "Simulation conditions browser",
      width: 750,
      height: 350,
      minWidth: 500,
      minHeight: 300,
      maximizable: true,
      modal: true,
      layout: "border",
      items: [
        {
          xtype: "tabpanel",
          region: "center",
          split: true,
          margins: "5 0 5 5",
          minWidth: 300,

          activeTab: 0,
          items: [list, me.treePanel],
        },
        me.detail,
      ],
    });
    me.callParent(arguments);
  },
  onListSelect: function (sm, record, index, eOpts) {
    var me = this;
    me.detail.updateDetail(record.data);
    me.down("[name=sim-cond-select]").enable();
  },
});
