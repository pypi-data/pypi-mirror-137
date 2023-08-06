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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.TemplateParList", {
  extend: "Ext.grid.Panel",

  initComponent: function () {
    var me = this;
    var url = "";
    if (me.is_test) url = GLOBAL.BASE_URL + "ProductionRequestManager/test_parlist";
    else if (this.is_wizard) url = GLOBAL.BASE_URL + "ProductionRequestManager/run_wizard";
    else url = GLOBAL.BASE_URL + "ProductionRequestManager/template_parlist";

    me.store = Ext.create("Ext.data.JsonStore", {
      autoLoad: false,
      fields: ["par", "label", "value", "default"],
      remoteSort: false,
      sorters: [
        {
          property: "label",
          direction: "ASC",
        },
      ],
      proxy: {
        type: "ajax",
        url: url,
        reader: {
          type: "json",
          rootProperty: "result",
        },
      },
    });

    Ext.apply(me, {
      columns: [
        {
          header: "Parameter",
          sortable: true,
          flex: true,
          dataIndex: "label",
        },
        {
          header: "Value",
          sortable: false,
          dataIndex: "value",
          editor: {
            allowBlank: true,
          },
        },
      ],
      plugins: Ext.create("Ext.grid.plugin.CellEditing", {
        clicksToEdit: 1,
      }),
      autoHeight: false,
      autoWidth: true,
      loadMask: true,
      // region : 'center',
      store: me.store,
      stripeRows: true,
      viewConfig: {
        forceFit: true,
      },
    });
    // me.store.sort('label', 'ASC');
    // me.store.lastRequest = Ext.Ajax.getLatest();
    //Ext.Ajax.abort(me.store.lastRequest);

    me.callParent(arguments);
  },
});
