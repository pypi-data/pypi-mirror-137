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
Ext.define("LHCbDIRAC.BookkeepingBrowser.classes.BookkeepingAddBookmarks", {
  extend: "Ext.window.Window",

  alias: "widget.addBookmark",

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
      bodyStyle: "padding: 5px",
      buttonAlign: "center",
      buttons: [
        {
          iconCls: "dirac-icon-plus",
          handler: function () {
            me.__handleAddBookmark();
          },
          minWidth: "150",
          tooltip: "Add the link in the input field to the bookmark panel",
          text: "Add bookmark",
        },
        {
          iconCls: "toolbar-other-close",
          handler: function () {
            me.doClose();
          },
          minWidth: "100",
          tooltip: "Click here to discard changes and close the window",
          text: "Cancel",
        },
      ],
      items: [
        {
          allowBlank: false,
          anchor: "100%",
          enableKeyEvents: true,
          name: "titleField",
          fieldLabel: "Title",
          selectOnFocus: true,
          xtype: "textfield",
        },
        {
          allowBlank: false,
          anchor: "100%",
          name: "pathField",
          enableKeyEvents: true,
          fieldLabel: "Path",
          selectOnFocus: true,
          xtype: "textfield",
        },
        {
          anchor: "100%",
          fieldLabel: "Tip",
          html: "You can create a bookmark draging a branch or a node from the BK tree and droping it over this window",
          xtype: "label",
        },
      ],
      labelAlign: "top",
    });
    Ext.apply(me, {
      width: 400,
      height: 210,
      title: "Add Bookmark Dialog",
      layout: "fit",
      items: [me.form],
    });
    me.callParent(arguments);
    // set the default title
    var titleIndex = me.form.items.findIndex("name", "titleField");
    var title = me.form.items.getAt(titleIndex);
    title.setRawValue(me.bkkBrowser.fullpath);

    var pathIndex = me.form.items.findIndex("name", "pathField");
    var path = me.form.items.getAt(pathIndex);
    path.setRawValue(me.bkkBrowser.prefix + me.bkkBrowser.fullpath);
  },
  __handleAddBookmark: function () {
    var me = this;
    var data = me.bkkBrowser.__getSelectedData();

    var pathIndex = me.form.items.findIndex("name", "pathField");
    var path = me.form.items.getAt(pathIndex);

    var pathToSave = path.getValue();

    var titleIndex = me.form.items.findIndex("name", "titleField");
    var title = me.form.items.getAt(titleIndex);

    var titleToSave = title.getValue();

    Ext.Ajax.request({
      url: "BookkeepingBrowser/addBookmark",
      params: {
        title: titleToSave,
        path: pathToSave,
      },
      success: function (response) {
        var value = Ext.JSON.decode(response.responseText);
        if (value.success == "false") {
          GLOBAL.APP.CF.alert(value.error, "error");
        } else {
          GLOBAL.APP.CF.alert(value.result, "info");
          me.bkkBrowser.bookmarksPanel.getStore().load();
          me.doClose();
        }
      },
      failure: function (response, opts) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
});
