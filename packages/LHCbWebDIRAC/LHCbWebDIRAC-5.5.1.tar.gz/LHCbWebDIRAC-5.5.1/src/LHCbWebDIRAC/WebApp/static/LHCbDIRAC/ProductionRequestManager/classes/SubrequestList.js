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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.SubrequestList", {
  extend: "Ext.grid.Panel",

  initComponent: function () {
    var me = this;

    me.store = Ext.create("Ext.data.JsonStore", {
      remoteSort: false,
      name: "ID",
      fields: [
        {
          name: "ID",
          type: "auto",
        },
        {
          name: "eventType",
        },
        {
          name: "eventNumber",
        },
        {
          name: "eventBK",
        },
        {
          name: "progress",
        },
        {
          name: "eventText",
        },
      ],
      proxy: {
        type: "ajax",
        url: GLOBAL.BASE_URL + "ProductionRequestManager/list",
        reader: {
          type: "json",
          rootProperty: "result",
        },
      },
    });

    me.store.sort("ID", "ASC");

    var sm = Ext.create("Ext.selection.CheckboxModel");

    Ext.apply(me, {
      selModel: sm,
      columns: [
        {
          name: "Id",
          header: "Id",
          sortable: true,
          dataIndex: "ID",
          width: 40,
        },
        {
          header: "Event type",
          sortable: true,
          dataIndex: "eventType",
        },
        {
          header: "Events requested",
          sortable: true,
          dataIndex: "eventNumber",
        },
        {
          header: "Events in BK",
          dataIndex: "eventBK",
        },
        {
          header: "Progress (%)",
          dataIndex: "progress",
        },
      ],
      autoHeight: false,
      autoWidth: true,
      loadMask: true,
      columnLines: true,
      region: "center",
      store: me.store,
      stripeRows: true,
      viewConfig: {
        forceFit: true,
      },
    });
    me.callParent(arguments);
  },
  rendererChkBox: function (val) {
    return '<input value="' + val + '" type="checkbox" class="checkrow" style="margin:0px;padding:0px"/>';
  },
});
