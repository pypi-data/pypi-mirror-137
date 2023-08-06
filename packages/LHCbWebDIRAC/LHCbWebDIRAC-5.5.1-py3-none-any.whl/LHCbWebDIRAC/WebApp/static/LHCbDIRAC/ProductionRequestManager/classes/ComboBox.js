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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.ComboBox", {
  extend: "Ext.form.field.ComboBox",

  requires: ["Ext.form.field.ComboBox", "Ext.data.Store", "Ext.data.proxy.Memory", "Ext.data.reader.Json", "Ext.XTemplate"],

  alias: "widget.dirac.combobox",
  /*
   * useOriginalValue - it allows to not use an pbject in a Form submission.
   */
  useOriginalValue: false,

  /*
   * url - URL to get data from
   */
  url: "",

  /*
   * displayField - expect { success: 'true', result: [ { displayField:
   * value}, ... ] } from the server
   */

  /*
   * valueField - if set in addition to displayField (and is different),
   * expect { success: 'true', result: [ { displayField: value, valueField:
   * value }, ... ] } from the server
   */

  /*
   * extraValues - add this values to the beginning of the list, if there
   * are not there
   */
  extraValues: [],

  initComponent: function () {
    var me = this;

    var fields = [
      {
        name: me.displayField,
      },
    ];
    if (me.valueField && me.valueField != me.displayField)
      fields.push({
        name: me.valueField,
      });

    var ajaxStore = new Ext.data.Store({
      proxy: {
        type: "ajax",
        url: me.url,
        reader: {
          type: "json",
          rootProperty: "result",
          successProperty: "success",
        },
      },
      fields: fields,
      autoLoad: true,
      loading: true,
      listeners: {
        load: {
          fn: me.__onStoreLoad,
          scope: me,
        },
      },
    });

    Ext.apply(me, {
      store: ajaxStore,
      queryMode: "local",
    });
    me.callParent(arguments);
  },

  __insertValue: function (i, value) {
    var me = this;
    if (value == "") return;
    var store = me.getStore();
    var extraRow = {};
    extraRow[me.displayField] = value;
    if (me.valueField != me.displayField) extraRow[me.valueField] = value;
    store.insert(i, [extraRow]);
  },

  /*
   * Prepend extraValues to the store
   */
  __onStoreLoad: function (store, records, successful, op) {
    var me = this;

    if (!me.extraValues) return;

    if (!successful) store.removeAll();

    for (var i = 0; i < me.extraValues.length; ++i) {
      var value = me.extraValues[i];
      if ((i > 0 && value == "") || store.find(me.displayField, value) >= 0) continue;
      me.__insertValue(i, value);
    }
  },

  /*
   * Append extraValue, visualize it and reload
   */
  setAndReload: function (value, params) {
    var me = this;
    params = typeof params == "undefined" ? {} : params;
    var store = me.getStore();
    if (me.extraValues && me.extraValues[0] == "") me.extraValues = [""];
    else me.extraValues = [];
    if (value != "") me.extraValues.push(value);
    /*
     * if( store.find( me.displayField, value) < 0 ) me.__insertValue( 0,
     * value );
     */
    store.removeAll(false);
    me.__insertValue(0, value);
    me.setValue(value);
    store.load(params);
  },
  getValue: function () {
    var me = this;
    var comboValue = "";

    if (me.useOriginalValue) {
      comboValue = me.superclass.getValue.call(me);
    } else {
      comboValue = me.getRawValue();
    }
    return comboValue;
  },
});
