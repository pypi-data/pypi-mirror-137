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
Ext.define("LHCbDIRAC.BookkeepingBrowser.classes.AdvancedSaveWindow", {
  extend: "Ext.window.Window",
  requires: ["Ext.form.field.ComboBox"],
  alias: "widget.lookup",

  plain: true,
  resizable: false,
  modal: true,
  title: "Advanced Save...",
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
        url: GLOBAL.BASE_URL + me.applicationName + "/t1sites",
        reader: {
          type: "json",
          rootProperty: "result",
          successProperty: "success",
        },
      },
      fields: [
        {
          name: "Name",
        },
        {
          name: "Value",
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
          name: "fieldsetsites",
          title: "List of Tier-0/1 sites...",
          autoHeight: true,
          items: [
            {
              xtype: "combobox",
              store: dataStore,
              flex: 1,
              name: "SiteName",
              forceSelection: true,
              displayField: "Name",
              emptyText: "Select site",
              selectOnFocus: true,
              queryMode: "local",
              validator: function (value) {
                var me = this;
                if (value == "") return false;
                else return true;
              },
            },
          ],
        },
        {
          xtype: "fieldset",
          defaults: {
            anchor: "100%",
          },
          items: [
            {
              xtype: "radiogroup",
              layout: {
                autoFlex: false,
              },
              columns: 1,
              vertical: true,
              defaults: {
                name: "formatType",
                margin: "0 15 0 0",
              },
              items: [
                {
                  boxLabel: "LFN(s)",
                  inputValue: "lfn",
                  checked: true,
                },
                {
                  boxLabel: "PFN(s)",
                  inputValue: "pfn",
                },
              ],
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
  getValues: function () {
    var me = this;
    var values = null;
    if (me.form.isValid()) {
      values = me.form.getValues();
    }
    return values;
  },
});
