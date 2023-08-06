<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

    <link rel="stylesheet" type="text/css" href="/DIRAC/static/extjs/ext-4.2.1.883/resources/css/ext-all-neptune-debug.css" />
    <link rel="stylesheet" type="text/css" href="/DIRAC/static/core/css/css.css" />
  {% autoescape None %}
    <!-- GC -->

    <!-- <x-compile> -->
    <!-- <x-bootstrap> -->

    <!-- </x-bootstrap> -->
    <script type="text/javascript">

     Ext.Loader.setPath({
            'LHCbDIRAC': '/DIRAC/static/LHCbDIRAC',
            'Ext.dirac.core': '/DIRAC/static/core/js/core',
            'Ext.dirac.utils': '/DIRAC/static/core/js/utils',
            'Ext.ux.form':'/DIRAC/static/extjs/ext-4.2.1.883/examples/ux/form'
         });

        Ext.require('LHCbDIRAC.Accounting.classes.Accounting');

    </script>
    <!-- </x-compile> -->
</head>

<body>
</body>
</html>

sencha -sdk /Users/zoltanmathe/tmp/DIRAC/WebAppDIRAC/WebApp/static/extjs/ext-4.2.1.883/src compile -classpath=/Users/zoltanmathe/tmp/DIRAC/WebAppDIRAC/WebApp/static/core/js/utils,/Users/zoltanmathe/tmp/DIRAC/WebAppDIRAC/WebApp/static/core/js/core,/Users/zoltanmathe/tmp/DIRAC/WebAppDIRAC/WebApp/static/extjs/ext-4.2.1.883/examples/ux/form,/Users/zoltanmathe/tmp/DIRAC/WebAppDIRAC/WebApp/static/LHCbDIRAC/Accounting/classes -debug=true page -name=page -in /Users/zoltanmathe/tmp/DIRAC/WebAppDIRAC/WebApp/CompileTeplates/lhcb_appAcounting.tpl -out /Users/zoltanmathe/tmp/DIRAC/WebAppDIRAC/WebApp/static/LHCbDIRAC/Accounting/build/index.html and restore page and exclude -not -namespace Ext.dirac.*,DIRAC.*,LHCbDIRAC.* and concat -yui /Users/zoltanmathe/tmp/DIRAC/WebAppDIRAC/WebApp/static/LHCbDIRAC/Accounting/build/Accounting.js

sencha -sdk /opt/dirac/WebPrototype/WebAppDIRAC/WebApp/static/extjs/ext-4.2.1.883/src compile -classpath=/opt/dirac/WebPrototype/WebAppDIRAC/WebApp/static/core/js/utils,/opt/dirac/WebPrototype/WebAppDIRAC/WebApp/static/core/js/core,/opt/dirac/WebPrototype/WebAppDIRAC/WebApp/static/extjs/ext-4.2.1.883/examples/ux/form,/opt/dirac/WebPrototype/WebAppDIRAC/WebApp/static/DIRAC/AccountingPlot/classes,/opt/dirac/WebPrototype/LHCbWebDIRAC/WebApp/static/LHCbDIRAC/Accounting/classes -debug=true page -name=page -in /opt/dirac/WebPrototype/LHCbWebDIRAC/WebApp/CompileTeplates/lhcb_appAcounting.tpl -out /opt/dirac/WebPrototype/DIRAC/LHCbWebDIRAC/WebApp/static/LHCbDIRAC/Accounting/build/index.html and restore page and exclude -not -namespace Ext.dirac.*,DIRAC.*,LHCbDIRAC.* and concat -yui /opt/dirac/WebPrototype/LHCbWebDIRAC/WebApp/static/LHCbDIRAC/Accounting/build/Accounting.js
