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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.PrWorkflow", {
  extend: "Ext.window.Window",
  requires: [
    "LHCbDIRAC.ProductionRequestManager.classes.TemplateList",
    "LHCbDIRAC.ProductionRequestManager.classes.TemplateDetail",
    "LHCbDIRAC.ProductionRequestManager.classes.TemplateParList",
    "LHCbDIRAC.ProductionRequestManager.classes.SubrequestList",
  ],

  alias: "widget.prworkflow",

  plain: true,
  resizable: true,
  modal: true,
  closeAction: "hide",
  initComponent: function () {
    var me = this;
    var list = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.TemplateList", {
      region: "center",
      split: true,
      margins: "5 0 5 5",
      minWidth: 300,
    });
    list.getSelectionModel().on("select", me.onTemplateSelect, me);

    me.detail = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.TemplateDetail", {
      region: "east",
      split: true,
      width: 350,
      minWidth: 200,
      margins: "5 5 5 0",

      title: "Template details",
      bodyStyle: "padding-left:15px; padding-top:5px",

      html: "<p>Plese select Template on the left side</p>",
    });

    var template_select = new Ext.Panel({
      name: "prw-template-card",
      layout: "border",
      items: [list, me.detail],
    });

    me.parlist = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.TemplateParList", {
      name: "prw-parlist-card",
      title: "Please specify Production parameters",
    });

    me.parlist.getStore().on("load", me.onTemplateLoad, me);

    me.sublist = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.SubrequestList", {
      name: "prw-subrequest-card",
      title: "Select subrequest(s)",
    });

    if (!me.pData._is_leaf) {
      me.sublist.store.load({
        params: {
          anode: me.pData.ID,
        },
      });
    }

    me.sublist.getSelectionModel().on("selectionchange", me.onSubrequestSelection, me);

    me.scriptlist = Ext.create("Ext.tab.Panel", {
      items: [
        {
          xtype: "textarea",
          title: "Something",
          readOnly: true,
        },
      ],
      enableTabScroll: true,
      layoutOnTabChange: true, // !!! BF: forms bug !!!
      name: "prw-scripts-card",
      activeTab: 0,
    });

    me.wizardPage = 0;
    me.wizardData = [];
    me.wizardGenerated = false;
    me.wizlist = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.TemplateParList", {
      name: "prw-wizlist-card",
      is_wizard: "yes",
      title: "Please specify Production parameters",
    });
    me.wizlist.getStore().on("load", me.onWizardLoad, me);

    Ext.apply(me, {
      title: "Generate production script",
      width: 750,
      height: 350,
      minWidth: 500,
      minHeight: 300,
      maximizable: true,
      modal: true,
      layout: "card",
      activeItem: 0,
      items: [template_select, me.parlist, me.wizlist, me.sublist, me.scriptlist],
      buttonAlign: "right",
      buttons: [
        {
          text: "&laquo; Previous",
          handler: me.onPrevious,
          scope: me,
          name: "prw-prev-btn",
          disabled: true,
        },
        {
          text: "Next &raquo;",
          handler: me.onNext,
          scope: me,
          name: "prw-next-btn",
          disabled: true,
        },
        {
          text: "Generate",
          handler: me.onGenerate,
          scope: me,
          name: "prw-finish-btn",
          disabled: true,
        },
        {
          text: "Preview",
          handler: me.onPreview,
          scope: me,
          name: "prw-preview-btn",
          disabled: true,
        },
        {
          text: "ScriptPreview",
          handler: me.onScriptPreview,
          scope: me,
          name: "prw-spreview-btn",
          disabled: true,
        },
        {
          text: "Cancel",
          handler: me.close,
          scope: me,
        },
      ],
    });
    me.callParent(arguments);
  },
  finishEnable: function () {
    var me = this;
    if (me.detail.data.Type != "Simple") {
      if (GLOBAL.USER_CREDENTIALS.group == "lhcb_prmgr") me.down("[name=prw-finish-btn]").enable();
      me.down("[name=prw-spreview-btn]").enable();
    }
    if (me.detail.data.Type != "Script") me.down("[name=prw-preview-btn]").enable();
  },
  finishDisable: function () {
    var me = this;
    me.down("[name=prw-finish-btn]").disable();
    me.down("[name=prw-preview-btn]").disable();
    me.down("[name=prw-spreview-btn]").disable();
  },
  loadWizard: function (page) {
    var me = this;
    me.down("[name=prw-next-btn]").disable();
    var pdict = {};
    pdict["RequestID"] = me.pData.ID;
    pdict["Wizard"] = me.detail.data.WFName;
    pdict["Page"] = page;
    for (var i = 0; i < page - 1; ++i) Ext.apply(pdict, me.wizardData[i]);
    if (page == me.wizardPage) {
      me.wizardSavedOutput = me.wizardOutput;
      me.wizardGenerated = true;
      pdict["Generate"] = "production";
      var subr = me.sublist.getSelectionModel().getSelection();
      var slist = [];
      for (var i = 0; i < subr.length; ++i) slist = slist.concat([subr[i].data.ID]);
      pdict["Subrequests"] = slist.join(",");
    }
    me.wizardOutput = "";
    me.wizardPage = page;
    me.wizlist.getStore().baseParams = pdict;
    me.wizlist.getStore().load();
  },
  onTemplateSelect: function (sm, row, rec) {
    var me = this;
    var data = row.getData();
    me.down("[name=prw-next-btn]").disable();
    me.finishDisable();
    me.detail.updateDetail(data);

    if (data.WFName.indexOf("_wizard.py") > 0) {
      me.wizardPage = 0;
      me.wizardData = [];
      me.wizardGenerated = false;
      me.loadWizard(1);
    } else {
      me.wizardPage = 0;
      me.parlist.getStore().proxy.extraParams = {
        tpl: data.WFName,
      };
      me.parlist.getStore().load();
    }
  },
  onTemplateLoad: function (st, rec, opt) {
    var me = this;
    if (st.getTotalCount() != 0 || !me.pData._is_leaf) me.down("[name=prw-next-btn]").enable();
    else me.finishEnable();
  },

  showWizardOutput: function () {
    var me = this;
    while (me.scriptlist.items.length) me.scriptlist.remove(me.scriptlist.items.first(0));
    for (var i = 0; i < me.wizardOutput.length; ++i) {
      me.scriptlist
        .add(
          new Ext.form.field.TextArea({
            title: me.wizardOutput[i].ID,
            value: me.wizardOutput[i].Body,
            readOnly: true,
          })
        )
        .show();
    }
    me.layout.setActiveItem(me.down("[name=prw-scripts-card]").id);
  },

  showWizardLastStep: function (decpage) {
    var me = this;
    if (me.wizardPage < 2) {
      me.finishDisable();
      if (!decpage) {
        me.down("[name=prw-next-btn]").disable();
        me.wizardPage = 0;
        me.loadWizard(1);
      } else me.down("[name=prw-next-btn]").enable();
      me.down("[name=prw-prev-btn]").disable();
      me.layout.setActiveItem(me.down("[name=prw-template-card]").id);
    } else {
      me.down("[name=prw-next-btn]").enable();
      me.finishDisable();
      me.down("[name=prw-prev-btn]").disable();
      me.layout.setActiveItem(me.down("[name=prw-wizlist-card]").id);
      var page = me.wizardPage - 1;
      me.wizardPage = 0;
      me.loadWizard(page);
    }
  },

  onWizardLoad: function (st, rec, opt) {
    var me = this;
    me.wizardOutput = st.reader.jsonData.output; // TODO: check st.reader
    if (me.layout.activeItem.name == "prw-wizlist-card" && me.wizlist.getStore().getTotalCount() == 0) {
      // TODO:
      // check
      // the
      // getTotalCount
      me.showWizardOutput();
      if (me.pData._is_leaf) {
        me.down("[name=prw-next-btn]").disable();
        me.down("[name=prw-finish-btn]").enable();
      } else {
        me.down("[name=prw-next-btn]").enable();
        me.down("[name=prw-finish-btn]").disable();
      }
      me.down("[name=prw-prev-btn]").enable();
    } else if (me.layout.activeItem.name == "prw-scripts-card" || me.layout.activeItem.name == "prw-subrequest-card") {
      me.showWizardOutput();
      me.down("[name=prw-next-btn]").disable();
      me.down("[name=prw-finish-btn]").disable();
      me.down("[name=prw-prev-btn]").enable();
    } else {
      me.down("[name=prw-next-btn]").enable();
    }
    if (me.layout.activeItem.name != "prw-template-card") me.down("[name=prw-prev-btn]").enable();
    if (me.wizardData[me.wizardPage - 1]) {
      var recs = me.wizlist.getStore().getRange();
      var pdict = me.wizardData[me.wizardPage - 1];
      for (var i = 0; i < recs.length; ++i) {
        if (recs[i].data.par in pdict) recs[i].set("value", pdict[recs[i].data.par]);
      }
    }
  },

  onSubrequestSelection: function (sm) {
    var me = this;
    var sel = sm.getSelection();
    if (!me.wizardPage) {
      if (!sel.length) me.finishDisable();
      else me.finishEnable();
    } else {
      if (!sel.length) me.down("[name=prw-finish-btn]").disable();
      else me.down("[name=prw-finish-btn]").enable();
    }
  },

  onNext: function () {
    var me = this;
    var sll = me.sublist.getSelectionModel().getSelection().length;
    if (me.layout.activeItem.name == "prw-wizlist-card") {
      var pdict = {};
      var recs = me.wizlist.getStore().getRange();
      for (var i = 0; i < recs.length; ++i) pdict[recs[i].data.par] = recs[i].data.value;
      me.wizardData[me.wizardPage - 1] = pdict;
      me.loadWizard(me.wizardPage + 1);
    } else if (me.layout.activeItem.name == "prw-template-card") {
      if (me.wizardPage > 0) {
        if (me.wizlist.getStore().getTotalCount() == 0) {
          // TODO:
          // getTotalCount!!!
          me.showWizardOutput();
          if (me.pData._is_leaf) {
            me.down("[name=prw-next-btn]").disable();
            me.down("[name=prw-finish-btn]").enable();
          } else {
            me.down("[name=prw-next-btn]").enable();
            me.down("[name=prw-finish-btn]").disable();
          }
        } else {
          me.layout.setActiveItem(me.down("[name=prw-wizlist-card]").id);
        }
        me.down("[name=prw-prev-btn]").enable();
      } else if (me.parlist.getStore().getTotalCount() == 0) {
        me.down("[name=prw-next-btn]").disable();
        if (sll) me.finishEnable();
        else me.finishDisable();
        me.down("[name=prw-prev-btn]").enable();
        me.layout.setActiveItem(me.down("[name=prw-subrequest-card]").id);
      } else {
        if (me.pData._is_leaf) {
          me.down("[name=prw-next-btn]").disable();
          me.finishEnable();
        } else {
          me.down("[name=prw-next-btn]").enable();
          me.finishDisable();
        }
        me.down("[name=prw-prev-btn]").enable();
        me.layout.setActiveItem(me.down("[name=prw-parlist-card]").id);
      }
    } else if (me.layout.activeItem.name == "prw-parlist-card") {
      me.down("[name=prw-next-btn]").disable();
      if (sll) me.finishEnable();
      else me.finishDisable();
      me.layout.setActiveItem(me.down("[name=prw-subrequest-card]").id);
    } else if (me.layout.activeItem.name == "prw-scripts-card") {
      me.down("[name=prw-next-btn]").disable();
      me.layout.setActiveItem(me.down("[name=prw-subrequest-card]").id);
      if (sll) me.down("[name=prw-finish-btn]").enable();
      else me.down("[name=prw-finish-btn]").disable();
      me.down("[name=prw-prev-btn]").enable();
    }
  },
  onPrevious: function () {
    var me = this;
    if (me.wizardPage > 0) {
      if (me.layout.activeItem.name == "prw-scripts-card") {
        if (me.wizardGenerated) {
          me.wizardGenerated = false;
          me.wizardOutput = me.wizardSavedOutput;
          if (me.pData._is_leaf) {
            me.showWizardOutput();
          } else {
            me.layout.setActiveItem(me.down("[name=prw-subrequest-card]").id);
          }
          me.down("[name=prw-next-btn]").disable();
          me.down("[name=prw-finish-btn]").enable();
        } else me.showWizardLastStep(false);
      } else if (me.layout.activeItem.name == "prw-subrequest-card") {
        me.showWizardOutput();
        me.down("[name=prw-next-btn]").enable();
        me.down("[name=prw-prev-btn]").enable();
        me.down("[name=prw-finish-btn]").disable();
      } else me.showWizardLastStep(true);
    } else if (me.layout.activeItem.name == "prw-subrequest-card") {
      if (me.parlist.getStore().getTotalCount() == 0) {
        me.down("[name=prw-next-btn]").enable();
        me.finishDisable();
        me.down("[name=prw-prev-btn]").disable();
        me.layout.setActiveItem(me.down("[name=prw-template-card]").id);
      } else {
        me.down("[name=prw-next-btn]").enable();
        me.finishDisable();
        me.layout.setActiveItem(me.down("[name=prw-parlist-card]").id);
      }
    } else if (me.layout.activeItem.name == "prw-parlist-card") {
      me.down("[name=prw-next-btn]").enable();
      me.finishDisable();
      me.down("[name=prw-prev-btn]").disable();
      me.layout.setActiveItem(me.down("[name=prw-template-card]").id);
    } else if (me.layout.activeItem.name == "prw-scripts-card") {
      if (!me.pData._is_leaf) {
        me.down("[name=prw-next-btn]").disable();
        me.finishDisable();
        me.layout.setActiveItem(me.down("[name=prw-subrequest-card]").id);
      } else {
        if (me.parlist.getStore().getTotalCount() == 0) {
          me.down("[name=prw-next-btn]").disable();
          me.down("[name=prw-prev-btn]").disable();
          me.finishEnable();
          me.layout.setActiveItem(me.down("[name=prw-template-card]").id);
        } else {
          me.down("[name=prw-next-btn]").disable();
          me.down("[name=prw-prev-btn]").enable();
          me.finishEnable();
          me.layout.setActiveItem(me.down("[name=prw-parlist-card]").id);
        }
      }
    }
  },
  onFinish: function () {
    var me = this;
    var pdict = {};
    pdict["RequestID"] = me.pData.ID;
    pdict["Template"] = me.detail.data.WFName;
    var recs = me.parlist.getStore().getRange();
    for (var i = 0; i < recs.length; ++i) pdict[recs[i].data.par] = recs[i].data.value;

    var subr = me.sublist.getSelectionModel().getSelection();
    var slist = [];
    for (i = 0; i < subr.length; ++i) slist = slist.concat([subr[i].data.ID]);
    pdict["Subrequests"] = slist.join(",");

    Ext.Ajax.request({
      url: GLOBAL.BASE_URL + "ProductionRequestManager/create_workflow",
      method: "POST",
      params: pdict,
      scope: me,
      timeout: 120000,
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
              title: "Create Workflow fail",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
        me.close();
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
  onPreview: function () {
    var me = this;
    me.doGenerate("Preview");
  },
  onScriptPreview: function () {
    var me = this;
    me.doGenerate("ScriptPreview");
  },
  onGenerate: function () {
    var me = this;
    if (me.wizardPage > 0) {
      me.down("[name=prw-finish-btn]").disable();
      me.loadWizard(me.wizardPage);
    }
    me.doGenerate("Generate");
  },
  doGenerate: function (operation) {
    var me = this;
    var pdict = {};
    if (me.RequestIDs && me.RequestIDs.length > 0) {
      pdict["RequestIDs"] = Ext.JSON.encode(me.RequestIDs);
    }

    pdict["RequestID"] = me.pData.ID;
    pdict["Template"] = me.detail.data.WFName;
    var recs = this.parlist.getStore().getRange();
    for (var i = 0; i < recs.length; ++i) pdict[recs[i].data.par] = recs[i].data.value;

    var subr = this.sublist.getSelectionModel().getSelection();
    var slist = [];
    for (i = 0; i < subr.length; ++i) slist = slist.concat([subr[i].data.ID]);
    pdict["Subrequests"] = slist.join(",");
    pdict["Operation"] = operation;
    me.layout.getActiveItem().setLoading("Generating the script....");
    Ext.Ajax.request({
      url: GLOBAL.BASE_URL + "ProductionRequestManager/create_workflow",
      method: "POST",
      params: pdict,
      scope: me,
      timeout: 120000,
      success: function (response) {
        me.layout.getActiveItem().setLoading(false);
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
              title: "Create Workflow fail",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
        var sll = me.sublist.getSelectionModel().getSelection().length;
        me.down("[name=prw-next-btn]").disable();
        me.down("[name=prw-finish-btn]").disable();
        me.down("[name=prw-prev-btn]").enable();

        while (me.scriptlist.items.length) me.scriptlist.remove(me.scriptlist.items.first(0));
        for (var i = 0; i < result.Value.length; ++i) {
          me.scriptlist
            .add(
              new Ext.form.field.TextArea({
                title: result.Value[i].ID,
                value: result.Value[i].Body,
                readOnly: true,
              })
            )
            .show();
        }
        me.down("[name=prw-finish-btn]").disable();
        me.layout.setActiveItem(me.down("[name=prw-scripts-card]").id);
        /*
         * Ext.MessageBox.show({ title: 'Production script', msg:
         * result.Value, buttons: Ext.MessageBox.OK, });
         */
      },
      failure: function (response) {
        me.layout.getActiveItem().setLoading(false);
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
});
