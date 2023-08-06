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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.TemplateDetail", {
  extend: "Ext.panel.Panel",
  tplMarkup: ["<b>Name:</b> {display_name}<br/>"],

  initComponent: function () {
    var me = this;
    me.tpl = new Ext.Template(me.tplMarkup);
    me.data = {};
    me.callParent(arguments);
  },

  updateDetail: function (data) {
    var me = this;
    me.data = data;
    me.data.display_name = data.WFName.replace(/_wizard\.py/, "");
    me.tpl.overwrite(me.body, me.data);
  },
});
