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
Ext.define("LHCbDIRAC.BookkeepingBrowser.classes.LookupWindow", {
  extend: "Ext.window.Window",
  requires: ["Ext.form.field.ComboBox"],
  alias: "widget.lookup",

  plain: true,
  resizable: false,
  modal: true,
  title: "RunLookup",
  url: null,
  constructor: function (config) {
    var me = this;
    me.callParent(arguments);
  },
  initComponent: function () {
    var me = this;

    var dataStore = Ext.create("Ext.data.Store", {
      proxy: {
        type: "ajax",
        url: me.url,
        reader: {
          type: "json",
          rootProperty: "result",
          successProperty: "success",
        },
      },
      fields: [
        {
          name: "data",
        },
      ],
      autoLoad: true,
      loading: true,
    });
    me.form = Ext.create("widget.form", {
      bodyPadding: "12 10 10",
      border: false,
      unstyled: true,
      items: [
        {
          xtype: "fieldset",
          name: "fieldsetFiletypes",
          title: "Production/RunLookup",
          autoHeight: true,
          items: [
            {
              xtype: "tagfield",
              store: dataStore,
              flex: 1,
              name: me.title,
              forceSelection: true,
              displayField: "data",
              emptyText: "Select items",
              selectOnFocus: true,
              queryMode: "local",
            },
          ],
        },
      ],
    });

    Ext.apply(me, {
      // width : 500,
      // height : 350,
      width: 400,
      height: 250,
      layout: "fit",
      items: me.form,
      buttons: [
        {
          text: "OK",
          handler: function () {
            me.onOK();
          },
        },
        {
          text: "Cancel",
          handler: function () {
            me.onCancel();
          },
        },
      ],
    });
    me.callParent(arguments);
  },
  onOK: function () {
    var me = this;
    me.fireEvent("okPressed");
  },
  onCancel: function () {
    var me = this;
    me.doClose(); // me is the window
  },
});
