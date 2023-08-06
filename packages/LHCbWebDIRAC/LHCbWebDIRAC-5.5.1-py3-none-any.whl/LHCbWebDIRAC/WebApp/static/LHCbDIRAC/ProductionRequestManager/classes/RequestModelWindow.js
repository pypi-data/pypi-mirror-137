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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.RequestModelWindow", {
  extend: "Ext.window.Window",

  alias: "widget.requestwindow",

  plain: true,
  resizable: false,
  modal: true,
  closeAction: "hide",

  initComponent: function () {
    var me = this;
    me.fireEvent("create");

    me.form = Ext.create("widget.form", {
      bodyPadding: "12 10 10",
      border: false,
      unstyled: true,
      items: [
        {
          anchor: "100%",
          fieldLabel: "Request Type",
          name: "reqType",
          forceSelection: true,
          displayField: "Description",
          valueField: "Name",
          useOriginalValue: true,
          queryMode: "local",
          labelAlign: "top",
          msgTarget: "under",
          anyMatch: true,
          xtype: "dirac.combobox",
          url: GLOBAL.BASE_URL + "ProductionRequestManager/typeandmodels",
        },
      ],
    });
    Ext.apply(me, {
      width: 500,
      title: "Please select Request Type or model",
      layout: "fit",
      items: me.form,
      buttons: [
        {
          xtype: "button",
          text: "Create request",
          scope: me,
          handler: me.onCreateClick,
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

  onCreateClick: function (addBtn) {
    var me = this;
    var value = me.form.getValues()["reqType"];
    if (value == "") return;
    me.fireEvent("create", value);
    me.close();
    me.destroy();
  },
});
