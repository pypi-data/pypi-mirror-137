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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.InDataDetail", {
  extend: "Ext.panel.Panel",
  tplSimMarkup: [
    "<b>Simulation conditions:</b> {simDesc}<br/>",
    "<b>Beam:</b> {BeamCond}<br/>",
    "<b>Beam energy:</b> {BeamEnergy}<br/>",
    "<b>Generator:</b> {Generator}<br/>",
    "<b>G4 settings:</b> {G4settings}<br/>",
    "<b>Magnetic field:</b> {MagneticField}<br/>",
    "<b>Detector:</b> {DetectorCond}<br/>",
    "<b>Luminosity:</b> {Luminosity}<br/>",
    "<br/><b>Process Pass:</b> {inProPass}<br/>",
    "<br/><b>Event type:</b> {evType}<br/>",
    "<br/><b>File type:</b> {inFileType}<br/>",
  ],

  tplRunMarkup: [
    "<b>Run conditions:</b> {simDesc}<br/>",
    "<b>Beam:</b> {BeamCond}<br/>",
    "<b>Beam energy:</b> {BeamEnergy}<br/>",
    "<b>Magnetic field:</b> {MagneticField}<br/>",
    "<b>Subdetectors:</b> {DetectorCond}<br/>",
    "<br/><b>Process Pass:</b> {inProPass}<br/>",
    "<br/><b>Event type:</b> {evType}<br/>",
    "<br/><b>File type:</b> {inFileType_sp}<br/>",
  ],

  initComponent: function () {
    var me = this;

    me.sim_tpl = new Ext.Template(me.tplSimMarkup);
    me.run_tpl = new Ext.Template(me.tplRunMarkup);
    me.data = {};
    me.callParent(arguments);
  },

  set: function (data) {
    for (var x in data) this.data[x] = data[x];
    this.data.inFileType_sp = data.inFileType;
  },

  updateDetail: function (data) {
    var me = this;
    if (data.condType == "Run") {
      if (
        me.data &&
        me.data.configName == data.configName &&
        me.data.configVersion == data.configVersion &&
        me.data.condType == data.condType &&
        me.data.inProPass.toString() == data.inProPass.toString() &&
        me.data.evType.toString() == data.evType.toString()
      ) {
        if (me.data.inFileType == data.inFileType) return; // exception, do not remove the last element
        var types = me.data.inFileType.split(",");
        for (var i = 0; i < types.length; ++i) {
          if (types[i] == data.inFileType) break;
        }
        if (i < types.length) types.splice(i, 1);
        else types.push(data.inFileType);
        types.sort();
        me.data.inFileType = types.join(",");
        me.data.inFileType_sp = types.join(" ");
        me.run_tpl.overwrite(me.body, me.data);
        return;
      }
      me.set(data);
      me.run_tpl.overwrite(me.body, me.data);
    } else {
      me.set(data);
      me.sim_tpl.overwrite(me.body, me.data);
    }
  },
});

Ext.define("LHCbDIRAC.ProductionRequestManager.classes.BookkeepingInputDataBrowser", {
  extend: "Ext.window.Window",

  alias: "widget.bkinputdatabrowser",

  plain: true,
  resizable: false,
  modal: true,
  closeAction: "hide",

  initComponent: function () {
    var me = this;

    me.treeStore = Ext.create("Ext.data.TreeStore", {
      fields: ["text", "id", "configName", "level", "configVersion", "simCondID", "condType", "inProPass", "evType"],
      autoLoad: true,
      scope: me,
      proxy: {
        type: "ajax",
        url: "ProductionRequestManager/bkk_input_tree",
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
          if (operation.node && operation.node.get("configName")) store.proxy.extraParams.configName = operation.node.get("configName");
          else delete store.proxy.extraParams.configName;
          if (operation.node && operation.node.get("configVersion")) store.proxy.extraParams.configVersion = operation.node.get("configVersion");
          else delete store.proxy.extraParams.configVersion;
          if (operation.node && operation.node.get("simCondID")) store.proxy.extraParams.simCondID = operation.node.get("simCondID");
          else delete store.proxy.extraParams.simCondID;
          if (operation.node && operation.node.get("condType")) store.proxy.extraParams.condType = operation.node.get("condType");
          else delete store.proxy.extraParams.condType;
          if (operation.node && operation.node.get("inProPass")) store.proxy.extraParams.inProPass = operation.node.get("inProPass");
          else delete store.proxy.extraParams.inProPass;
          if (operation.node && operation.node.get("evType")) store.proxy.extraParams.evType = operation.node.get("evType");
          else delete store.proxy.extraParams.evType;
        },
      },
    });

    me.treePanel = Ext.create("Ext.tree.Panel", {
      title: "Input data",
      stateful: true,
      rootVisible: false,
      layout: "fit",
      store: me.treeStore,
      loading: true,
      scrollable: true,

      listeners: {
        itemclick: function (aa, record, item, index, e, opt) {
          if (record.isLeaf()) {
            me.detail.updateDetail(record.raw);
            me.down("[name=in-data-select]").enable();
          }
        },
      },

      scope: me,
    });
    me.treePanel.setLoading(true);
    me.detail = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.InDataDetail", {
      region: "east",
      split: true,
      width: 350,
      minWidth: 200,
      margins: "5 5 5 0",

      title: "Details",
      bodyStyle: "padding-left:15px; padding-top:5px",

      html: "<p>Plese select Input Data on the left side</p>",

      buttonAlign: "center",
      buttons: [
        {
          text: "Select",
          name: "in-data-select",
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
      title: "Input data browser",
      width: 750,
      height: 350,
      minWidth: 500,
      minHeight: 300,
      maximizable: true,
      modal: true,
      layout: "border",
      items: [
        {
          xtype: "panel",
          region: "center",
          split: true,
          margins: "5 0 5 5",
          minWidth: 300,
          scrollable: true,
          activeTab: 0,
          items: [me.treePanel],
        },
        me.detail,
      ],
    });
    me.callParent(arguments);
  },
});
