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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.RequestSpliter", {
  extend: "Ext.window.Window",
  requires: ["LHCbDIRAC.ProductionRequestManager.classes.RequestDetail", "LHCbDIRAC.ProductionRequestManager.classes.SimpleSubrequestList"],

  alias: "widget.requestspliter",

  plain: true,
  resizable: false,
  modal: true,
  closeAction: "hide",
  initComponent: function () {
    var me = this;
    me.master = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.RequestDetail", {
      ID: me.reqdata.ID,
      minWidth: 200,
      region: "center",
      frame: true,
      title: "Request",
      scrollable: true,
    });

    me.master.on(
      "afterrender",
      function () {
        me.master.updateDetail(me.reqdata);
      },
      me
    );

    me.subrq = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.SimpleSubrequestList", {
      title: "Select subrequest(s) to separate",
      viewConfig: {
        forceFit: true,
      },
    });
    if (!me.reqdata._is_leaf) {
      me.subrq.store.load({
        params: {
          anode: Ext.JSON.encode([me.reqdata.ID]),
        },
      });
    }
    me.subrq.getSelectionModel().on("selectionchange", me.onSubrequestSelection, me);

    me.east = Ext.create("Ext.panel.Panel", {
      region: "east",
      split: true,
      width: 500,
      minWidth: 500,
      border: false,

      layout: "fit",
      items: me.subrq,

      buttonAlign: "center",
      buttons: [
        {
          text: "Split",
          disabled: true,
          name: "rs-split-btn",
          handler: me.onSplit,
          scope: me,
        },
        {
          text: "Cancel",
          handler: me.close,
          scope: me,
        },
      ],
    });

    me.form = Ext.create("Ext.form.Panel", {
      border: false,
      items: {
        xtype: "panel",
        layout: "border",
        frame: true,
        border: false,
        anchor: "100% 100%",
        items: [me.master, me.east],
      },
    });

    Ext.apply(me, {
      width: 950,
      height: 350,
      minWidth: 500,
      minHeight: 300,
      maximizable: true,
      modal: true,
      layout: "fit",
      items: me.form,
    });
    me.callParent(arguments);
  },
  initEvents: function () {
    var me = this;
    me.fireEvent("saved");
  },
  onSubrequestSelection: function (sm) {
    var me = this;

    var sel = sm.getSelection();
    if (!sel.length || sel.length == me.subrq.store.getCount()) me.down("[name=rs-split-btn]").disable();
    else me.down("[name=rs-split-btn]").enable();
  },
  onSplit: function () {
    var me = this;

    var subrIds = [];

    var checkboxcomp = Ext.query("#" + me.id + " input.checkrow");

    for (var i = 0; i < checkboxcomp.length; i++) if (checkboxcomp[i].checked) subrIds.push(parseInt(checkboxcomp[i].value));

    var pdict = {
      ID: me.reqdata.ID,
      Subrequests: Ext.JSON.encode(subrIds),
    };

    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/split",
      method: "POST",
      params: pdict,
      scope: me,
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
              title: "Split request fail",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
          Ext.MessageBox.show({
            title: "Split was successful",
            msg: "New request ID is " + result.Value,
            buttons: Ext.MessageBox.OK,
            icon: Ext.MessageBox.INFO,
          });
        }
        me.fireEvent("saved", me);
        me.close();
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
});
