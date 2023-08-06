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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.RequestPriorityEditor", {
  extend: "Ext.window.Window",
  plain: true,
  resizable: false,
  modal: true,
  initComponent: function () {
    var me = this;

    me.form = Ext.create("widget.form", {
      bodyPadding: "12 10 10",
      minWidth: 200,
      border: false,
      unstyled: true,
      items: [
        {
          xtype: "combo",
          fieldLabel: "Priority",
          name: "reqPrio",
          store: ["1a", "1b", "2a", "2b"],
          forceSelection: true,
          mode: "local",
          selectOnFocus: true,
          columnWidth: 0.25,
        },
      ],
    });
    Ext.apply(me, {
      width: 500,
      title: "Please select a priority:",
      layout: "fit",
      items: me.form,
      buttons: [
        {
          xtype: "button",
          text: "Set Priority",
          scope: me,
          handler: me.onSetClick,
        },
        {
          xtype: "button",
          text: "Cancel",
          scope: me,
          handler: me.doHide,
        },
      ],
    });
    me.callParent(arguments);
  },

  doHide: function () {
    this.hide();
  },

  onSetClick: function (addBtn) {
    var me = this;
    var value = me.form.getValues()["reqPrio"];
    if (value == "") return;
    me.fireEvent("setClick", value);
    me.close();
    me.destroy();
  },
});
