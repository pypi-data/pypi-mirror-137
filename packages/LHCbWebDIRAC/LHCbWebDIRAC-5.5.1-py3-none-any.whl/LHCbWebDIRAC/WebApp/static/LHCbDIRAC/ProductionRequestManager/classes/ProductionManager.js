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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.ProductionManager", {
  extend: "Ext.window.Window",
  requires: [],

  alias: "widget.productionmanager",

  plain: true,
  resizable: false,
  modal: true,
  closeAction: "hide",
  initComponent: function () {
    var me = this;
    me.readonly = true;
    if (GLOBAL.USER_CREDENTIALS.group == "lhcb_prmgr") me.readonly = false;
    me.menu = new Ext.menu.Menu();
    me.modyfied = false; // to trigger "save" event

    me.store = Ext.create("Ext.data.JsonStore", {
      remoteSort: false,
      fields: ["ProductionID", "RequestID", "Used", "BkEvents"],
      proxy: {
        type: "ajax",
        url: GLOBAL.BASE_URL + "ProductionRequestManager/progress?RequestID=" + me.rID,
        reader: {
          type: "json",
          rootProperty: "result",
        },
      },
    });

    me.store.load();

    me.grid = Ext.create("Ext.grid.Panel", {
      region: "center",
      margins: "2 2 2 2",
      store: me.store,
      columns: [
        {
          header: "Used",
          dataIndex: "Used",
          renderer: me.renderUse,
        },
        {
          header: "Production",
          dataIndex: "ProductionID",
        },
        {
          header: "Events in BK",
          dataIndex: "BkEvents",
        },
      ],
      stripeRows: true,
      viewConfig: {
        forceFit: true,
      },
    });

    me.form = Ext.create("Ext.form.Panel", {
      region: "south",
      margins: "2 2 2 2",
      autoHeight: true,
      frame: true,
      items: {
        layout: "column",
        items: [
          {
            layout: "column",
            items: {
              xtype: "numberfield",
              allowDecimals: false,
              name: "ProductionID",
              emptyText: "Enter production ID",
              hideLabel: true,
            },
          },
          {
            layout: "column",
            bodyStyle: "padding-left: 5px;",
            items: {
              xtype: "button",
              text: "Add",
              handler: me.onAdd,
              scope: me,
            },
          },
        ],
      },
    });
    var items = [me.grid, me.form];
    if (me.readonly) items = me.grid;

    Ext.apply(me, {
      modal: true,
      width: 300,
      height: 200,
      layout: "border",
      items: items,
    });
    me.callParent(arguments);
  },

  onRowClick: function (grid, record, item, index, e, eOpts) {
    var me = this;
    var id = record.get("ProductionID");
    var usedLabel = "";
    me.menu.removeAll();
    me.menu.add({
      handler: function () {
        me.removeProduction(record);
      },
      scope: me,
      text: "Remove",
    });
    if (record.get("Used")) usedLabel = "Mark unused";
    else usedLabel = "Mark used";
    me.menu.add({
      handler: function () {
        me.toggleUsed(record);
      },
      scope: me,
      text: usedLabel,
    });
    me.menu.showAt(e.getXY());
  },

  removeProduction: function (r) {
    var me = this;
    me.action(
      "Deassociate production",
      GLOBAL.BASE_URL + "ProductionRequestManager/remove_production",
      {
        ProductionID: r.data.ProductionID,
      },
      me.onModifySuccess
    );
  },

  toggleUsed: function (r) {
    var me = this;
    me.action(
      "Toggle production use",
      GLOBAL.BASE_URL + "ProductionRequestManager/use_production",
      {
        ProductionID: r.data.ProductionID,
        Used: !r.data.Used ? 1 : 0,
      },
      me.onModifySuccess
    );
  },

  onAdd: function () {
    var me = this;
    var form = me.form.getForm();
    var productionID = form.findField("ProductionID").getValue();
    if (!productionID) return;
    form.submit({
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
      success: me.onModifySuccess,
      scope: me,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/add_production?RequestID=" + me.rID,
      waitMsg: "Assigning production",
    });
  },

  onModifySuccess: function () {
    var me = this;
    me.modyfied = true;
    me.store.reload();
  },

  renderUse: function (val) {
    if (val) return '<span style="color:green;">yes</span>';
    return '<span style="color:red;">no</span>';
  },

  initEvents: function () {
    var me = this;
    me.fireEvent("saved");
    if (!me.readonly)
      // me.grid.getSelectionModel().on('selection', me.onRowClick, me);
      me.grid.on("itemclick", me.onRowClick, me);
    me.on("close", function (win) {
      if (win.modyfied) win.fireEvent("saved", win);
    });
  },

  action: function (name, url, params, cbsuccess) {
    var me = this;
    Ext.Ajax.request({
      url: url,
      method: "GET",
      params: params,
      scope: me,
      timeout: 120000,
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
              title: name + " fail",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
        if (cbsuccess) cbsuccess.call(me);
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
});
