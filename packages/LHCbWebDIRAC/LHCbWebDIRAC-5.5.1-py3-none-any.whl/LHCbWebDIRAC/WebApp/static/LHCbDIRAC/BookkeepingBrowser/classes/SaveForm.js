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
Ext.define("LHCbDIRAC.BookkeepingBrowser.classes.SaveForm", {
  extend: "Ext.window.Window",
  requires: ["Ext.util.*", "LHCbDIRAC.BookkeepingBrowser.classes.AdvancedSaveWindow"],
  alias: "widget.saveForm",

  plain: true,
  resizable: false,
  modal: true,
  constructor: function (config) {
    var me = this;
    me.callParent(arguments);
  },
  initComponent: function () {
    var me = this;

    me.form = Ext.create("widget.form", {
      bodyPadding: "12 10 10",
      border: false,
      unstyled: true,
      items: [
        {
          xtype: "fieldset",
          title: "File Type",
          autoHeight: true,
          defaultType: "radiogroup",
          items: [
            {
              xtype: "radiogroup",
              name: "filetype",
              columns: 1,
              vertical: true,
              listeners: {
                change: function (elm, newValue, oldValue) {
                  var textField = Ext.ComponentQuery.query("textfield[name=fname]", me)[0];
                  var filename = textField.getValue().trim();
                  // Remove the old file extension (if necessary)
                  const oldExtension = "." + oldValue.filetype;
                  if (filename.endsWith(oldExtension)) {
                    filename = filename.slice(0, -oldExtension.length);
                  }
                  textField.setValue(filename + "." + newValue.filetype);
                },
              },
              items: [
                {
                  boxLabel: "Save as a text file (*.txt)",
                  inputValue: "txt",
                  checked: true,
                },
                {
                  boxLabel: "Save as a python file (*.py)",
                  inputValue: "py",
                },
                {
                  boxLabel: "Save as a CSV file (*.csv)",
                  inputValue: "csv",
                },
              ],
            },
          ],
        },
        {
          xtype: "fieldset",
          name: "fieldsetRecords",
          title: "Records",
          layout: {
            type: "hbox",
          },
          defaults: {
            grow: true,
            labelAlign: "right",
          },
          items: [
            {
              xtype: "radiofield",
              boxLabel: "All",
              name: "records",
              flex: 1,
              checked: true,
            },
            {
              xtype: "radiofield",
              boxLabel: "Records",
              name: "records",
              flex: 1,
              listeners: {
                change: function (elm, newValue, oldValue) {
                  var parent = this.up("fieldset");
                  var fromField = Ext.ComponentQuery.query("numberfield[name=from]", parent)[0];
                  fromField.setDisabled(!fromField.isDisabled());
                  var toField = Ext.ComponentQuery.query("numberfield[name=to]", parent)[0];
                  toField.setDisabled(!toField.isDisabled());
                },
              },
            },
            {
              xtype: "numberfield",
              name: "from",
              fieldLabel: "From",
              labelWidth: 40,
              flex: 2,
              minValue: 0,
              value: 0,
              disabled: true,
            },
            {
              xtype: "numberfield",
              name: "to",
              fieldLabel: "To",
              labelWidth: 40,
              flex: 2,
              minValue: 1,
              value: 100,
              disabled: true,
            },
          ],
        },
      ],
    });

    Ext.apply(me, {
      width: 500,
      height: 350,
      title: "Save Dialog",
      layout: "fit",
      items: me.form,
      buttons: [
        {
          text: "Save",
          handler: function () {
            me.onSave();
          },
        },
        {
          text: "Advanced Save",
          handler: function () {
            me.onAdvancedSave();
          },
        },
        {
          text: "Cancel",
          handler: function () {
            me.onCancel();
          },
        },
        {
          text: "Info",
          handler: function () {
            me.onInfo();
          },
        },
      ],
    });
    me.callParent(arguments);
    var path = "";
    for (var i = 1; i < me.scope.fullpath.length; i++) {
      if (me.scope.fullpath[i] == "/") {
        path += "_";
      } else if (me.scope.fullpath[i] == "," || me.scope.fullpath[i] == "-" || me.scope.fullpath[i] == "") {
        continue;
      } else {
        path += me.scope.fullpath[i];
      }
    }
    path += "." + Ext.ComponentQuery.query("radiogroup[name=filetype]", me)[0].getValue().filetype;

    me.form.add({
      xtype: "fieldset",
      name: "saveAs",
      title: "Save As...",
      autoHeight: true,
      defaultType: "textfield",
      items: [
        {
          labelAlign: "top",
          width: "auto",
          name: "fname",
          readOnly: false,
          value: path,
          grow: true,
        },
      ],
    });
  },
  onCancel: function () {
    var me = this;
    me.doClose(); // me is the window
  },
  onInfo: function () {
    var me = this;
    var datastore = new Ext.data.JsonStore({
      autoLoad: true,

      proxy: {
        type: "ajax",
        url: "BookkeepingBrowser/getStatistics",
        reader: {
          type: "json",
          rootProperty: "result",
          idProperty: "name",
        },
      },

      fields: [
        {
          name: "nbfiles",
        },
        {
          name: "nbevents",
        },
        {
          name: "fsize",
        },
      ],
    });

    datastore.proxy.extraParams = me.__createExtraParams();

    var tpl = new Ext.XTemplate(
      '<tpl for=".">',
      '<div style="margin-bottom: 10px;" class="dataset-statistics">',
      "<br/>Number of files:<span>{nbfiles}</span>",
      "<br/>Number of events:<span>{nbevents}</span>",
      "<br/>File Size:<span>{fsize}</span>",
      "</div>",
      "</tpl>"
    );
    var panel = new Ext.Panel({
      items: new Ext.view.View({
        store: datastore,
        tpl: tpl,
        itemSelector: "div.dataset-statistics",
        autoHeight: true,
      }),
      bodyStyle: "padding: 5px",
    });
    // TODO use the proper method...
    var window = Ext.create("Ext.window.Window", {
      plain: true,
      resizable: false,
      modal: false,
      width: 300,
      height: 120,
    });
    window.add(panel);
    window.show();
  },
  onSave: function () {
    var me = this;

    const format = Ext.ComponentQuery.query("radiogroup[name=filetype]", me)[0].getValue().filetype;
    const filename = Ext.ComponentQuery.query("textfield[name=fname]", me)[0].getValue();

    var params = me.__createExtraParams();
    params.format = format;
    params.filename = filename;
    var bkQuery = me.bkQuery;
    if (params["TCK"].length > 0) {
      bkQuery["TCK"] = params["TCK"];
    } else {
      delete bkQuery["TCK"];
    }
    params.bkQuery = Ext.JSON.encode(bkQuery);

    var handleException = function (response, options) {
      var result = Ext.decode(response.responseText, true);
      var blob = new Blob([response.responseText], {
        type: "text/plain;charset=utf-8",
      });
      _global.saveAs(blob, filename);
      if (result) {
        Ext.Msg.alert("Message", result["message"]);
      }
    };

    Ext.Ajax.request({
      url: "BookkeepingBrowser/saveDataSet",
      params: params,
      isUpload: true,
      scope: me,
      success: function (response, options) {
        var blob = new Blob([response.responseText], {
          type: "text/plain;charset=utf-8",
        });
        _global.saveAs(blob, filename);
      },
      failure: function (response, options) {
        Ext.Msg.alert("ERROR: Saving dataset failed!", response.responseText.substr(0, 1000));
      },
    });
  },
  __createExtraParams: function () {
    var me = this;
    var extraParams = me.scope.__getSelectedData();
    extraParams["fullpath"] = me.scope.fullpath;

    const allradioButton = Ext.ComponentQuery.query('radiofield[name="records"][boxLabel="All"]', me)[0].getValue();
    if (allradioButton) {
      extraParams.start = 0;
      extraParams.limit = me.scope.grid.getStore().getProxy().getReader().rawData.total;
    } else {
      const fromField = Ext.ComponentQuery.query("numberfield[name=from]", me)[0];
      const toField = Ext.ComponentQuery.query("numberfield[name=to]", me)[0];
      extraParams.start = fromField.getValue();
      extraParams.limit = toField.getValue();
    }
    return extraParams;
  },
  onAdvancedSave: function () {
    var me = this;
    var advSave = Ext.create("LHCbDIRAC.BookkeepingBrowser.classes.AdvancedSaveWindow", {
      applicationName: me.scope.applicationName,
    });
    advSave.show();
    advSave.on("okPressed", function () {
      var values = advSave.getValues();
      if (values) {
        // Close the window
        advSave.onCancel();

        me.setLoading("Creating pool xml catalog...");

        var params = me.__createExtraParams();
        const filename = Ext.ComponentQuery.query("textfield[name=fname]", me)[0].getValue();
        params.fileName = filename;
        var bkQuery = me.bkQuery;
        if (params["TCK"].length > 0) {
          bkQuery["TCK"] = params["TCK"];
        } else {
          delete bkQuery["TCK"];
        }
        params.bkQuery = Ext.JSON.encode(bkQuery);
        params.formatType = values.formatType;
        params.SiteName = values.SiteName;

        Ext.Ajax.request({
          url: "BookkeepingBrowser/createCatalog",
          params: params,
          binary: true,
          scope: me,
          success: function (response, options) {
            me.setLoading(false);
            var blob = new Blob([response.responseBytes], {
              type: response.getResponseHeader("content-type"),
            });
            _global.saveAs(blob, filename + ".tar.gz");
          },
          failure: function (response, options) {
            me.setLoading(false);
            Ext.Msg.alert("ERROR: Saving dataset failed!", response.responseText.substr(0, 1000));
          },
        });
      }
    });
  },
});
