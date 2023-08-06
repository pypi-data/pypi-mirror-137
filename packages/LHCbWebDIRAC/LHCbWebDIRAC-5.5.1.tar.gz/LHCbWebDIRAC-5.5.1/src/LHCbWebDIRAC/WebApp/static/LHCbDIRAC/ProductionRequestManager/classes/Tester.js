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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.Tester", {
  extend: "Ext.window.Window",
  requires: [
    "LHCbDIRAC.ProductionRequestManager.classes.TestStatus",
    "LHCbDIRAC.ProductionRequestManager.classes.TestList",
    "LHCbDIRAC.ProductionRequestManager.classes.TemplateDetail",
  ],

  alias: "widget.tester",

  plain: true,
  resizable: false,
  modal: true,
  closeAction: "hide",
  initComponent: function () {
    var me = this;

    me.status = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.TestStatus", {
      pData: me.pData,
      name: "prw-tests-card",
    });

    me.status.getSelectionModel().on("selectionchange", me.onSubrequestSelection, me);

    me.list = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.TestList", {
      region: "center",
      split: true,
      margins: "5 0 5 5",
      minWidth: 300,
    });
    me.list.getSelectionModel().on("select", me.onTemplateSelect, me);

    me.detail = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.TemplateDetail", {
      region: "east",
      split: true,
      width: 350,
      minWidth: 200,
      margins: "5 5 5 0",

      title: "Test details",
      bodyStyle: "padding-left:15px; padding-top:5px",

      html: "<p>Plese select test kind on the left side</p>",
    });

    template_select = Ext.create("Ext.panel.Panel", {
      name: "prw-template-card",
      layout: "border",
      items: [me.list, me.detail],
    });

    me.parlist = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.TemplateParList", {
      is_test: "yes",
      name: "prw-parlist-card",
      title: "Please specify Test parameters",
    });
    me.parlist.getStore().on("load", me.onTemplateLoad, this);

    Ext.apply(me, {
      title: "Test(s) for request " + me.pData.ID,
      width: 750,
      height: 350,
      minWidth: 500,
      minHeight: 300,
      maximizable: true,
      modal: true,
      layout: "card",
      activeItem: 0,
      items: [me.status, template_select, me.parlist],
      buttonAlign: "right",
      buttons: [
        {
          text: "&laquo; Previous",
          handler: this.onPrevious,
          scope: this,
          name: "prw-prev-btn",
          disabled: true,
        },
        {
          text: "Next &raquo;",
          handler: this.onNext,
          scope: this,
          name: "prw-next-btn",
          disabled: true,
        },
        {
          text: "Submit test(s)",
          handler: this.onSubmit,
          scope: this,
          name: "prw-submit-btn",
          disabled: true,
        },
      ],
    });

    me.callParent(arguments);
  },
  finishEnable: function () {
    var me = this;
    me.down("[name=prw-submit-btn]").enable();
  },
  finishDisable: function () {
    var me = this;
    me.down("[name=prw-submit-btn]").disable();
  },
  onTemplateSelect: function (sm, row, rec) {
    var me = this;
    me.down("[name=prw-next-btn]").enable();
    me.finishDisable();
    me.detail.updateDetail(row.data);
    me.parlist.getStore().load({
      params: {
        tpl: row.data.WFName,
      },
    });
  },
  onTemplateLoad: function (st, rec, opt) {
    var me = this;
    me.templateLoaded = true;
    if (st.getTotalCount() != 0) me.down("[name=prw-next-btn]").enable();
    else me.finishEnable();
  },
  onSubrequestSelection: function (sm) {
    var me = this;
    if (!sm.getSelection().length) me.down("[name=prw-next-btn]").disable();
    else me.down("[name=prw-next-btn]").enable();
  },
  onNext: function () {
    var me = this;
    sll = me.status.getSelectionModel().getSelection().length;
    if (me.layout.activeItem.name == "prw-tests-card") {
      if (me.templateLoaded) {
        if (me.parlist.getStore().getTotalCount() == 0) {
          me.down("[name=prw-next-btn]").disable();
          me.finishEnable();
        } else {
          me.down("[name=prw-next-btn]").enable();
          me.finishDisable();
        }
      } else me.down("[name=prw-next-btn]").disable();
      me.down("[name=prw-prev-btn]").enable();
      me.layout.setActiveItem(me.down("[name=prw-template-card]").id);
    } else if (me.layout.activeItem.name == "prw-template-card") {
      me.down("[name=prw-next-btn]").disable();
      me.finishEnable();
      me.layout.setActiveItem(me.down("[name=prw-parlist-card]").id);
    }
  },
  onPrevious: function () {
    var me = this;
    if (me.layout.activeItem.name == "prw-template-card") {
      me.finishDisable();
      me.down("[name=prw-prev-btn]").disable();
      me.down("[name=prw-next-btn]").enable();
      me.layout.setActiveItem(me.down("[name=prw-tests-card]").id);
    } else if (me.layout.activeItem.name == "prw-parlist-card") {
      if (me.parlist.getStore().getTotalCount() == 0) {
        me.down("[name=prw-next-btn]").disable();
        me.finishEnable();
      } else {
        me.down("[name=prw-next-btn]").enable();
        me.finishDisable();
      }
      me.down("[name=prw-prev-btn]").enable();
      me.layout.setActiveItem(me.down("[name=prw-template-card]").id);
    }
  },
  onSubmit: function () {
    var me = this;
    var pdict = {};
    pdict["RequestID"] = me.pData.ID;
    pdict["Template"] = me.detail.data.WFName;
    var recs = me.parlist.getStore().getRange();
    for (var i = 0; i < recs.length; ++i) pdict[recs[i].data.par] = recs[i].data.value;

    var subr = me.status.getSelectionModel().getSelection();
    var slist = [];
    for (i = 0; i < subr.length; ++i) slist = slist.concat([subr[i].data.RequestID]);
    pdict["Subrequests"] = slist.join(",");

    var conn = new Ext.data.Connection();
    conn.request({
      url: GLOBAL.BASE_URL + "ProductionRequestManager/submit_test",
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
              title: "Test submit failed",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
        me.down("[name=prw-next-btn]").enable();
        me.finishDisable();
        me.down("[name=prw-prev-btn]").disable();
        me.layout.setActiveItem(me.down("[name=prw-tests-card]").id);
        me.status.store.reload();
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
});
